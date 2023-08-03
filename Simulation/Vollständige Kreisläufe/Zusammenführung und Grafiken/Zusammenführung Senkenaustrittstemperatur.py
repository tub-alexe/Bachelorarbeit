import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np

# importing the module
import json

with open('../Einfacher Kreislauf mit IHX/Senkenaustrittstemperatur.txt') as f:
    read = f.readlines()

data_T190_IHX_R1233ZDE = json.loads(read[5])
eta_T190_IHX_R1233ZDE = json.loads(read[6])

data_T195_IHX_R1233ZDE = json.loads(read[9])
eta_T195_IHX_R1233ZDE = json.loads(read[10])

data_T200_IHX_R1233ZDE = json.loads(read[13])
eta_T200_IHX_R1233ZDE = json.loads(read[14])

data_T205_IHX_R1233ZDE = json.loads(read[17])
eta_T205_IHX_R1233ZDE = json.loads(read[18])

data_T210_IHX_R1233ZDE = json.loads(read[21])
eta_T210_IHX_R1233ZDE = json.loads(read[22])

data_T215_IHX_R1233ZDE = json.loads(read[25])
eta_T215_IHX_R1233ZDE = json.loads(read[26])

data_T220_IHX_R1233ZDE = json.loads(read[29])
eta_T220_IHX_R1233ZDE = json.loads(read[30])

data_ttd_u_15_IHX_R1233ZDE = json.loads(read[35])
eta_ttd_u_15_IHX_R1233ZDE = json.loads(read[36])

data_ttd_u_20_IHX_R1233ZDE = json.loads(read[40])
eta_ttd_u_20_IHX_R1233ZDE = json.loads(read[41])

data_ttd_u_30_IHX_R1233ZDE = json.loads(read[45])
eta_ttd_u_30_IHX_R1233ZDE = json.loads(read[46])

data_ttd_u_40_IHX_R1233ZDE = json.loads(read[50])
eta_ttd_u_40_IHX_R1233ZDE = json.loads(read[51])

data_T190_IHX_R600 = json.loads(read[57])
eta_T190_IHX_R600 = json.loads(read[58])

data_T195_IHX_R600 = json.loads(read[61])
eta_T195_IHX_R600 = json.loads(read[62])

data_T200_IHX_R600 = json.loads(read[65])
eta_T200_IHX_R600 = json.loads(read[66])

data_T205_IHX_R600 = json.loads(read[69])
eta_T205_IHX_R600 = json.loads(read[70])

data_T210_IHX_R600 = json.loads(read[73])
eta_T210_IHX_R600 = json.loads(read[74])

data_T215_IHX_R600 = json.loads(read[77])
eta_T215_IHX_R600 = json.loads(read[78])

data_T220_IHX_R600 = json.loads(read[81])
eta_T220_IHX_R600 = json.loads(read[82])

data_ttd_u_10_IHX_R600 = json.loads(read[87])
eta_ttd_u_10_IHX_R600 = json.loads(read[88])

data_ttd_u_15_IHX_R600 = json.loads(read[92])
eta_ttd_u_15_IHX_R600 = json.loads(read[93])

data_ttd_u_20_IHX_R600 = json.loads(read[97])
eta_ttd_u_20_IHX_R600 = json.loads(read[98])

data_ttd_u_30_IHX_R600 = json.loads(read[102])
eta_ttd_u_30_IHX_R600 = json.loads(read[103])

data_T190_IHX_R1336MZZZ = json.loads(read[109])
eta_T190_IHX_R1336MZZZ = json.loads(read[110])

data_T195_IHX_R1336MZZZ = json.loads(read[113])
eta_T195_IHX_R1336MZZZ = json.loads(read[114])

data_T200_IHX_R1336MZZZ = json.loads(read[117])
eta_T200_IHX_R1336MZZZ = json.loads(read[118])

data_T205_IHX_R1336MZZZ = json.loads(read[121])
eta_T205_IHX_R1336MZZZ = json.loads(read[122])

data_T210_IHX_R1336MZZZ = json.loads(read[125])
eta_T210_IHX_R1336MZZZ = json.loads(read[126])

data_T215_IHX_R1336MZZZ = json.loads(read[129])
eta_T215_IHX_R1336MZZZ = json.loads(read[130])

data_T220_IHX_R1336MZZZ = json.loads(read[133])
eta_T220_IHX_R1336MZZZ= json.loads(read[134])

data_ttd_u_10_IHX_R1336MZZZ = json.loads(read[139])
eta_ttd_u_10_IHX_R1336MZZZ = json.loads(read[140])

data_ttd_u_15_IHX_R1336MZZZ = json.loads(read[144])
eta_ttd_u_15_IHX_R1336MZZZ = json.loads(read[145])

