import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# importing the module
import json

with open('Einfacher Kreislauf mit IHX\Senkenaustrittstemperatur.txt') as f:
    read = f.readlines()

data_T190_IHX_R1233ZDE = json.loads(read[1])
COP_T190_IHX_R1233ZDE = json.loads(read[2])
eta_T190_IHX_R1233ZDE = json.loads(read[3])

data_T195_IHX_R1233ZDE = json.loads(read[5])
COP_T195_IHX_R1233ZDE = json.loads(read[6])
eta_T195_IHX_R1233ZDE = json.loads(read[7])

data_T200_IHX_R1233ZDE = json.loads(read[9])
COP_T200_IHX_R1233ZDE = json.loads(read[10])
eta_T200_IHX_R1233ZDE = json.loads(read[11])

data_T205_IHX_R1233ZDE = json.loads(read[13])
COP_T205_IHX_R1233ZDE = json.loads(read[14])
eta_T205_IHX_R1233ZDE = json.loads(read[15])

data_T210_IHX_R1233ZDE = json.loads(read[17])
COP_T210_IHX_R1233ZDE = json.loads(read[18])
eta_T210_IHX_R1233ZDE = json.loads(read[19])

data_T215_IHX_R1233ZDE = json.loads(read[21])
COP_T215_IHX_R1233ZDE = json.loads(read[22])
eta_T215_IHX_R1233ZDE = json.loads(read[23])

data_T220_IHX_R1233ZDE = json.loads(read[25])
COP_T220_IHX_R1233ZDE = json.loads(read[26])
eta_T220_IHX_R1233ZDE = json.loads(read[27])

data_T190_IHX_R601 = json.loads(read[29])
COP_T190_IHX_R601 = json.loads(read[30])
eta_T190_IHX_R601 = json.loads(read[31])

data_T195_IHX_R601 = json.loads(read[33])
COP_T195_IHX_R601 = json.loads(read[34])
eta_T195_IHX_R601 = json.loads(read[35])

data_T200_IHX_R601 = json.loads(read[37])
COP_T200_IHX_R601 = json.loads(read[38])
eta_T200_IHX_R601 = json.loads(read[39])

data_T205_IHX_R601 = json.loads(read[41])
COP_T205_IHX_R601 = json.loads(read[42])
eta_T205_IHX_R601 = json.loads(read[43])

data_T210_IHX_R601 = json.loads(read[45])
COP_T210_IHX_R601 = json.loads(read[46])
eta_T210_IHX_R601 = json.loads(read[47])

data_T215_IHX_R601 = json.loads(read[49])
COP_T215_IHX_R601 = json.loads(read[50])
eta_T215_IHX_R601 = json.loads(read[51])

data_T220_IHX_R601 = json.loads(read[53])
COP_T220_IHX_R601 = json.loads(read[54])
eta_T220_IHX_R601 = json.loads(read[55])

with open('Parallelkompression\Senkenaustrittstemperatur.txt') as f:
    read = f.readlines()

data_T190_Parallel_R1233ZDE = json.loads(read[1])
COP_T190_Parallel_R1233ZDE = json.loads(read[2])
eta_T190_Parallel_R1233ZDE = json.loads(read[3])

data_T195_Parallel_R1233ZDE = json.loads(read[5])
COP_T195_Parallel_R1233ZDE = json.loads(read[6])
eta_T195_Parallel_R1233ZDE = json.loads(read[7])

data_T200_Parallel_R1233ZDE = json.loads(read[9])
COP_T200_Parallel_R1233ZDE = json.loads(read[10])
eta_T200_Parallel_R1233ZDE = json.loads(read[11])

data_T205_Parallel_R1233ZDE = json.loads(read[13])
COP_T205_Parallel_R1233ZDE = json.loads(read[14])
eta_T205_Parallel_R1233ZDE = json.loads(read[15])

data_T210_Parallel_R1233ZDE = json.loads(read[17])
COP_T210_Parallel_R1233ZDE = json.loads(read[18])
eta_T210_Parallel_R1233ZDE = json.loads(read[19])

data_T215_Parallel_R1233ZDE = json.loads(read[21])
COP_T215_Parallel_R1233ZDE = json.loads(read[22])
eta_T215_Parallel_R1233ZDE = json.loads(read[23])

data_T220_Parallel_R1233ZDE = json.loads(read[25])
COP_T220_Parallel_R1233ZDE = json.loads(read[26])
eta_T220_Parallel_R1233ZDE = json.loads(read[27])

data_T190_Parallel_R601 = json.loads(read[29])
COP_T190_Parallel_R601 = json.loads(read[30])
eta_T190_Parallel_R601 = json.loads(read[31])

data_T195_Parallel_R601 = json.loads(read[33])
COP_T195_Parallel_R601 = json.loads(read[34])
eta_T195_Parallel_R601 = json.loads(read[35])

data_T200_Parallel_R601 = json.loads(read[37])
COP_T200_Parallel_R601 = json.loads(read[38])
eta_T200_Parallel_R601 = json.loads(read[39])

data_T205_Parallel_R601 = json.loads(read[41])
COP_T205_Parallel_R601 = json.loads(read[42])
eta_T205_Parallel_R601 = json.loads(read[43])

data_T210_Parallel_R601 = json.loads(read[45])
COP_T210_Parallel_R601 = json.loads(read[46])
eta_T210_Parallel_R601 = json.loads(read[47])

