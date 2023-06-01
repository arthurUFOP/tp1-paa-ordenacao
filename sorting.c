#include <stdlib.h>
#include "sorting.h"

void conquistar(int *v, int inicio, int meio, int fim) {
    int *vetEsq = malloc((meio - inicio + 1) * sizeof(int));
    int *vetDir = malloc((fim-(meio+1)+1) * sizeof(int));
    int maxI = meio - inicio;
    int maxJ = fim - (meio+1);
    int i = 0, j=0;
    int index = inicio;
    for (int z=inicio; z<=meio; z++) {
        vetEsq[i] = v[z];
        i++;
    }
    i=0;
    for (int z=meio+1; z<=fim; z++) {
        vetDir[i] = v[z];
        i++;
    }
    i=0;

    while (i<=maxI && j<=maxJ) {
        if (vetEsq[i] <= vetDir[j]) {
            v[index] = vetEsq[i];
            i++;
        }
        else {
            v[index] = vetDir[j];
            j++;
        }
        index++;
    }

    while (i<=maxI) {
        v[index] = vetEsq[i];
        i++;
        index++;
    }

    while (j<=maxJ) {
        v[index] = vetDir[j];
        j++;
        index++;
    }

    free(vetEsq);
    free(vetDir);
}

void mergeSort(int *v, int inicio, int fim) {
    if (inicio < fim) {
        int meio = (inicio + fim) / 2;
        mergeSort(v, inicio, meio);
        mergeSort(v, meio+1, fim);
        conquistar(v, inicio, meio, fim);
    }
}

void insertionSort(int *v, int n) {
    for (int i=1; i<n; i++) {
        int j=i;
        int temp = v[j];
        while (j>0 && temp<v[j-1]) {
            v[j] = v[j-1];
            j--;
        }
        v[j] = temp;
    }
}

void radixSort(int *v, int n) {
    
    int max_val = v[0];
    for (int i=1; i<n; i++)
        if (max_val < v[i])
            max_val = v[i];
    
    int *ord_v = calloc(n, sizeof(int));

    // 'while the algorithm hasnt arrived at the last digit'
    int exp = 1;
    while (max_val / exp > 0) {

        // Counting sort principle
        int bucket[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; // 0 - 9
        for (int i=0; i<n; i++)
            bucket[(v[i] / exp) % 10] ++; // Sum 1 to its occurrence
        
        for (int i=1; i<10; i++)
            bucket[i] += bucket[i-1]; // Adjust last index of ocurrence
        
        for (int i=n-1; i>=0; i--) {
            ord_v[bucket[(v[i] / exp) % 10] - 1] = v[i]; // According to bucket, sort the vector
            bucket[(v[i] / exp) % 10] --; // Adjust for subsequent items
        }
        for (int i=0; i<n; i++)
            v[i] = ord_v[i]; // Copy results to original vector

        exp *= 10; // Next digit
            
    }

    free(ord_v);
}