data_ttd_u_20_IHX_R1336MZZZ = json.loads(read[149])
eta_ttd_u_20_IHX_R1336MZZZ= json.loads(read[150])

data_ttd_u_30_IHX_R1336MZZZ = json.loads(read[154])
eta_ttd_u_30_IHX_R1336MZZZ = json.loads(read[155])

data_T190_IHX_R601 = json.loads(read[161])
eta_T190_IHX_R601 = json.loads(read[162])

data_T195_IHX_R601 = json.loads(read[165])
eta_T195_IHX_R601 = json.loads(read[166])

data_T200_IHX_R601 = json.loads(read[169])
eta_T200_IHX_R601 = json.loads(read[170])

data_T205_IHX_R601 = json.loads(read[173])
eta_T205_IHX_R601 = json.loads(read[174])

data_T210_IHX_R601 = json.loads(read[177])
eta_T210_IHX_R601 = json.loads(read[178])

data_T215_IHX_R601 = json.loads(read[181])
eta_T215_IHX_R601 = json.loads(read[182])

data_T220_IHX_R601 = json.loads(read[185])
eta_T220_IHX_R601 = json.loads(read[186])

data_ttd_u_10_IHX_R601 = json.loads(read[191])
eta_ttd_u_10_IHX_R601 = json.loads(read[192])

data_ttd_u_15_IHX_R601 = json.loads(read[196])
eta_ttd_u_15_IHX_R601 = json.loads(read[197])

data_ttd_u_20_IHX_R601 = json.loads(read[201])
eta_ttd_u_20_IHX_R601 = json.loads(read[202])

data_ttd_u_30_IHX_R601 = json.loads(read[206])
eta_ttd_u_30_IHX_R601 = json.loads(read[207])

with open('../Parallelkompression/Senkenaustrittstemperatur.txt') as f:
    read = f.readlines()

data_T190_Parallel_R1233ZDE = json.loads(read[5])
eta_T190_Parallel_R1233ZDE = json.loads(read[6])

data_T195_Parallel_R1233ZDE = json.loads(read[9])
eta_T195_Parallel_R1233ZDE = json.loads(read[10])

data_T200_Parallel_R1233ZDE = json.loads(read[13])
eta_T200_Parallel_R1233ZDE = json.loads(read[14])

data_T205_Parallel_R1233ZDE = json.loads(read[17])
eta_T205_Parallel_R1233ZDE = json.loads(read[18])

data_T210_Parallel_R1233ZDE = json.loads(read[21])
eta_T210_Parallel_R1233ZDE = json.loads(read[22])

data_T215_Parallel_R1233ZDE = json.loads(read[25])
eta_T215_Parallel_R1233ZDE = json.loads(read[26])

data_T220_Parallel_R1233ZDE = json.loads(read[29])
eta_T220_Parallel_R1233ZDE = json.loads(read[30])

data_ttd_u_5_Parallel_R1233ZDE = json.loads(read[35])
eta_ttd_u_5_Parallel_R1233ZDE = json.loads(read[36])

data_ttd_u_10_Parallel_R1233ZDE = json.loads(read[41])
eta_ttd_u_10_Parallel_R1233ZDE = json.loads(read[42])

data_ttd_u_15_Parallel_R1233ZDE = json.loads(read[47])
eta_ttd_u_15_Parallel_R1233ZDE = json.loads(read[48])

data_ttd_u_20_Parallel_R1233ZDE = json.loads(read[53])
eta_ttd_u_20_Parallel_R1233ZDE = json.loads(read[54])

data_T190_Parallel_R600 = json.loads(read[61])
eta_T190_Parallel_R600 = json.loads(read[62])

data_T195_Parallel_R600 = json.loads(read[65])
eta_T195_Parallel_R600 = json.loads(read[66])

data_T200_Parallel_R600 = json.loads(read[69])
eta_T200_Parallel_R600 = json.loads(read[70])

data_T205_Parallel_R600 = json.loads(read[73])
eta_T205_Parallel_R600 = json.loads(read[74])

data_T210_Parallel_R600 = json.loads(read[77])
eta_T210_Parallel_R600 = json.loads(read[78])

data_ttd_u_5_Parallel_R600 = json.loads(read[83])
eta_ttd_u_5_Parallel_R600 = json.loads(read[84])

data_ttd_u_10_Parallel_R600 = json.loads(read[89])
eta_ttd_u_10_Parallel_R600 = json.loads(read[90])

data_ttd_u_15_Parallel_R600 = json.loads(read[95])
eta_ttd_u_15_Parallel_R600 = json.loads(read[96])

data_ttd_u_20_Parallel_R600 = json.loads(read[101])
eta_ttd_u_20_Parallel_R600 = json.loads(read[102])

