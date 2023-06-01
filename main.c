#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "sorting.h"

//#define VET_TRANSP
#define VETS_FILENAME "./csvs_2/vetor_transparencia.txt"

double calculate_time(clock_t start, clock_t end) {
    return ((double) (end - start)) / CLOCKS_PER_SEC;
}

void test_case(int n, char* mer_filename, char* ins_filename, char* rad_filename) {
    FILE* f_mer = fopen(mer_filename, "a+");
    FILE* f_ins = fopen(ins_filename, "a+");
    FILE* f_rad = fopen(rad_filename, "a+");

    #ifdef VET_TRANSP
    FILE* f_vets = fopen(VETS_FILENAME, "a+"); // Transparencias dos valores dos vetores
    #endif

    FILE* files[3] = {f_mer, f_ins, f_rad};

    // Um vetor para cada caso de teste
    int **vets = malloc(3 * sizeof(int*));
    for (int i=0; i<3; i++)
        vets[i] = malloc(n * sizeof(int));

    // Populando os vetores com valores aleatorios
    for (int i=0; i<n; i++) {
        int val = rand() % 2000000; // Valores ate 2 milhoes
        vets[0][i] = val;
        vets[1][i] = val;
        vets[2][i] = val;
    }

    // Registrando o valor de n
    for (int i=0; i<3; i++) {
        fprintf(files[i], "%d, ", n);
    }
    
    // Se escolhido, registrar transparencia do vetor
    #ifdef VET_TRANSP
    printf("Registrando p n=%d\n", n);
    fprintf(f_vets, "VETOR N=%d\n", n);
    for (int i=0; i<n; i++) {
        fprintf(f_vets, "%d, ", vets[0][i]);
    }
    fprintf(f_vets, "\n\n");
    #endif

    // Experimentos
    clock_t start, end;
    double time;
    for (int i=0; i<3; i++) {

        // start = clock() dentro dos cases para evitar contabilizar 
        // o tempo de execucao das instrucoes de branch do switch statement
        switch (i) {
        case 0:
            start = clock();
            mergeSort(vets[0], 0, n-1);
            break;
        
        case 1:
            if (n>409600) {
                printf("Tempo inviavel para insertion sort. Pulando...\n");
                continue;
            }
            start = clock();
            insertionSort(vets[1], n);
            break;
        
        case 2:
            start = clock();
            radixSort(vets[2], n);
            break;
        }

        end = clock();
        time = calculate_time(start, end);
        printf("Experimento n=%d terminado para o metodo numero %d -> tempo = %lf\n", n, i, time);

        fprintf(files[i], "%lf\n", time);
    }

    #ifdef VET_TRANSP
    fprintf(f_vets, "VETOR N=%d (ORDENADO)\n", n);
    for (int i=0; i<n; i++) {
        fprintf(f_vets, "%d, ", vets[0][i]);
    }
    fprintf(f_vets, "\n\n");
    fclose(f_vets);
    #endif

    for (int i=0; i<3; i++)
        free(vets[i]);
    free(vets);

    fclose(f_mer);
    fclose(f_ins);
    fclose(f_rad);
}


int main() {
    srand(76); // Para capacidade de repetir os experimentos
    // Para o Insertion Sort i<=13
    // A partir desse momento comeca a ficar muito lento
    for (int i=0; i<=22; i++)
        for (int j=0; j<20; j++)
            test_case((int) 100*pow(2, i), "./csvs_2/merge_test.csv", "./csvs_2/ins_test.csv", "./csvs_2/rad_test.csv");

    return 0;
}