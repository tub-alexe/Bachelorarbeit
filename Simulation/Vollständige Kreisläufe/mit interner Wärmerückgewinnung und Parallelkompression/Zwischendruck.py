import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import json

#Import der Datensätze
with open('Zwischendruck.txt') as f:
    read = f.readlines()

data_zw8 = json.loads(read[3])
eta_zw8 = json.loads(read[4])

data_zw11 = json.loads(read[6])
eta_zw11 = json.loads(read[7])

data_zw15 = json.loads(read[9])
eta_zw15 = json.loads(read[10])

data_zw19 = json.loads(read[12])
eta_zw19 = json.loads(read[13])

data_ttd_u_5 = json.loads(read[16])
eta_ttd_u_5 = json.loads(read[17])

data_ttd_u_10 = json.loads(read[19])
eta_ttd_u_10 = json.loads(read[20])

data_ttd_u_15 = json.loads(read[22])
eta_ttd_u_15 = json.loads(read[23])

data_ttd_u_20 = json.loads(read[25])
eta_ttd_u_20 = json.loads(read[26])

#Erstellung der Grafiken mit Kennzeichnung von Datenpunkten
plt.rc('font', **{'size': 20})
plt.rcParams["figure.figsize"] = (20, 12)

plt.plot(data_zw8, eta_zw8, color='black')
plt.annotate('8', xy=(30.5, 66.01), xytext=(30.5, 66.01))
plt.plot(data_zw11, eta_zw11, color='black')
plt.annotate('11', xy=(30.8, 69.79), xytext=(30.8, 69.79))
plt.plot(data_zw15, eta_zw15, color='black')
plt.annotate('15', xy=(30.4, 72.59), xytext=(30.4, 72.59))
plt.plot(data_zw19, eta_zw19, color='black')
plt.annotate('18,17', xy=(30.1, 73.52), xytext=(30.1, 73.52))

plt.plot(data_ttd_u_5, eta_ttd_u_5, linestyle='--', color='red')
plt.plot(data_ttd_u_10, eta_ttd_u_10, linestyle='--', color='orange')
plt.plot(data_ttd_u_15, eta_ttd_u_15, linestyle='--', color='green')
plt.plot(data_ttd_u_20, eta_ttd_u_20, linestyle='--', color='steelblue')

plt.plot(data_ttd_u_5[0], eta_ttd_u_5[0], color='black', marker='x', markersize=12)
plt.annotate('8', xy=(33.9, 66.09), xytext=(33.9, 66.09))
plt.plot(34.27, 69.40, color='black', marker='x', markersize=12)
plt.annotate('11', xy=(33.85, 69.15), xytext=(33.85, 69.15))
plt.plot(33.68, 71.90, color='black', marker='x', markersize=12)
plt.annotate('15', xy=(33.25, 71.65), xytext=(33.25, 71.65))
plt.plot(32.78, 72.59, color='black', marker='x', markersize=12)
plt.annotate('18,17', xy=(32.74, 72.7), xytext=(32.74, 72.7))

plt.plot(data_ttd_u_10[0], eta_ttd_u_10[0], color='black', marker='x', markersize=12)
plt.annotate('8', xy=(37.3, 65.71), xytext=(37.3, 65.71))
plt.plot(37.59, 68.79, color='black', marker='x', markersize=12)
plt.annotate('11', xy=(37.1, 68.59), xytext=(37.1, 68.59))
plt.plot(36.82, 71.05, color='black', marker='x', markersize=12)
plt.annotate('15', xy=(36.4, 70.80), xytext=(36.4, 70.80))
plt.plot(35.69, 71.65, color='black', marker='x', markersize=12)
plt.annotate('18,17', xy=(35.65, 71.77), xytext=(35.65, 71.77))

plt.plot(data_ttd_u_15[0], eta_ttd_u_15[0], color='black', marker='x', markersize=12)
plt.annotate('8', xy=(41.08, 65.3), xytext=(41.08, 65.3))
plt.plot(41.24, 68.15, color='black', marker='x', markersize=12)
plt.annotate('11', xy=(40.85, 67.9), xytext=(40.85, 67.9))
plt.plot(40.27, 70.24, color='black', marker='x', markersize=12)
plt.annotate('15', xy=(39.80, 69.99), xytext=(39.80, 69.99))
plt.plot(38.90, 70.75, color='black', marker='x', markersize=12)
plt.annotate('18,17', xy=(38.87, 70.87), xytext=(38.87, 70.87))

plt.plot(44.14, 69.45, color='black', marker='x', markersize=12)
plt.annotate('15', xy=(43.74, 69.2), xytext=(43.74, 69.2))
plt.plot(42.47, 69.91, color='black', marker='x', markersize=12)
plt.annotate('18,17', xy=(42.44, 70.03), xytext=(42.44, 70.03))

plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
plt.xlim(30, 45)

o_line = mlines.Line2D([], [], color='black', label=r'$p_{zw}$ [bar]          $ΔT_{GK,ob}$:')
s_line = mlines.Line2D([], [], color='black',  linestyle='--', label='ttd_gk,ob:')
red_line = mlines.Line2D([], [], color='red', linestyle='--', label='5 K')
yellow_line = mlines.Line2D([], [], color='orange', linestyle='--', label='10 K')
green_line = mlines.Line2D([], [], color='green', linestyle='--', label='15 K')
blue_line = mlines.Line2D([], [], color='steelblue', linestyle='--', label='20 K')
black_line = mlines.Line2D([], [], color='blueviolet', linestyle='--', label='15 K')

plt.legend(handles=[o_line, red_line, yellow_line, green_line, blue_line], loc='lower center', ncol=7)
plt.grid()
plt.savefig('Zwischendruck Parallel R1336mzz(Z).svg')
plt.show()