data_T190_Parallel_R1336MZZZ = json.loads(read[109])
eta_T190_Parallel_R1336MZZZ = json.loads(read[110])

data_T195_Parallel_R1336MZZZ = json.loads(read[113])
eta_T195_Parallel_R1336MZZZ = json.loads(read[114])

data_T200_Parallel_R1336MZZZ = json.loads(read[117])
eta_T200_Parallel_R1336MZZZ = json.loads(read[118])

data_T205_Parallel_R1336MZZZ = json.loads(read[121])
eta_T205_Parallel_R1336MZZZ = json.loads(read[122])

data_T210_Parallel_R1336MZZZ = json.loads(read[125])
eta_T210_Parallel_R1336MZZZ = json.loads(read[126])

data_T215_Parallel_R1336MZZZ = json.loads(read[129])
eta_T215_Parallel_R1336MZZZ = json.loads(read[130])

data_ttd_u_5_Parallel_R1336MZZZ = json.loads(read[135])
eta_ttd_u_5_Parallel_R1336MZZZ = json.loads(read[136])

data_ttd_u_10_Parallel_R1336MZZZ = json.loads(read[141])
eta_ttd_u_10_Parallel_R1336MZZZ = json.loads(read[142])

data_ttd_u_15_Parallel_R1336MZZZ = json.loads(read[147])
eta_ttd_u_15_Parallel_R1336MZZZ = json.loads(read[148])

data_ttd_u_20_Parallel_R1336MZZZ = json.loads(read[153])
eta_ttd_u_20_Parallel_R1336MZZZ = json.loads(read[154])

data_T190_Parallel_R601 = json.loads(read[161])
eta_T190_Parallel_R601 = json.loads(read[162])

data_T195_Parallel_R601 = json.loads(read[165])
eta_T195_Parallel_R601 = json.loads(read[166])

data_T200_Parallel_R601 = json.loads(read[169])
eta_T200_Parallel_R601 = json.loads(read[170])

data_T205_Parallel_R601 = json.loads(read[173])
eta_T205_Parallel_R601 = json.loads(read[174])

data_T210_Parallel_R601 = json.loads(read[177])
eta_T210_Parallel_R601 = json.loads(read[178])

data_T215_Parallel_R601 = json.loads(read[181])
eta_T215_Parallel_R601 = json.loads(read[182])

data_T220_Parallel_R601 = json.loads(read[185])
eta_T220_Parallel_R601 = json.loads(read[186])

data_ttd_u_5_Parallel_R601 = json.loads(read[191])
eta_ttd_u_5_Parallel_R601 = json.loads(read[192])

data_ttd_u_10_Parallel_R601 = json.loads(read[197])
eta_ttd_u_10_Parallel_R601 = json.loads(read[198])

data_ttd_u_15_Parallel_R601 = json.loads(read[203])
eta_ttd_u_15_Parallel_R601 = json.loads(read[204])

data_ttd_u_20_Parallel_R601 = json.loads(read[209])
eta_ttd_u_20_Parallel_R601 = json.loads(read[210])


plt.rc('font', **{'size': 20})
plt.rcParams["figure.figsize"] = (20, 13)