data_T215_Parallel_R601 = json.loads(read[49])
COP_T215_Parallel_R601 = json.loads(read[50])
eta_T215_Parallel_R601 = json.loads(read[51])

data_T220_Parallel_R601 = json.loads(read[53])
COP_T220_Parallel_R601 = json.loads(read[54])
eta_T220_Parallel_R601 = json.loads(read[55])

plt.rc('font', **{'size': 18})

plt.plot(data_T190_IHX_R1233ZDE, eta_T190_IHX_R1233ZDE, color='red', label='190°C')
plt.plot(data_T195_IHX_R1233ZDE, eta_T195_IHX_R1233ZDE, color='orange', label='195°C')
plt.plot(data_T200_IHX_R1233ZDE, eta_T200_IHX_R1233ZDE, color='green', label='200°C')
plt.plot(data_T205_IHX_R1233ZDE, eta_T205_IHX_R1233ZDE, color='steelblue', label='205°C')
plt.plot(data_T210_IHX_R1233ZDE, eta_T210_IHX_R1233ZDE, color='blueviolet', label='210°C')
plt.plot(data_T215_IHX_R1233ZDE, eta_T215_IHX_R1233ZDE, color='black', label='215°C')
plt.plot(data_T220_IHX_R1233ZDE, eta_T220_IHX_R1233ZDE, color='grey', label='220°C')
plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('exergetischer Wirkungsgrad')
plt.legend(loc='lower right')
plt.grid()
plt.show()

plt.plot(data_T190_Parallel_R1233ZDE, eta_T190_Parallel_R1233ZDE, color='red', label='190°C')
plt.plot(39.3, 71.78, color='black', marker='x', markersize=12)
plt.plot(data_T195_Parallel_R1233ZDE, eta_T195_Parallel_R1233ZDE, color='orange', label='195°C')
plt.plot(41.5, 72.79, color='black', marker='x', markersize=12)
plt.plot(data_T200_Parallel_R1233ZDE, eta_T200_Parallel_R1233ZDE, color='green', label='200°C')
plt.plot(44.36, 72.96, color='black', marker='x', markersize=12)
plt.plot(data_T205_Parallel_R1233ZDE, eta_T205_Parallel_R1233ZDE, color='steelblue', label='205°C')
plt.plot(47.63, 72.92, color='black', marker='x', markersize=12)
plt.plot(data_T210_Parallel_R1233ZDE, eta_T210_Parallel_R1233ZDE, color='blueviolet', label='210°C')
plt.plot(51.23, 72.81, color='black', marker='x', markersize=12)
plt.plot(data_T215_Parallel_R1233ZDE, eta_T215_Parallel_R1233ZDE, color='black', label='215°C')
plt.plot(55.19, 72.69, color='black', marker='x', markersize=12)
plt.plot(data_T220_Parallel_R1233ZDE, eta_T220_Parallel_R1233ZDE, color='grey', label='220°C')
plt.plot(59.53, 72.56, color='black', marker='x', markersize=12)
plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('exergetischer Wirkungsgrad')
plt.legend(loc='lower left', fontsize='16')
plt.grid()
plt.show()

plt.plot(data_T190_IHX_R601, eta_T190_IHX_R601, color='red', label='190°C')
plt.plot(data_T195_IHX_R601, eta_T195_IHX_R601, color='orange', label='195°C')
plt.plot(data_T200_IHX_R601, eta_T200_IHX_R601, color='green', label='200°C')
plt.plot(data_T205_IHX_R601, eta_T205_IHX_R601, color='steelblue', label='205°C')
plt.plot(data_T210_IHX_R601, eta_T210_IHX_R601, color='blueviolet', label='210°C')
plt.plot(data_T215_IHX_R601, eta_T215_IHX_R601, color='black', label='215°C')
plt.plot(data_T220_IHX_R601, eta_T220_IHX_R601, color='grey', label='220°C')
plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('exergetischer Wirkungsgrad')
plt.legend(loc='lower right')
plt.grid()
plt.show()

plt.plot(data_T190_Parallel_R601, eta_T190_Parallel_R601, color='red', label='190°C')
plt.plot(data_T195_Parallel_R601, eta_T195_Parallel_R601, color='orange', label='195°C')
plt.plot(29.67, 74.89, color='black', marker='x', markersize=12)
plt.plot(data_T200_Parallel_R601, eta_T200_Parallel_R601, color='green', label='200°C')
plt.plot(32.29, 74.58, color='black', marker='x', markersize=12)
plt.plot(data_T205_Parallel_R601, eta_T205_Parallel_R601, color='steelblue', label='205°C')
plt.plot(35.01, 74.42, color='black', marker='x', markersize=12)
plt.plot(data_T210_Parallel_R601, eta_T210_Parallel_R601, color='blueviolet', label='210°C')
plt.plot(37.86, 74.35, color='black', marker='x', markersize=12)
plt.plot(data_T215_Parallel_R601, eta_T215_Parallel_R601, color='black', label='215°C')
plt.plot(40.92, 74.34, color='black', marker='x', markersize=12)
plt.plot(data_T220_Parallel_R601, eta_T220_Parallel_R601, color='grey', label='220°C')
plt.plot(44.28, 74.36, color='black', marker='x', markersize=12)
plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('exergetischer Wirkungsgrad')
plt.legend(loc='lower left', fontsize='16')
plt.grid()
plt.show()