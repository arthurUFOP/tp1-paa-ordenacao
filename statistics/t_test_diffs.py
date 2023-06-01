import numpy as np
import scipy.stats as st
import os
import csv
import math

methods = ["RadixSort", "MergeSort", "InsertionSort"]
filenames = ["rad_test.csv", "merge_test.csv", "ins_test.csv"]

def read_data(filename):
    n_size, values = [], []
    with open(os.path.join(os.getcwd(), "csvs_2", filename), "r") as f:
        reader = csv.reader(f)
        data = np.array(list(reader))
        n_size = np.array([int(x[0]) for x in data[::20]])
        for i in range(0, 23): # Para insertion sort, eh necessario alterar este 23 por 13
            values.append(np.array(data[20*i : 20*(i+1)][:, 1].astype(np.float64)))
    return n_size, values

# Returns:
# True -> methods show a statistically significant difference (at 95% significance)
# False -> methods do not show a statistically significant difference (at 95% significance)
def t_test_diffs(sample_a, sample_b, name_a, name_b):
    lower_bound, upper_bound = 0, 0
    a_mean = np.mean(sample_a)
    b_mean = np.mean(sample_b)
    a_std = np.std(sample_a) # Desvio padrão = Standard deviation
    b_std = np.std(sample_b)
    a_var = pow(a_std,2)
    b_var = pow(b_std,2)
    n_a = len(sample_a)
    n_b = len(sample_b)

    mean_diffs = a_mean - b_mean
    diffs_std = math.sqrt((a_var/n_a) + 
                          (b_var/n_b))
    v = pow((a_var/n_a)+(b_var/n_b) , 2) / ((1/(n_a+1))*pow(a_var/n_a,2) + (1/(n_b+1))*pow(b_var/n_b,2)) # Grau efetivo de liberdade
    # In case of NaN, there is no significant difference
    try:
        t_student = st.t.ppf(0.95, round(v))
    except:
        print(f"\tMédia do {name_a} = {round(a_mean,4)}\n\tMédia do {name_b} = {round(b_mean,4)}\n\tIntervalo de confiança - ({round(lower_bound, 4)}, {round(upper_bound, 4)})")
        return False

    lower_bound = mean_diffs - (t_student*diffs_std)
    upper_bound = mean_diffs + (t_student*diffs_std)
    
    print(f"\tMédia do {name_a} = {round(a_mean,4)}\n\tMédia do {name_b} = {round(b_mean,4)}\n\tIntervalo de confiança - ({round(lower_bound, 4)}, {round(upper_bound, 4)})")
    zero_in_interval = lower_bound <= 0 <= upper_bound

    return not zero_in_interval

def print_t_test(method_a, method_b, n, is_diff):
    print(f"\tPara n={n}, ", end="")
    if is_diff:
        print(f"existem evidências estatísticas a um nível de 95% de significância que o método {method_a} tem tempo de execução significativamente diferente de {method_b}")
    else:
        print(f"não existem evidências estatísticas a um nível de 95% de significância que o método {method_a} tem tempo de execução significativamente diferente de {method_b}")
    print()

# Array of arrays
size_n_rad, vals_n_rad = read_data(filenames[0])
size_n_mer, vals_n_mer = read_data(filenames[1])
size_n_ins, vals_n_ins = read_data(filenames[2])

for i, n in enumerate(size_n_rad): # Except insertion, all methods have all n's
    print(f"n = {n}")
    print_t_test(methods[0], methods[1], n, t_test_diffs(vals_n_rad[i], vals_n_mer[i], "RadixSort", "MergeSort"))
    if n <= 409600:
        print_t_test(methods[0], methods[2], n, t_test_diffs(vals_n_rad[i], vals_n_ins[i], "RadixSort", "InsertionSort"))
        print_t_test(methods[1], methods[2], n, t_test_diffs(vals_n_mer[i], vals_n_ins[i], "MergeSort", "InsertionSort"))
    print("----------------------------------------------------------------------------------------------------------------")
    
    