plt.plot(data_T190_IHX_R1233ZDE, eta_T190_IHX_R1233ZDE, color='black', label='190°C')
plt.annotate('190', xy=(58.1, 66.3), xytext=(58.1, 66.3))
plt.plot(data_T195_IHX_R1233ZDE, eta_T195_IHX_R1233ZDE, color='black', label='195°C')
plt.annotate('195', xy=(58.1, 67), xytext=(58.1, 67))
plt.plot(data_T200_IHX_R1233ZDE, eta_T200_IHX_R1233ZDE, color='black', label='200°C')
plt.annotate('200', xy=(58.1, 67.7), xytext=(58.1, 67.7))
plt.plot(data_T205_IHX_R1233ZDE, eta_T205_IHX_R1233ZDE, color='black', label='205°C')
plt.annotate('205', xy=(58.1, 68.4), xytext=(58.1, 68.4))
plt.plot(data_T210_IHX_R1233ZDE, eta_T210_IHX_R1233ZDE, color='black', label='210°C')
plt.annotate('210', xy=(58.1, 69.1), xytext=(58.1, 69.1))
plt.plot(data_T215_IHX_R1233ZDE, eta_T215_IHX_R1233ZDE, color='black', label='215°C')
plt.annotate('215', xy=(58.1, 69.8), xytext=(58.1, 69.8))
plt.plot(data_T220_IHX_R1233ZDE, eta_T220_IHX_R1233ZDE, color='black', label='220°C')
plt.annotate('220', xy=(58.1, 70.5), xytext=(58.1, 70.5))
plt.plot(data_ttd_u_15_IHX_R1233ZDE, eta_ttd_u_15_IHX_R1233ZDE, linestyle='--', color='red', label='15°C')
plt.plot(data_ttd_u_20_IHX_R1233ZDE, eta_ttd_u_20_IHX_R1233ZDE, linestyle='--', color='orange', label='20°C')
plt.plot(data_ttd_u_30_IHX_R1233ZDE, eta_ttd_u_30_IHX_R1233ZDE, linestyle='--', color='green', label='30°C')
plt.plot(data_ttd_u_40_IHX_R1233ZDE, eta_ttd_u_40_IHX_R1233ZDE, linestyle='--', color='steelblue', label='40°C')
plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
o_line = mlines.Line2D([], [], color='black', label=r'$T_{se,ein}$ [C]          $ΔT_{gk,ob}$:')
s_line = mlines.Line2D([], [], color='black',  linestyle='--', label='ttd_gk,ob:')
red_line = mlines.Line2D([], [], color='red', linestyle='--', label='15 K')
yellow_line = mlines.Line2D([], [], color='orange', linestyle='--', label='20 K')
green_line = mlines.Line2D([], [], color='green', linestyle='--', label='30 K')
blue_line = mlines.Line2D([], [], color='steelblue', linestyle='--', label='40 K')
plt.ylim(59, 72)
plt.xlim(37.5, 59)
plt.legend(handles=[o_line, red_line, yellow_line, green_line, blue_line], loc='lower center', ncol=7)
plt.grid()
plt.savefig('Senkenaustrittstemperatur IWUE R1233ZD(E).svg')
plt.show()

plt.plot(data_T190_Parallel_R1233ZDE, eta_T190_Parallel_R1233ZDE, color='black', label='190')
plt.annotate('190', xy=(37.9, 68.7), xytext=(37.9, 68.7))
#plt.plot(39.3, 71.78, color='black', marker='x', markersize=12)
plt.plot(data_T195_Parallel_R1233ZDE, eta_T195_Parallel_R1233ZDE, color='black', label='195')
plt.annotate('195', xy=(38.65, 72.67), xytext=(38.65, 72.67))
#plt.plot(41.5, 72.79, color='black', marker='x', markersize=12)
plt.plot(data_T200_Parallel_R1233ZDE, eta_T200_Parallel_R1233ZDE, color='black', label='200')
plt.annotate('200', xy=(40.75, 73.5), xytext=(40.75, 73.5))
#plt.plot(44.36, 72.96, color='black', marker='x', markersize=12)
plt.plot(data_T205_Parallel_R1233ZDE, eta_T205_Parallel_R1233ZDE, color='black', label='205')
plt.annotate('205', xy=(43.8, 73.66), xytext=(43.8, 73.66))
#plt.plot(47.63, 72.92, color='black', marker='x', markersize=12)
plt.plot(data_T210_Parallel_R1233ZDE, eta_T210_Parallel_R1233ZDE, color='black', label='210')
plt.annotate('210', xy=(47.3, 73.55), xytext=(47.3, 73.55))
#plt.plot(51.23, 72.81, color='black', marker='x', markersize=12)
plt.plot(data_T215_Parallel_R1233ZDE, eta_T215_Parallel_R1233ZDE, color='black', label='215')
plt.annotate('215', xy=(51.2, 73.4), xytext=(51.2, 73.4))
#plt.plot(55.19, 72.69, color='black', marker='x', markersize=12)
plt.plot(data_T220_Parallel_R1233ZDE, eta_T220_Parallel_R1233ZDE, color='black', label='220')
plt.annotate('220', xy=(55.55, 73.25), xytext=(55.55, 73.25))
#plt.plot(59.53, 72.56, color='black', marker='x', markersize=12)

plt.plot(data_ttd_u_5_Parallel_R1233ZDE, eta_ttd_u_5_Parallel_R1233ZDE, linestyle='--', color='red', label='5 K')
plt.plot(data_ttd_u_10_Parallel_R1233ZDE, eta_ttd_u_10_Parallel_R1233ZDE, linestyle='--', color='orange', label='10 K')
plt.plot(data_ttd_u_15_Parallel_R1233ZDE, eta_ttd_u_15_Parallel_R1233ZDE, linestyle='--', color='green', label='15 K')
plt.plot(data_ttd_u_20_Parallel_R1233ZDE, eta_ttd_u_20_Parallel_R1233ZDE, linestyle='--', color='steelblue', label='20 K')
plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
o_line = mlines.Line2D([], [], color='black', label=r'$T_{se,ein}$ [C]          $ΔT_{gk,ob}$:')
s_line = mlines.Line2D([], [], color='black',  linestyle='--', label='ttd_gk,ob:')
red_line = mlines.Line2D([], [], color='red', linestyle='--', label='5 K')
yellow_line = mlines.Line2D([], [], color='orange', linestyle='--', label='10 K')
green_line = mlines.Line2D([], [], color='green', linestyle='--', label='15 K')
blue_line = mlines.Line2D([], [], color='steelblue', linestyle='--', label='20 K')
black_line = mlines.Line2D([], [], color='blueviolet', linestyle='--', label='25 K')
plt.legend(handles=[o_line, red_line, yellow_line, green_line, blue_line], loc='lower center', ncol=7)
plt.ylim(68.5, 74)
plt.xlim(37.5, 60)
plt.grid()
plt.savefig('Senkenaustrittstemperatur Parallel R1233ZD(E).svg')
plt.show()

