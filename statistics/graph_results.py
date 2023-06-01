from matplotlib import pyplot as plt
import numpy as np
import scipy.stats as st
import csv
import os

method = "RadixSort"
filename = "rad_test.csv"

n_size, mean, l_bound, u_bound = [], [], [], []
with open(os.path.join(os.getcwd(), "csvs_2", filename), "r") as f:
    reader = csv.reader(f)
    data = np.array(list(reader))
    n_size = np.array([int(x[0]) for x in data[::20]])
    for i in range(0, 23): # Para insertion sort, eh necessario alterar este 23 por 13
        values = np.array(data[20*i : 20*(i+1)][:, 1].astype(np.float64))

        m = np.mean(values)
        mean.append(m)

        l_b, u_b = st.t.interval(
            confidence=0.95,
            df = len(values),
            loc = m,
            scale = st.sem(values)
        )
        l_bound.append(l_b)
        u_bound.append(u_b)
        
    mean = np.array(mean)
    l_bound = np.array(l_bound)
    u_bound = np.array(u_bound)
    
fig, ax = plt.subplots()

ax.plot(n_size, mean, "ob")
ax.plot((n_size, n_size), (l_bound, u_bound))
ax.set(xlabel='Tamanho da instância',
       ylabel='Média de tempo (segundos)',
       title=f'Média de tempo gasto pelo {method}')
plt.show()