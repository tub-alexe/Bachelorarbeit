import matplotlib.pyplot as plt



# importing the module
import json

# reading the data from the file
with open('../Simulation/Vollständige Kreisläufe/Parallelkompression/Senkenaustrittstemperatur.txt') as f:
    read = f.readlines()

data_T190 = json.loads(read[1])
COP_T190 = json.loads(read[2])
eta_T190 = json.loads(read[3])

data_T195 = json.loads(read[5])
COP_T195 = json.loads(read[6])
eta_T195 = json.loads(read[7])

data_T200 = json.loads(read[9])
COP_T200 = json.loads(read[10])
eta_T200 = json.loads(read[11])

data_T205 = json.loads(read[13])
COP_T205 = json.loads(read[14])
eta_T205 = json.loads(read[15])

data_T210 = json.loads(read[17])
COP_T210 = json.loads(read[18])
eta_T210 = json.loads(read[19])

plt.rc('font', **{'size': 18})

plt.plot(data_T190, eta_T190, color='red', label='190°C')
plt.plot(39.3, 71.78, color='black', marker='x', markersize=12)
plt.plot(data_T195, eta_T195, color='orange', label='195°C')
plt.plot(41.5, 72.79, color='black', marker='x', markersize=12)
plt.plot(data_T200, eta_T200, color='green', label='200°C')
plt.plot(44.36, 72.96, color='black', marker='x', markersize=12)
plt.plot(data_T205, eta_T205, color='steelblue', label='205°C')
plt.plot(47.63, 72.92, color='black', marker='x', markersize=12)
plt.plot(data_T210, eta_T210, color='blueviolet', label='210°C')
plt.plot(51.23, 72.81, color='black', marker='x', markersize=12)
plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('exergetischer Wirkungsgrad')
plt.legend(loc='upper right')
plt.grid()
plt.show()