plt.plot(data_T190_IHX_R600, eta_T190_IHX_R600, color='black', label='190°C')
plt.annotate('190', xy=(70.05, 64.6), xytext=(70.05, 64.6), fontsize='12')
plt.plot(data_T195_IHX_R600, eta_T195_IHX_R600, color='black', label='195°C')
plt.annotate('195', xy=(70.05, 65.33), xytext=(70.05, 65.33), fontsize='12')
plt.plot(data_T200_IHX_R600, eta_T200_IHX_R600, color='black', label='200°C')
plt.annotate('200', xy=(70.05, 66.05), xytext=(70.05, 66.05), fontsize='12')
plt.plot(data_T205_IHX_R600, eta_T205_IHX_R600, color='black', label='205°C')
plt.annotate('205', xy=(70.05, 66.8), xytext=(70.05, 66.8), fontsize='12')
plt.plot(data_T210_IHX_R600, eta_T210_IHX_R600, color='black', label='210°C')
plt.annotate('210', xy=(37.9, 67.5), xytext=(70.05, 67.5), fontsize='12')
plt.plot(data_T215_IHX_R600, eta_T215_IHX_R600, color='black', label='215°C')
plt.annotate('215', xy=(70.05, 68.18), xytext=(70.05, 68.18), fontsize='12')
plt.plot(data_T220_IHX_R600, eta_T220_IHX_R600, color='black', label='220°C')
plt.annotate('220', xy=(70.05, 68.9), xytext=(70.05, 68.9), fontsize='12')
plt.plot(data_ttd_u_10_IHX_R600, eta_ttd_u_10_IHX_R600, linestyle='--', color='red', label='10 K')
plt.plot(data_ttd_u_15_IHX_R600, eta_ttd_u_15_IHX_R600, linestyle='--', color='orange', label='15 K')
plt.plot(data_ttd_u_20_IHX_R600, eta_ttd_u_20_IHX_R600, linestyle='--', color='green', label='20 K')
plt.plot(data_ttd_u_30_IHX_R600, eta_ttd_u_30_IHX_R600, linestyle='--', color='steelblue', label='30 K')
o_line = mlines.Line2D([], [], color='black', label=r'$T_{se,ein}$ [C]          $ΔT_{gk,ob}$:')
s_line = mlines.Line2D([], [], color='black',  linestyle='--', label='ΔT_{gk,ob}:')
red_line = mlines.Line2D([], [], color='red', linestyle='--', label='10 K')
yellow_line = mlines.Line2D([], [], color='orange', linestyle='--', label='15 K')
green_line = mlines.Line2D([], [], color='green', linestyle='--', label='20 K')
blue_line = mlines.Line2D([], [], color='steelblue', linestyle='--', label='30 K')
plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('exergetischer Wirkungsgrad')
plt.ylim(45, 70)
plt.legend(handles=[o_line, red_line, yellow_line, green_line, blue_line], loc='lower center', ncol=7)
plt.grid()
plt.savefig('Senkenaustrittstemperatur IWUE R600.svg')
plt.show()

