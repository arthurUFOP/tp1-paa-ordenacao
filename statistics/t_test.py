import numpy as np
import scipy.stats as st
import os
import csv

methods = ["InsertionSort", "MergeSort", "RadixSort"]
filenames = ["ins_test.csv", "merge_test.csv", "rad_test.csv"]

def read_data(filename):
    n_size, values = [], []
    with open(os.path.join(os.getcwd(), "csvs_2", filename), "r") as f:
        reader = csv.reader(f)
        data = np.array(list(reader))
        n_size = np.array([int(x[0]) for x in data[::20]])
        for i in range(0, 23): # Para insertion sort, eh necessario alterar este 23 por 13
            values.append(np.array(data[20*i : 20*(i+1)][:, 1].astype(np.float64)))
    return n_size, values

# Solo array
# 0 -> a_mean < b_mean
# 1 -> a_mean = b_mean
def t_test(a_vals, a_name, b_vals, b_name):
    #‘less’: 
    # the mean of the distribution underlying the first sample 
    # is less than the mean of the distribution underlying the second sample.
    hip = st.ttest_ind(a_vals, b_vals, equal_var=False, alternative='less')
    # Ho -> a_mean = b_mean
    # Ha -> a_mean < b_mean

    reject_hip_value = st.t.ppf(q=0.05, df=19) # T-student for less than

    ho = f"Ho: media de tempo do {a_name} = media de tempo do {b_name}"
    ha = f"Ha: media de tempo do {a_name} < media de tempo do {b_name}"

    print(ho)
    print(ha)

    print("Valor t calculado: ", hip[0])
    print("Valor t para 95%: ", reject_hip_value)

    reject = hip[0] < reject_hip_value

    print(f"Resultado: Hipotese Ho {'rejeitada' if reject else 'aceita'}")
    if reject:
        print(ha, "\n")
        return 0
    else:
        print(ho, "\n")
        return 1

# Array of arrays
size_n_ins, vals_n_ins = read_data(filenames[0])
size_n_mer, vals_n_mer = read_data(filenames[1])
size_n_rad, vals_n_rad = read_data(filenames[2])

t_test(vals_n_rad[-1], "Radix", vals_n_ins[-1], "Insertion")
t_test(vals_n_rad[-1], "Radix", vals_n_mer[-1], "MergeSort")
t_test(vals_n_mer[-1], "MergeSort", vals_n_ins[-1], "Insertion")

# n_sizes are equal to each one
for i, n in enumerate(size_n_ins):
    print(f"====================================\nTeste com n={n}\n\n")
    t_test(vals_n_rad[i], "Radix", vals_n_ins[i], "Insertion")
    t_test(vals_n_rad[i], "Radix", vals_n_mer[i], "MergeSort")
    t_test(vals_n_mer[i], "MergeSort", vals_n_ins[i], "Insertion")
    print("====================================\n")

            
            
        