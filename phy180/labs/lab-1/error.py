# import numpy as np
# mu, sigma = 4.6, 0.1 # mean and standard deviation
# s = np.random.normal(mu,sigma,10000000)
# s = [round(number * 2) / 2 for number in s]

# print(sum(s)/len(s))

import numpy as np
import matplotlib.pyplot as plt
sum_list = []
j_list = []
for j in range(2,5):
    s = []
    for i in range(10**j):
        t_actual_1 = np.random.random()
        t_actual_2 = np.random.random()
        s.append(t_actual_2-t_actual_1)
    sum_list.append(sum(s)/len(s))
    j_list.append(j)
print(sum_list)

plt.plot(j_list, sum_list)