plt.plot(data_T190_Parallel_R600, eta_T190_Parallel_R600, color='black', label='190')
plt.annotate('190', xy=(75, 64.88), xytext=(75, 64.88))
plt.plot(data_T195_Parallel_R600, eta_T195_Parallel_R600, color='black', label='195')
plt.annotate('195', xy=(75, 65.59), xytext=(75, 65.59))
plt.plot(data_T200_Parallel_R600, eta_T200_Parallel_R600, color='black', label='200')
plt.annotate('200', xy=(75, 66.31), xytext=(75, 66.31))
plt.plot(data_T205_Parallel_R600, eta_T205_Parallel_R600, color='black', label='205')
plt.annotate('205', xy=(75, 67.05), xytext=(75, 67.05))
plt.plot(data_T210_Parallel_R600, eta_T210_Parallel_R600, color='black', label='210')
plt.annotate('210', xy=(75, 67.75), xytext=(75, 67.75))
o_line = mlines.Line2D([], [], color='black', label=r'$T_{se,ein}$ [C]          $ΔT_{gk,ob}$:')
s_line = mlines.Line2D([], [], color='black',  linestyle='--', label='ttd_gk,ob:')
red_line = mlines.Line2D([], [], color='red', linestyle='--', label='5 K')
yellow_line = mlines.Line2D([], [], color='orange', linestyle='--', label='10 K')
green_line = mlines.Line2D([], [], color='green', linestyle='--', label='15 K')
blue_line = mlines.Line2D([], [], color='steelblue', linestyle='--', label='20 K')
black_line = mlines.Line2D([], [], color='blueviolet', linestyle='--', label='25 K')
plt.plot(data_ttd_u_5_Parallel_R600, eta_ttd_u_5_Parallel_R600, linestyle='--', color='red', label='5 K')
plt.plot(data_ttd_u_10_Parallel_R600, eta_ttd_u_10_Parallel_R600, linestyle='--', color='orange', label='10 K')
plt.plot(data_ttd_u_15_Parallel_R600, eta_ttd_u_15_Parallel_R600, linestyle='--', color='green', label='15 K')
plt.plot(data_ttd_u_20_Parallel_R600, eta_ttd_u_20_Parallel_R600, linestyle='--', color='steelblue', label='20 K')
plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('exergetischer Wirkungsgrad')
plt.xlim(50, 76)
plt.legend(handles=[o_line, red_line, yellow_line, green_line, blue_line], loc='lower center', ncol=7)
plt.grid()
plt.savefig('Senkenaustrittstemperatur Parallel R600.svg')
plt.show()

plt.plot(data_T190_IHX_R1336MZZZ, eta_T190_IHX_R1336MZZZ, color='black', label='190°C')
plt.annotate('190', xy=(35.03, 68.53), xytext=(35.03, 68.53))
plt.plot(data_T195_IHX_R1336MZZZ, eta_T195_IHX_R1336MZZZ, color='black', label='195°C')
plt.annotate('195', xy=(35.03, 69.28), xytext=(35.03, 69.28))
plt.plot(data_T200_IHX_R1336MZZZ, eta_T200_IHX_R1336MZZZ, color='black', label='200°C')
plt.annotate('200', xy=(35.03, 70.01), xytext=(35.03, 70.01))
plt.plot(data_T205_IHX_R1336MZZZ, eta_T205_IHX_R1336MZZZ, color='black', label='205°C')
plt.annotate('205', xy=(35.03, 70.72), xytext=(35.03, 70.72))
plt.plot(data_T210_IHX_R1336MZZZ, eta_T210_IHX_R1336MZZZ, color='black', label='210°C')
plt.annotate('210', xy=(35.03, 71.46), xytext=(35.03, 71.46))
plt.plot(data_T215_IHX_R1336MZZZ, eta_T215_IHX_R1336MZZZ, color='black', label='215°C')
plt.annotate('215', xy=(35.03, 72.17), xytext=(35.03, 72.17))
plt.plot(data_T220_IHX_R1336MZZZ, eta_T220_IHX_R1336MZZZ, color='black', label='220°C')
plt.annotate('220', xy=(35.03, 72.89), xytext=(35.03, 72.89))
o_line = mlines.Line2D([], [], color='black', label=r'$T_{se,ein}$ [C]          $ΔT_{gk,ob}$:')
s_line = mlines.Line2D([], [], color='black',  linestyle='--', label='ΔT_{gk,ob}:')
red_line = mlines.Line2D([], [], color='red', linestyle='--', label='10 K')
yellow_line = mlines.Line2D([], [], color='orange', linestyle='--', label='15 K')
green_line = mlines.Line2D([], [], color='green', linestyle='--', label='20 K')
blue_line = mlines.Line2D([], [], color='steelblue', linestyle='--', label='30 K')
plt.plot(data_ttd_u_10_IHX_R1336MZZZ, eta_ttd_u_10_IHX_R1336MZZZ, linestyle='--', color='red', label='10 K')
plt.plot(data_ttd_u_15_IHX_R1336MZZZ, eta_ttd_u_15_IHX_R1336MZZZ, linestyle='--', color='orange', label='15 K')
plt.plot(data_ttd_u_20_IHX_R1336MZZZ, eta_ttd_u_20_IHX_R1336MZZZ, linestyle='--', color='green', label='20 K')
plt.plot(data_ttd_u_30_IHX_R1336MZZZ, eta_ttd_u_30_IHX_R1336MZZZ, linestyle='--', color='steelblue', label='30 K')
plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('exergetischer Wirkungsgrad')
plt.legend(handles=[o_line, red_line, yellow_line, green_line, blue_line], loc='lower center', ncol=7)
plt.grid()
plt.savefig('Senkenaustrittstemperatur IWUE R1336MZZ(Z).svg')
plt.show()

#vielleicht bei 50 bar enden lassen
plt.plot(data_T190_Parallel_R1336MZZZ, eta_T190_Parallel_R1336MZZZ, color='black', label='190')
plt.annotate('190', xy=(52.8, 68.0), xytext=(52.8, 68.0))
plt.plot(data_T195_Parallel_R1336MZZZ, eta_T195_Parallel_R1336MZZZ, color='black', label='195')
plt.annotate('195', xy=(53.9, 68.6), xytext=(53.9, 68.6))
plt.plot(data_T200_Parallel_R1336MZZZ, eta_T200_Parallel_R1336MZZZ, color='black', label='200')
plt.annotate('200', xy=(54.6, 69.25), xytext=(54.6, 69.25))
plt.plot(data_T205_Parallel_R1336MZZZ, eta_T205_Parallel_R1336MZZZ, color='black', label='205')
plt.annotate('205', xy=(55.2, 69.9), xytext=(55.2, 69.9))
plt.plot(data_T210_Parallel_R1336MZZZ, eta_T210_Parallel_R1336MZZZ, color='black', label='210')
plt.annotate('210', xy=(55.8, 70.55), xytext=(55.8, 70.55))
plt.plot(data_T215_Parallel_R1336MZZZ, eta_T215_Parallel_R1336MZZZ, color='black', label='215')
plt.annotate('215', xy=(56.3, 71.18), xytext=(56.3, 71.18))
o_line = mlines.Line2D([], [], color='black', label=r'$T_{se,ein}$ [C]          $ΔT_{gk,ob}$:')
s_line = mlines.Line2D([], [], color='black',  linestyle='--', label='ΔT_{gk,ob}:')
red_line = mlines.Line2D([], [], color='red', linestyle='--', label='5 K')
yellow_line = mlines.Line2D([], [], color='orange', linestyle='--', label='10 K')
green_line = mlines.Line2D([], [], color='green', linestyle='--', label='15 K')
blue_line = mlines.Line2D([], [], color='steelblue', linestyle='--', label='20 K')
black_line = mlines.Line2D([], [], color='blueviolet', linestyle='--', label='25 K')
plt.plot(data_ttd_u_5_Parallel_R1336MZZZ, eta_ttd_u_5_Parallel_R1336MZZZ, linestyle='--', color='red', label='5 K')
plt.plot(data_ttd_u_10_Parallel_R1336MZZZ, eta_ttd_u_10_Parallel_R1336MZZZ, linestyle='--', color='orange', label='10 K')
plt.plot(data_ttd_u_15_Parallel_R1336MZZZ, eta_ttd_u_15_Parallel_R1336MZZZ, linestyle='--', color='green', label='15 K')
plt.plot(data_ttd_u_20_Parallel_R1336MZZZ, eta_ttd_u_20_Parallel_R1336MZZZ, linestyle='--', color='steelblue', label='20 K')
plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('exergetischer Wirkungsgrad')
plt.xlim(30, 58)
plt.ylim(67.8, 74)
plt.legend(handles=[o_line, red_line, yellow_line, green_line, blue_line], loc='upper center', ncol=7)
plt.grid()
plt.savefig('Senkenaustrittstemperatur Parallel R1336MZZ(Z).svg')
plt.show()

plt.plot(data_T190_IHX_R601, eta_T190_IHX_R601, color='black', label='190°C')
plt.annotate('190', xy=(40.05, 68.63), xytext=(40.05, 68.63))
plt.plot(data_T195_IHX_R601, eta_T195_IHX_R601, color='black', label='195°C')
plt.annotate('195', xy=(40.05, 69.42), xytext=(40.05, 69.42))
plt.plot(data_T200_IHX_R601, eta_T200_IHX_R601, color='black', label='200°C')
plt.annotate('200', xy=(40.05, 70.15), xytext=(40.05, 70.15))
plt.plot(data_T205_IHX_R601, eta_T205_IHX_R601, color='black', label='205°C')
plt.annotate('205', xy=(40.05, 70.9), xytext=(40.05, 70.9))
plt.plot(data_T210_IHX_R601, eta_T210_IHX_R601, color='black', label='210°C')
plt.annotate('210', xy=(40.05, 71.6), xytext=(40.05, 71.6))
plt.plot(data_T215_IHX_R601, eta_T215_IHX_R601, color='black', label='215°C')
plt.annotate('215', xy=(40.05, 72.32), xytext=(40.05, 72.32))
plt.plot(data_T220_IHX_R601, eta_T220_IHX_R601, color='black', label='220°C')
plt.annotate('220', xy=(40.05, 73.04), xytext=(40.05, 73.04))
plt.plot(data_ttd_u_10_IHX_R601, eta_ttd_u_10_IHX_R601, linestyle='--', color='red', label='10°C')
plt.plot(data_ttd_u_15_IHX_R601, eta_ttd_u_15_IHX_R601, linestyle='--', color='orange', label='15°C')
plt.plot(data_ttd_u_20_IHX_R601, eta_ttd_u_20_IHX_R601, linestyle='--', color='green', label='20°C')
plt.plot(data_ttd_u_30_IHX_R601, eta_ttd_u_30_IHX_R601, linestyle='--', color='steelblue', label='30°C')
o_line = mlines.Line2D([], [], color='black', label=r'$T_{se,ein}$ [C]          $ΔT_{gk,ob}$:')
s_line = mlines.Line2D([], [], color='black',  linestyle='--', label='ΔT_{gk,ob}:')
red_line = mlines.Line2D([], [], color='red', linestyle='--', label='10 K')
yellow_line = mlines.Line2D([], [], color='orange', linestyle='--', label='15 K')
green_line = mlines.Line2D([], [], color='green', linestyle='--', label='20 K')
blue_line = mlines.Line2D([], [], color='steelblue', linestyle='--', label='30 K')
plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('exergetischer Wirkungsgrad')
plt.xlim(24, 41)
plt.ylim(68.01, 78)
plt.legend(handles=[o_line, red_line, yellow_line, green_line, blue_line], loc='lower center', ncol=7)
plt.grid()
plt.savefig('Senkenaustrittstemperatur IWUE R601.svg')
plt.show()

plt.plot(data_T190_Parallel_R601, eta_T190_Parallel_R601, color='black', label='190°C')
plt.annotate('190', xy=(55, 68.2), xytext=(55, 68.2))
plt.plot(data_T195_Parallel_R601, eta_T195_Parallel_R601, color='black', label='195°C')
plt.annotate('195', xy=(55, 68.95), xytext=(55, 68.95))
plt.plot(data_T200_Parallel_R601, eta_T200_Parallel_R601, color='black', label='200°C')
plt.annotate('200', xy=(55, 69.7), xytext=(55, 69.7))
plt.plot(data_T205_Parallel_R601, eta_T205_Parallel_R601, color='black', label='205°C')
plt.annotate('205', xy=(55, 70.4), xytext=(55, 70.4))
plt.plot(data_T210_Parallel_R601, eta_T210_Parallel_R601, color='black', label='210°C')
plt.annotate('210', xy=(55, 71.15), xytext=(55, 71.15))
plt.plot(data_T215_Parallel_R601, eta_T215_Parallel_R601, color='black', label='215°C')
plt.annotate('215', xy=(55, 71.85), xytext=(55, 71.85))
plt.plot(data_T220_Parallel_R601, eta_T220_Parallel_R601, color='black', label='220°C')
plt.annotate('220', xy=(55, 72.55), xytext=(55, 72.55))
o_line = mlines.Line2D([], [], color='black', label=r'$T_{se,ein}$ [C]          $ΔT_{gk,ob}$:')
s_line = mlines.Line2D([], [], color='black',  linestyle='--', label='ttd_gk,ob:')
red_line = mlines.Line2D([], [], color='red', linestyle='--', label='5 K')
yellow_line = mlines.Line2D([], [], color='orange', linestyle='--', label='10 K')
green_line = mlines.Line2D([], [], color='green', linestyle='--', label='15 K')
blue_line = mlines.Line2D([], [], color='steelblue', linestyle='--', label='20 K')
black_line = mlines.Line2D([], [], color='blueviolet', linestyle='--', label='25 K')
plt.plot(data_ttd_u_5_Parallel_R601, eta_ttd_u_5_Parallel_R601, linestyle='--', color='red', label='5 K')
plt.plot(data_ttd_u_10_Parallel_R601, eta_ttd_u_10_Parallel_R601, linestyle='--', color='orange', label='10 K')
plt.plot(data_ttd_u_15_Parallel_R601, eta_ttd_u_15_Parallel_R601, linestyle='--', color='green', label='15 K')
plt.plot(data_ttd_u_20_Parallel_R601, eta_ttd_u_20_Parallel_R601, linestyle='--', color='steelblue', label='20 K')
plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('exergetischer Wirkungsgrad')
plt.ylim(68, 76)
plt.legend(handles=[o_line, red_line, yellow_line, green_line, blue_line], loc='lower center', ncol=7)
plt.grid()
plt.savefig('Senkenaustrittstemperatur Parallel R601.svg')
plt.show()