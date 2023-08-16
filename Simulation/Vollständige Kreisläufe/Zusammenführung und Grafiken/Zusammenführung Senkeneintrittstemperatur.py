import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import json

#Import der Datensätze
with open('../mit interner Wärmerückgewinnung/Senkeneintrittstemperatur.txt') as f:
    read = f.readlines()

data_IHX_T160_R1233ZDE = json.loads(read[5])
eta_IHX_T160_R1233ZDE = json.loads(read[6])

data_IHX_T150_R1233ZDE = json.loads(read[9])
eta_IHX_T150_R1233ZDE = json.loads(read[10])

data_IHX_T140_R1233ZDE = json.loads(read[13])
eta_IHX_T140_R1233ZDE = json.loads(read[14])

data_IHX_T130_R1233ZDE = json.loads(read[17])
eta_IHX_T130_R1233ZDE = json.loads(read[18])

data_IHX_T120_R1233ZDE = json.loads(read[21])
eta_IHX_T120_R1233ZDE = json.loads(read[22])

data_ttd_u_5_IHX_R1233ZDE = json.loads(read[27])
eta_ttd_u_5_IHX_R1233ZDE = json.loads(read[28])

data_ttd_u_10_IHX_R1233ZDE = json.loads(read[32])
eta_ttd_u_10_IHX_R1233ZDE = json.loads(read[33])

data_ttd_u_15_IHX_R1233ZDE = json.loads(read[37])
eta_ttd_u_15_IHX_R1233ZDE = json.loads(read[38])

data_ttd_u_20_IHX_R1233ZDE = json.loads(read[42])
eta_ttd_u_20_IHX_R1233ZDE = json.loads(read[43])

data_ttd_u_25_IHX_R1233ZDE = json.loads(read[47])
eta_ttd_u_25_IHX_R1233ZDE = json.loads(read[48])

data_IHX_T160_R600 = json.loads(read[54])
eta_IHX_T160_R600 = json.loads(read[55])

data_IHX_T150_R600 = json.loads(read[58])
eta_IHX_T150_R600 = json.loads(read[59])

data_IHX_T140_R600 = json.loads(read[62])
eta_IHX_T140_R600 = json.loads(read[63])

data_IHX_T130_R600 = json.loads(read[66])
eta_IHX_T130_R600 = json.loads(read[67])

data_IHX_T120_R600 = json.loads(read[70])
eta_IHX_T120_R600 = json.loads(read[71])

data_ttd_u_5_IHX_R600 = json.loads(read[76])
eta_ttd_u_5_IHX_R600 = json.loads(read[77])

data_ttd_u_10_IHX_R600 = json.loads(read[81])
eta_ttd_u_10_IHX_R600 = json.loads(read[82])

data_ttd_u_15_IHX_R600 = json.loads(read[86])
eta_ttd_u_15_IHX_R600 = json.loads(read[87])

data_ttd_u_20_IHX_R600 = json.loads(read[91])
eta_ttd_u_20_IHX_R600 = json.loads(read[92])

data_ttd_u_25_IHX_R600 = json.loads(read[96])
eta_ttd_u_25_IHX_R600 = json.loads(read[97])

data_IHX_T160_R1336MZZZ = json.loads(read[103])
eta_IHX_T160_R1336MZZZ = json.loads(read[104])

data_IHX_T150_R1336MZZZ = json.loads(read[107])
eta_IHX_T150_R1336MZZZ = json.loads(read[108])

data_IHX_T140_R1336MZZZ = json.loads(read[111])
eta_IHX_T140_R1336MZZZ = json.loads(read[112])

data_IHX_T130_R1336MZZZ = json.loads(read[115])
eta_IHX_T130_R1336MZZZ = json.loads(read[116])

data_IHX_T120_R1336MZZZ = json.loads(read[119])
eta_IHX_T120_R1336MZZZ = json.loads(read[120])

data_ttd_u_5_IHX_R1336MZZZ = json.loads(read[125])
eta_ttd_u_5_IHX_R1336MZZZ = json.loads(read[126])

data_ttd_u_10_IHX_R1336MZZZ = json.loads(read[130])
eta_ttd_u_10_IHX_R1336MZZZ = json.loads(read[131])

data_ttd_u_15_IHX_R1336MZZZ = json.loads(read[135])
eta_ttd_u_15_IHX_R1336MZZZ = json.loads(read[136])

data_ttd_u_20_IHX_R1336MZZZ = json.loads(read[140])
eta_ttd_u_20_IHX_R1336MZZZ = json.loads(read[141])

data_ttd_u_25_IHX_R1336MZZZ = json.loads(read[145])
eta_ttd_u_25_IHX_R1336MZZZ = json.loads(read[146])

data_IHX_T160_R601 = json.loads(read[152])
eta_IHX_T160_R601 = json.loads(read[153])

data_IHX_T150_R601 = json.loads(read[156])
eta_IHX_T150_R601 = json.loads(read[157])

data_IHX_T140_R601 = json.loads(read[160])
eta_IHX_T140_R601 = json.loads(read[161])

data_IHX_T130_R601 = json.loads(read[164])
eta_IHX_T130_R601 = json.loads(read[165])

data_IHX_T120_R601 = json.loads(read[168])
eta_IHX_T120_R601 = json.loads(read[169])

data_ttd_u_5_IHX_R601 = json.loads(read[174])
eta_ttd_u_5_IHX_R601 = json.loads(read[175])

data_ttd_u_10_IHX_R601 = json.loads(read[179])
eta_ttd_u_10_IHX_R601 = json.loads(read[180])

data_ttd_u_15_IHX_R601 = json.loads(read[184])
eta_ttd_u_15_IHX_R601 = json.loads(read[185])

data_ttd_u_20_IHX_R601 = json.loads(read[189])
eta_ttd_u_20_IHX_R601 = json.loads(read[190])

data_ttd_u_25_IHX_R601 = json.loads(read[194])
eta_ttd_u_25_IHX_R601 = json.loads(read[195])

with open('../mit interner Wärmerückgewinnung und Parallelkompression/Senkeneintrittstemperatur.txt') as f:
    read = f.readlines()

data_Parallel_T160_R1233ZDE = json.loads(read[5])
eta_Parallel_T160_R1233ZDE = json.loads(read[6])

data_Parallel_T150_R1233ZDE = json.loads(read[9])
eta_Parallel_T150_R1233ZDE = json.loads(read[10])

data_Parallel_T140_R1233ZDE = json.loads(read[13])
eta_Parallel_T140_R1233ZDE = json.loads(read[14])

data_Parallel_T130_R1233ZDE = json.loads(read[17])
eta_Parallel_T130_R1233ZDE = json.loads(read[18])

data_ttd_u_5_Parallel_R1233ZDE = json.loads(read[23])
eta_ttd_u_5_Parallel_R1233ZDE = json.loads(read[24])

data_ttd_u_10_Parallel_R1233ZDE = json.loads(read[29])
eta_ttd_u_10_Parallel_R1233ZDE = json.loads(read[30])

data_ttd_u_15_Parallel_R1233ZDE = json.loads(read[35])
eta_ttd_u_15_Parallel_R1233ZDE = json.loads(read[36])

data_ttd_u_20_Parallel_R1233ZDE = json.loads(read[41])
eta_ttd_u_20_Parallel_R1233ZDE = json.loads(read[42])

data_Parallel_T160_R1233ZDE_opt = json.loads(read[49])
eta_Parallel_T160_R1233ZDE_opt = json.loads(read[50])

data_Parallel_T150_R1233ZDE_opt = json.loads(read[55])
eta_Parallel_T150_R1233ZDE_opt = json.loads(read[56])

data_Parallel_T140_R1233ZDE_opt = json.loads(read[61])
eta_Parallel_T140_R1233ZDE_opt = json.loads(read[62])

data_Parallel_T130_R1233ZDE_opt = json.loads(read[67])
eta_Parallel_T130_R1233ZDE_opt = json.loads(read[68])

data_ttd_u_5_Parallel_R1233ZDE_opt = json.loads(read[75])
eta_ttd_u_5_Parallel_R1233ZDE_opt = json.loads(read[76])

data_ttd_u_10_Parallel_R1233ZDE_opt = json.loads(read[81])
eta_ttd_u_10_Parallel_R1233ZDE_opt = json.loads(read[82])

data_ttd_u_15_Parallel_R1233ZDE_opt = json.loads(read[87])
eta_ttd_u_15_Parallel_R1233ZDE_opt = json.loads(read[88])

data_ttd_u_20_Parallel_R1233ZDE_opt = json.loads(read[93])
eta_ttd_u_20_Parallel_R1233ZDE_opt = json.loads(read[94])

data_Parallel_T160_R600 = json.loads(read[101])
eta_Parallel_T160_R600 = json.loads(read[102])

data_Parallel_T150_R600 = json.loads(read[105])
eta_Parallel_T150_R600 = json.loads(read[106])

data_Parallel_T140_R600 = json.loads(read[109])
eta_Parallel_T140_R600 = json.loads(read[110])

data_Parallel_T130_R600 = json.loads(read[113])
eta_Parallel_T130_R600 = json.loads(read[114])

data_ttd_u_5_Parallel_R600 = json.loads(read[119])
eta_ttd_u_5_Parallel_R600 = json.loads(read[120])

data_ttd_u_10_Parallel_R600 = json.loads(read[125])
eta_ttd_u_10_Parallel_R600 = json.loads(read[126])

data_ttd_u_15_Parallel_R600 = json.loads(read[131])
eta_ttd_u_15_Parallel_R600 = json.loads(read[132])

data_ttd_u_20_Parallel_R600 = json.loads(read[137])
eta_ttd_u_20_Parallel_R600 = json.loads(read[138])

data_Parallel_T160_R600_opt = json.loads(read[145])
eta_Parallel_T160_R600_opt = json.loads(read[146])

data_Parallel_T150_R600_opt = json.loads(read[151])
eta_Parallel_T150_R600_opt = json.loads(read[152])

data_Parallel_T140_R600_opt = json.loads(read[157])
eta_Parallel_T140_R600_opt = json.loads(read[158])

data_Parallel_T130_R600_opt = json.loads(read[163])
eta_Parallel_T130_R600_opt = json.loads(read[164])

data_ttd_u_5_Parallel_R600_opt = json.loads(read[171])
eta_ttd_u_5_Parallel_R600_opt = json.loads(read[172])

data_ttd_u_10_Parallel_R600_opt = json.loads(read[177])
eta_ttd_u_10_Parallel_R600_opt = json.loads(read[178])

data_ttd_u_15_Parallel_R600_opt = json.loads(read[183])
eta_ttd_u_15_Parallel_R600_opt = json.loads(read[184])

data_ttd_u_20_Parallel_R600_opt = json.loads(read[189])
eta_ttd_u_20_Parallel_R600_opt = json.loads(read[190])

data_Parallel_T160_R1336MZZZ = json.loads(read[197])
eta_Parallel_T160_R1336MZZZ = json.loads(read[198])

data_Parallel_T150_R1336MZZZ = json.loads(read[201])
eta_Parallel_T150_R1336MZZZ = json.loads(read[202])

data_Parallel_T140_R1336MZZZ = json.loads(read[205])
eta_Parallel_T140_R1336MZZZ = json.loads(read[206])

data_Parallel_T130_R1336MZZZ = json.loads(read[209])
eta_Parallel_T130_R1336MZZZ = json.loads(read[210])

data_ttd_u_5_Parallel_R1336MZZZ = json.loads(read[215])
eta_ttd_u_5_Parallel_R1336MZZZ = json.loads(read[216])

data_ttd_u_10_Parallel_R1336MZZZ = json.loads(read[221])
eta_ttd_u_10_Parallel_R1336MZZZ = json.loads(read[222])

data_ttd_u_15_Parallel_R1336MZZZ = json.loads(read[227])
eta_ttd_u_15_Parallel_R1336MZZZ = json.loads(read[228])

data_ttd_u_20_Parallel_R1336MZZZ = json.loads(read[233])
eta_ttd_u_20_Parallel_R1336MZZZ = json.loads(read[234])

data_Parallel_T160_R1336MZZZ_opt = json.loads(read[241])
eta_Parallel_T160_R1336MZZZ_opt = json.loads(read[242])

data_Parallel_T150_R1336MZZZ_opt = json.loads(read[247])
eta_Parallel_T150_R1336MZZZ_opt = json.loads(read[248])

data_Parallel_T140_R1336MZZZ_opt = json.loads(read[253])
eta_Parallel_T140_R1336MZZZ_opt = json.loads(read[254])

data_Parallel_T130_R1336MZZZ_opt = json.loads(read[259])
eta_Parallel_T130_R1336MZZZ_opt = json.loads(read[260])

data_ttd_u_5_Parallel_R1336MZZZ_opt = json.loads(read[267])
eta_ttd_u_5_Parallel_R1336MZZZ_opt = json.loads(read[268])

data_ttd_u_10_Parallel_R1336MZZZ_opt = json.loads(read[273])
eta_ttd_u_10_Parallel_R1336MZZZ_opt = json.loads(read[274])

data_ttd_u_15_Parallel_R1336MZZZ_opt = json.loads(read[279])
eta_ttd_u_15_Parallel_R1336MZZZ_opt = json.loads(read[280])

data_ttd_u_20_Parallel_R1336MZZZ_opt = json.loads(read[285])
eta_ttd_u_20_Parallel_R1336MZZZ_opt = json.loads(read[286])

data_Parallel_T160_R601 = json.loads(read[293])
eta_Parallel_T160_R601 = json.loads(read[294])

data_Parallel_T155_R601 = json.loads(read[297])
eta_Parallel_T155_R601 = json.loads(read[298])

data_Parallel_T150_R601 = json.loads(read[301])
eta_Parallel_T150_R601 = json.loads(read[302])

data_ttd_u_5_Parallel_R601 = json.loads(read[307])
eta_ttd_u_5_Parallel_R601 = json.loads(read[308])

data_ttd_u_10_Parallel_R601 = json.loads(read[313])
eta_ttd_u_10_Parallel_R601 = json.loads(read[314])

data_ttd_u_15_Parallel_R601 = json.loads(read[319])
eta_ttd_u_15_Parallel_R601 = json.loads(read[320])

data_ttd_u_20_Parallel_R601 = json.loads(read[325])
eta_ttd_u_20_Parallel_R601 = json.loads(read[326])

data_Parallel_T160_R601_opt = json.loads(read[333])
eta_Parallel_T160_R601_opt = json.loads(read[334])

data_Parallel_T155_R601_opt = json.loads(read[339])
eta_Parallel_T155_R601_opt = json.loads(read[340])

data_Parallel_T150_R601_opt = json.loads(read[345])
eta_Parallel_T150_R601_opt = json.loads(read[346])

data_ttd_u_5_Parallel_R601_opt = json.loads(read[353])
eta_ttd_u_5_Parallel_R601_opt = json.loads(read[354])

data_ttd_u_10_Parallel_R601_opt = json.loads(read[359])
eta_ttd_u_10_Parallel_R601_opt = json.loads(read[360])

data_ttd_u_15_Parallel_R601_opt = json.loads(read[365])
eta_ttd_u_15_Parallel_R601_opt = json.loads(read[366])

data_ttd_u_20_Parallel_R601_opt = json.loads(read[371])
eta_ttd_u_20_Parallel_R601_opt = json.loads(read[372])

#Erstellung der Grafiken mit Kennzeichnung von Datenpunkten
plt.rc('font', **{'size': 20})
plt.rcParams["figure.figsize"] = (20, 12)

plt.plot(data_IHX_T160_R1233ZDE, eta_IHX_T160_R1233ZDE, color='black', label='160°C IHX')
plt.annotate('160', xy=(54.1, 66.68), xytext=(54.1, 66.68))
plt.plot(data_IHX_T150_R1233ZDE, eta_IHX_T150_R1233ZDE, color='black', label='150°C IHX')
plt.annotate('150', xy=(54.1, 68.27), xytext=(54.1, 68.27))
plt.plot(data_IHX_T140_R1233ZDE, eta_IHX_T140_R1233ZDE,  color='black', label=' 140°C IHX')
plt.annotate('140', xy=(54.1, 69.46), xytext=(54.1, 69.46))
plt.plot(data_IHX_T130_R1233ZDE, eta_IHX_T130_R1233ZDE,  color='black', label='130°C IHX')
plt.annotate('130', xy=(54.1, 70.46), xytext=(54.1, 70.46))
plt.plot(data_IHX_T120_R1233ZDE, eta_IHX_T120_R1233ZDE,  color='black', label='120°C IHX')
plt.annotate('120', xy=(54.1, 70.32), xytext=(54.1, 71.32))
plt.plot(data_ttd_u_5_IHX_R1233ZDE, eta_ttd_u_5_IHX_R1233ZDE, linestyle='--', color='red')
plt.plot(data_ttd_u_10_IHX_R1233ZDE, eta_ttd_u_10_IHX_R1233ZDE, linestyle='--', color='orange')
plt.plot(data_ttd_u_15_IHX_R1233ZDE, eta_ttd_u_15_IHX_R1233ZDE, linestyle='--', color='green')
plt.plot(data_ttd_u_20_IHX_R1233ZDE, eta_ttd_u_20_IHX_R1233ZDE, linestyle='--', color='steelblue')
plt.plot(data_ttd_u_25_IHX_R1233ZDE, eta_ttd_u_25_IHX_R1233ZDE, linestyle='--', color='blueviolet')
o_line = mlines.Line2D([], [], color='black', label=r'$T_{se,ein}$ [°C]          $ΔT_{GK,ob}$:')
red_line = mlines.Line2D([], [], color='red', linestyle='--', label='5 K')
orange_line = mlines.Line2D([], [], color='orange', linestyle='--', label='10 K')
green_line = mlines.Line2D([], [], color='green', linestyle='--', label='15 K')
blue_line = mlines.Line2D([], [], color='steelblue', linestyle='--', label='20 K')
black_line = mlines.Line2D([], [], color='blueviolet', linestyle='--', label='25 K')
plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
plt.xlim(32, 55)
plt.ylim(65, 78)
plt.legend(handles=[o_line, red_line, orange_line, green_line, blue_line, black_line], loc='lower center', ncol=7)
plt.grid()
plt.savefig('Senkeneintrittstemperatur IWUE R1233ZD(E).svg')
plt.show()

plt.plot(data_Parallel_T160_R1233ZDE, eta_Parallel_T160_R1233ZDE, color='black', label='160°C Parallel')
plt.annotate('160', xy=(54.1, 69.15), xytext=(54.1, 69.15))
plt.plot(data_Parallel_T150_R1233ZDE, eta_Parallel_T150_R1233ZDE, color='black', label='150°C Parallel')
plt.annotate('150', xy=(54.1, 70.41), xytext=(54.1, 70.41))
plt.plot(data_Parallel_T140_R1233ZDE, eta_Parallel_T140_R1233ZDE, color='black', label='140°C Parallel')
plt.annotate('140', xy=(54.1, 71.35), xytext=(54.1, 71.35))
plt.plot(data_Parallel_T130_R1233ZDE, eta_Parallel_T130_R1233ZDE, color='black', label='130°C Parallel')
plt.annotate('130', xy=(54.1, 72.15), xytext=(54.1, 72.15))
plt.plot(data_ttd_u_5_Parallel_R1233ZDE, eta_ttd_u_5_Parallel_R1233ZDE, color='red', linestyle='--')
plt.plot(data_ttd_u_10_Parallel_R1233ZDE, eta_ttd_u_10_Parallel_R1233ZDE, color='orange', linestyle='--')
plt.plot(data_ttd_u_15_Parallel_R1233ZDE, eta_ttd_u_15_Parallel_R1233ZDE, color='green', linestyle='--')
plt.plot(data_ttd_u_20_Parallel_R1233ZDE, eta_ttd_u_20_Parallel_R1233ZDE, color='steelblue', linestyle='--')
plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
plt.ylim(69, 76)
plt.legend(handles=[o_line, red_line, orange_line, green_line, blue_line], loc='lower center', ncol=7)
plt.grid()
plt.savefig('Senkeneintrittstemperatur Parallel R1233ZD(E).svg')
plt.show()

plt.plot(data_Parallel_T160_R1233ZDE_opt, eta_Parallel_T160_R1233ZDE_opt, color='black')
plt.annotate('160', xy=(54.8, 69.2), xytext=(54.8, 69.15))
plt.plot(data_Parallel_T150_R1233ZDE_opt, eta_Parallel_T150_R1233ZDE_opt, color='black')
plt.annotate('150', xy=(54.8, 69.9), xytext=(54.8, 69.9))
plt.plot(data_Parallel_T140_R1233ZDE_opt, eta_Parallel_T140_R1233ZDE_opt, color='black')
plt.annotate('140', xy=(54.8, 70.9), xytext=(54.8, 70.9))
plt.plot(data_Parallel_T130_R1233ZDE_opt, eta_Parallel_T130_R1233ZDE_opt, color='black')
plt.annotate('130', xy=(54.8, 72), xytext=(54.8, 72))

plt.plot(data_ttd_u_5_Parallel_R1233ZDE_opt, eta_ttd_u_5_Parallel_R1233ZDE_opt, color='red', linestyle='--')
plt.plot(data_ttd_u_10_Parallel_R1233ZDE_opt, eta_ttd_u_10_Parallel_R1233ZDE_opt, color='orange', linestyle='--')
plt.plot(data_ttd_u_15_Parallel_R1233ZDE_opt, eta_ttd_u_15_Parallel_R1233ZDE_opt, color='green', linestyle='--')
plt.plot(data_ttd_u_20_Parallel_R1233ZDE_opt, eta_ttd_u_20_Parallel_R1233ZDE_opt, color='steelblue', linestyle='--')

plt.plot(data_ttd_u_5_Parallel_R1233ZDE_opt[0], eta_ttd_u_5_Parallel_R1233ZDE_opt[0], color='black', marker='x')
plt.annotate('160', xy=(data_ttd_u_5_Parallel_R1233ZDE_opt[0] - 0.04, eta_ttd_u_5_Parallel_R1233ZDE_opt[0] - 0.24), xytext=(data_ttd_u_5_Parallel_R1233ZDE_opt[0] - 0.04, eta_ttd_u_5_Parallel_R1233ZDE_opt[0] - 0.24), fontsize='17')
plt.plot(data_ttd_u_5_Parallel_R1233ZDE_opt[20], eta_ttd_u_5_Parallel_R1233ZDE_opt[20], color='black', marker='x')
plt.annotate('150', xy=(data_ttd_u_5_Parallel_R1233ZDE_opt[20] - 0.55, eta_ttd_u_5_Parallel_R1233ZDE_opt[20] - 0.24), xytext=(data_ttd_u_5_Parallel_R1233ZDE_opt[20] - 0.55, eta_ttd_u_5_Parallel_R1233ZDE_opt[20] - 0.20), fontsize='17')
plt.plot(data_ttd_u_5_Parallel_R1233ZDE_opt[41], eta_ttd_u_5_Parallel_R1233ZDE_opt[41], color='black', marker='x')
plt.annotate('140', xy=(data_ttd_u_5_Parallel_R1233ZDE_opt[41] - 0.34, eta_ttd_u_5_Parallel_R1233ZDE_opt[41] - 0.24), xytext=(data_ttd_u_5_Parallel_R1233ZDE_opt[41] - 0.34, eta_ttd_u_5_Parallel_R1233ZDE_opt[41] - 0.24), fontsize='17')
plt.plot(data_ttd_u_5_Parallel_R1233ZDE_opt[61], eta_ttd_u_5_Parallel_R1233ZDE_opt[61], color='black', marker='x')
plt.annotate('130', xy=(data_ttd_u_5_Parallel_R1233ZDE_opt[61] - 0.34, eta_ttd_u_5_Parallel_R1233ZDE_opt[61] - 0.24), xytext=(data_ttd_u_5_Parallel_R1233ZDE_opt[61] - 0.34, eta_ttd_u_5_Parallel_R1233ZDE_opt[61] - 0.24), fontsize='17')

plt.plot(data_ttd_u_10_Parallel_R1233ZDE_opt[0], eta_ttd_u_10_Parallel_R1233ZDE_opt[0], color='black', marker='x')
plt.annotate('160', xy=(data_ttd_u_10_Parallel_R1233ZDE_opt[0] - 0.3, eta_ttd_u_10_Parallel_R1233ZDE_opt[0] - 0.25), xytext=(data_ttd_u_10_Parallel_R1233ZDE_opt[0] - 0.3, eta_ttd_u_10_Parallel_R1233ZDE_opt[0] - 0.25), fontsize='17')
plt.plot(data_ttd_u_10_Parallel_R1233ZDE_opt[20], eta_ttd_u_10_Parallel_R1233ZDE_opt[20], color='black', marker='x')
plt.annotate('150', xy=(data_ttd_u_10_Parallel_R1233ZDE_opt[20] - 0.55, eta_ttd_u_10_Parallel_R1233ZDE_opt[20] - 0.24), xytext=(data_ttd_u_10_Parallel_R1233ZDE_opt[20] - 0.55, eta_ttd_u_10_Parallel_R1233ZDE_opt[20] - 0.20), fontsize='17')
plt.plot(data_ttd_u_10_Parallel_R1233ZDE_opt[40], eta_ttd_u_10_Parallel_R1233ZDE_opt[40], color='black', marker='x')
plt.annotate('140', xy=(data_ttd_u_10_Parallel_R1233ZDE_opt[40] - 0.34, eta_ttd_u_10_Parallel_R1233ZDE_opt[40] - 0.24), xytext=(data_ttd_u_10_Parallel_R1233ZDE_opt[40] - 0.34, eta_ttd_u_10_Parallel_R1233ZDE_opt[40] - 0.24), fontsize='17')
plt.plot(data_ttd_u_10_Parallel_R1233ZDE_opt[60], eta_ttd_u_10_Parallel_R1233ZDE_opt[60], color='black', marker='x')
plt.annotate('130', xy=(data_ttd_u_10_Parallel_R1233ZDE_opt[60] - 0.34, eta_ttd_u_10_Parallel_R1233ZDE_opt[60] - 0.24), xytext=(data_ttd_u_10_Parallel_R1233ZDE_opt[60] - 0.34, eta_ttd_u_10_Parallel_R1233ZDE_opt[60] - 0.24), fontsize='17')

plt.plot(data_ttd_u_15_Parallel_R1233ZDE_opt[0], eta_ttd_u_15_Parallel_R1233ZDE_opt[0], color='black', marker='x')
plt.annotate('160', xy=(data_ttd_u_15_Parallel_R1233ZDE_opt[0] - 0.3, eta_ttd_u_15_Parallel_R1233ZDE_opt[0] - 0.25), xytext=(data_ttd_u_15_Parallel_R1233ZDE_opt[0] - 0.3, eta_ttd_u_15_Parallel_R1233ZDE_opt[0] - 0.25), fontsize='17')
plt.plot(data_ttd_u_15_Parallel_R1233ZDE_opt[20], eta_ttd_u_15_Parallel_R1233ZDE_opt[20], color='black', marker='x')
plt.annotate('150', xy=(data_ttd_u_15_Parallel_R1233ZDE_opt[20] - 0.55, eta_ttd_u_15_Parallel_R1233ZDE_opt[20] - 0.24), xytext=(data_ttd_u_15_Parallel_R1233ZDE_opt[20] - 0.55, eta_ttd_u_15_Parallel_R1233ZDE_opt[20] - 0.20), fontsize='17')
plt.plot(data_ttd_u_15_Parallel_R1233ZDE_opt[40], eta_ttd_u_15_Parallel_R1233ZDE_opt[40], color='black', marker='x')
plt.annotate('140', xy=(data_ttd_u_15_Parallel_R1233ZDE_opt[40] - 0.34, eta_ttd_u_15_Parallel_R1233ZDE_opt[40] - 0.24), xytext=(data_ttd_u_15_Parallel_R1233ZDE_opt[40] - 0.34, eta_ttd_u_15_Parallel_R1233ZDE_opt[40] - 0.24), fontsize='17')
plt.plot(data_ttd_u_15_Parallel_R1233ZDE_opt[60], eta_ttd_u_15_Parallel_R1233ZDE_opt[60], color='black', marker='x')
plt.annotate('130', xy=(data_ttd_u_15_Parallel_R1233ZDE_opt[60] - 0.34, eta_ttd_u_15_Parallel_R1233ZDE_opt[60] - 0.24), xytext=(data_ttd_u_15_Parallel_R1233ZDE_opt[60] - 0.34, eta_ttd_u_15_Parallel_R1233ZDE_opt[60] - 0.24), fontsize='17')

plt.plot(data_ttd_u_20_Parallel_R1233ZDE_opt[0], eta_ttd_u_20_Parallel_R1233ZDE_opt[0], color='black', marker='x')
plt.annotate('160', xy=(data_ttd_u_20_Parallel_R1233ZDE_opt[0] - 0.3, eta_ttd_u_20_Parallel_R1233ZDE_opt[0] - 0.25), xytext=(data_ttd_u_20_Parallel_R1233ZDE_opt[0] - 0.3, eta_ttd_u_20_Parallel_R1233ZDE_opt[0] - 0.25), fontsize='17')
plt.plot(data_ttd_u_20_Parallel_R1233ZDE_opt[20], eta_ttd_u_20_Parallel_R1233ZDE_opt[20], color='black', marker='x')
plt.annotate('150', xy=(data_ttd_u_20_Parallel_R1233ZDE_opt[20] - 0.55, eta_ttd_u_20_Parallel_R1233ZDE_opt[20] - 0.24), xytext=(data_ttd_u_20_Parallel_R1233ZDE_opt[20] - 0.55, eta_ttd_u_20_Parallel_R1233ZDE_opt[20] - 0.20), fontsize='17')
plt.plot(data_ttd_u_20_Parallel_R1233ZDE_opt[40], eta_ttd_u_20_Parallel_R1233ZDE_opt[40], color='black', marker='x')
plt.annotate('140', xy=(data_ttd_u_20_Parallel_R1233ZDE_opt[40] - 0.34, eta_ttd_u_20_Parallel_R1233ZDE_opt[40] - 0.24), xytext=(data_ttd_u_20_Parallel_R1233ZDE_opt[40] - 0.34, eta_ttd_u_20_Parallel_R1233ZDE_opt[40] - 0.24), fontsize='17')
plt.plot(data_ttd_u_20_Parallel_R1233ZDE_opt[60], eta_ttd_u_20_Parallel_R1233ZDE_opt[60], color='black', marker='x')
plt.annotate('130', xy=(data_ttd_u_20_Parallel_R1233ZDE_opt[60] - 0.34, eta_ttd_u_20_Parallel_R1233ZDE_opt[60] - 0.24), xytext=(data_ttd_u_20_Parallel_R1233ZDE_opt[60] - 0.34, eta_ttd_u_20_Parallel_R1233ZDE_opt[60] - 0.24), fontsize='17')

plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
plt.legend(handles=[o_line, red_line, orange_line, green_line, blue_line], loc='lower center', ncol=7)
#plt.legend(loc='lower left')
plt.ylim(69, 76.5)
plt.xlim(35.5, 55.5)
plt.grid()
plt.savefig('Senkeneintrittstemperatur Parallel R1233ZD(E) optimal.svg')
plt.show()

plt.plot(data_IHX_T160_R600, eta_IHX_T160_R600, color='black', label='160°C IHX')
plt.annotate('160', xy=(65.05, 64.7), xytext=(65.05, 64.7))
plt.plot(data_IHX_T150_R600, eta_IHX_T150_R600, color='black', label='150°C IHX')
plt.annotate('150', xy=(65.05, 66.71), xytext=(65.05, 66.71))
plt.plot(data_IHX_T140_R600, eta_IHX_T140_R600,  color='black', label=' 140°C IHX')
plt.annotate('140', xy=(65.05, 68.24), xytext=(65.05, 68.24))
plt.plot(data_IHX_T130_R600, eta_IHX_T130_R600,  color='black', label='130°C IHX')
plt.annotate('130', xy=(65.05, 69.52), xytext=(65.05, 69.52))
plt.plot(data_IHX_T120_R600, eta_IHX_T120_R600,  color='black', label='120°C IHX')
plt.annotate('120', xy=(65.05, 70.8), xytext=(65.05, 70.8))
plt.plot(data_ttd_u_5_IHX_R600, eta_ttd_u_5_IHX_R600, linestyle='--', color='red')
plt.plot(data_ttd_u_10_IHX_R600, eta_ttd_u_10_IHX_R600, linestyle='--', color='orange')
plt.plot(data_ttd_u_15_IHX_R600, eta_ttd_u_15_IHX_R600, linestyle='--', color='green')
plt.plot(data_ttd_u_20_IHX_R600, eta_ttd_u_20_IHX_R600, linestyle='--', color='steelblue')
plt.plot(data_ttd_u_25_IHX_R600, eta_ttd_u_25_IHX_R600, linestyle='--', color='blueviolet')
o_line = mlines.Line2D([], [], color='black', label=r'$T_{se,ein}$ [°C]          $ΔT_{GK,ob}$:')
s_line = mlines.Line2D([], [], color='black',  linestyle='--', label='ttd_gk,ob:')
red_line = mlines.Line2D([], [], color='red', linestyle='--', label='5 K')
orange_line = mlines.Line2D([], [], color='orange', linestyle='--', label='10 K')
green_line = mlines.Line2D([], [], color='green', linestyle='--', label='15 K')
blue_line = mlines.Line2D([], [], color='steelblue', linestyle='--', label='20 K')
black_line = mlines.Line2D([], [], color='blueviolet', linestyle='--', label='25 K')
plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
plt.ylim(45, 76)
plt.legend(handles=[o_line, red_line, orange_line, green_line, blue_line, black_line], loc='lower center', ncol=7)
plt.grid()
plt.savefig('Senkeneintrittstemperatur IWUE R600.svg')
plt.show()

plt.plot(data_Parallel_T160_R600, eta_Parallel_T160_R600, color='black', label='160°C Parallel')
plt.annotate('160', xy=(70.05, 65.45), xytext=(70.05, 65.45))
plt.plot(data_Parallel_T150_R600, eta_Parallel_T150_R600, color='black', label='150°C Parallel')
plt.annotate('150', xy=(70.05, 67.25), xytext=(70.05, 67.25))
plt.plot(data_Parallel_T140_R600, eta_Parallel_T140_R600, color='black', label=' 140°C Parallel')
plt.annotate('140', xy=(70.05, 68.75), xytext=(70.05, 68.75))
plt.plot(data_Parallel_T130_R600, eta_Parallel_T130_R600, color='black', label='130°C Parallel')
plt.annotate('130', xy=(70.05, 70.05), xytext=(70.05, 70.05))
plt.plot(data_ttd_u_5_Parallel_R600, eta_ttd_u_5_Parallel_R600, linestyle='--', color='red')
plt.plot(data_ttd_u_10_Parallel_R600, eta_ttd_u_10_Parallel_R600, linestyle='--', color='orange')
plt.plot(data_ttd_u_15_Parallel_R600, eta_ttd_u_15_Parallel_R600, linestyle='--', color='green')
plt.plot(data_ttd_u_20_Parallel_R600, eta_ttd_u_20_Parallel_R600, linestyle='--', color='steelblue')

plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
plt.xlim(50, 71)
plt.ylim(65.01, 73)
plt.legend(handles=[o_line, red_line, orange_line, green_line, blue_line], loc='upper center', ncol=7)
plt.grid()
plt.savefig('Senkeneintrittstemperatur Parallel R600.svg')
plt.show()


plt.plot(data_Parallel_T160_R600_opt, eta_Parallel_T160_R600_opt, color='black', label='160°C Parallel')
plt.annotate('160', xy=(75.1, 64.85), xytext=(75.1, 64.85))
plt.plot(data_Parallel_T150_R600_opt, eta_Parallel_T150_R600_opt, color='black', label='150°C Parallel')
plt.annotate('150', xy=(75.05, 66.38), xytext=(75.05, 66.38))
plt.plot(data_Parallel_T140_R600_opt, eta_Parallel_T140_R600_opt,  color='black', label=' 140°C Parallel')
plt.annotate('140', xy=(75.05, 67.65), xytext=(75.05, 67.65))
plt.plot(data_Parallel_T130_R600_opt, eta_Parallel_T130_R600_opt,  color='black', label='130°C Parallel')
plt.annotate('130', xy=(75.05, 69.21), xytext=(75.05, 69.21))
plt.plot(data_ttd_u_5_Parallel_R600_opt, eta_ttd_u_5_Parallel_R600_opt, linestyle='--', color='red')
plt.plot(data_ttd_u_10_Parallel_R600_opt, eta_ttd_u_10_Parallel_R600_opt, linestyle='--', color='orange')
plt.plot(data_ttd_u_15_Parallel_R600_opt, eta_ttd_u_15_Parallel_R600_opt, linestyle='--', color='green')
plt.plot(data_ttd_u_20_Parallel_R600_opt, eta_ttd_u_20_Parallel_R600_opt, linestyle='--', color='steelblue')

plt.plot(data_ttd_u_5_Parallel_R600_opt[0], eta_ttd_u_5_Parallel_R600_opt[0], color='black', marker='x')
plt.annotate('160', xy=(data_ttd_u_5_Parallel_R600_opt[0] - 0.04, eta_ttd_u_5_Parallel_R600_opt[0] - 0.24), xytext=(data_ttd_u_5_Parallel_R600_opt[0] - 0.04, eta_ttd_u_5_Parallel_R600_opt[0] - 0.24), fontsize='17')
plt.plot(data_ttd_u_5_Parallel_R600_opt[20], eta_ttd_u_5_Parallel_R600_opt[20], color='black', marker='x')
plt.annotate('150', xy=(data_ttd_u_5_Parallel_R600_opt[20] - 0.16, eta_ttd_u_5_Parallel_R600_opt[20] - 0.37), xytext=(data_ttd_u_5_Parallel_R600_opt[20] - 0.16, eta_ttd_u_5_Parallel_R600_opt[20] - 0.37), fontsize='17')
plt.plot(data_ttd_u_5_Parallel_R600_opt[40], eta_ttd_u_5_Parallel_R600_opt[40], color='black', marker='x')
plt.annotate('140', xy=(data_ttd_u_5_Parallel_R600_opt[40] - 0.12, eta_ttd_u_5_Parallel_R600_opt[40] - 0.38), xytext=(data_ttd_u_5_Parallel_R600_opt[40] - 0.12, eta_ttd_u_5_Parallel_R600_opt[40] - 0.38), fontsize='17')
plt.plot(data_ttd_u_5_Parallel_R600_opt[60], eta_ttd_u_5_Parallel_R600_opt[60], color='black', marker='x')
plt.annotate('130', xy=(data_ttd_u_5_Parallel_R600_opt[60] - 0.37, eta_ttd_u_5_Parallel_R600_opt[60] - 0.3), xytext=(data_ttd_u_5_Parallel_R600_opt[60] - 0.37, eta_ttd_u_5_Parallel_R600_opt[60] - 0.3), fontsize='17')

plt.plot(data_ttd_u_10_Parallel_R600_opt[0], eta_ttd_u_10_Parallel_R600_opt[0], color='black', marker='x')
plt.annotate('160', xy=(data_ttd_u_10_Parallel_R600_opt[0] - 0.3, eta_ttd_u_10_Parallel_R600_opt[0] - 0.25), xytext=(data_ttd_u_10_Parallel_R600_opt[0] - 0.3, eta_ttd_u_10_Parallel_R600_opt[0] - 0.25), fontsize='17')
plt.plot(data_ttd_u_10_Parallel_R600_opt[20], eta_ttd_u_10_Parallel_R600_opt[20], color='black', marker='x')
plt.annotate('150', xy=(data_ttd_u_10_Parallel_R600_opt[20] - 0.18, eta_ttd_u_10_Parallel_R600_opt[20] - 0.37), xytext=(data_ttd_u_10_Parallel_R600_opt[20] - 0.18, eta_ttd_u_10_Parallel_R600_opt[20] - 0.37), fontsize='17')
plt.plot(data_ttd_u_10_Parallel_R600_opt[40], eta_ttd_u_10_Parallel_R600_opt[40], color='black', marker='x')
plt.annotate('140', xy=(data_ttd_u_10_Parallel_R600_opt[40] - 0.18, eta_ttd_u_10_Parallel_R600_opt[40] - 0.37), xytext=(data_ttd_u_10_Parallel_R600_opt[40] - 0.18, eta_ttd_u_10_Parallel_R600_opt[40] - 0.37), fontsize='17')
plt.plot(data_ttd_u_10_Parallel_R600_opt[60], eta_ttd_u_10_Parallel_R600_opt[60], color='black', marker='x')
plt.annotate('130', xy=(data_ttd_u_10_Parallel_R600_opt[60] - 0.34, eta_ttd_u_10_Parallel_R600_opt[60] - 0.3), xytext=(data_ttd_u_10_Parallel_R600_opt[60] - 0.34, eta_ttd_u_10_Parallel_R600_opt[60] - 0.3), fontsize='17')

plt.plot(data_ttd_u_15_Parallel_R600_opt[0], eta_ttd_u_15_Parallel_R600_opt[0], color='black', marker='x')
plt.annotate('160', xy=(data_ttd_u_15_Parallel_R600_opt[0] - 0.3, eta_ttd_u_15_Parallel_R600_opt[0] - 0.25), xytext=(data_ttd_u_15_Parallel_R600_opt[0] - 0.3, eta_ttd_u_15_Parallel_R600_opt[0] - 0.25), fontsize='17')
plt.plot(data_ttd_u_15_Parallel_R600_opt[20], eta_ttd_u_15_Parallel_R600_opt[20], color='black', marker='x')
plt.annotate('150', xy=(data_ttd_u_15_Parallel_R600_opt[20] - 0.27, eta_ttd_u_15_Parallel_R600_opt[20] - 0.35), xytext=(data_ttd_u_15_Parallel_R600_opt[20] - 0.27, eta_ttd_u_15_Parallel_R600_opt[20] - 0.35), fontsize='17')
plt.plot(data_ttd_u_15_Parallel_R600_opt[48], eta_ttd_u_15_Parallel_R600_opt[48], color='black', marker='x')
plt.annotate('140', xy=(data_ttd_u_15_Parallel_R600_opt[48] - 0.34, eta_ttd_u_15_Parallel_R600_opt[48] - 0.28), xytext=(data_ttd_u_15_Parallel_R600_opt[48] - 0.34, eta_ttd_u_15_Parallel_R600_opt[48] - 0.28), fontsize='17')
plt.plot(data_ttd_u_15_Parallel_R600_opt[68], eta_ttd_u_15_Parallel_R600_opt[68], color='black', marker='x')
plt.annotate('130', xy=(data_ttd_u_15_Parallel_R600_opt[68] - 0.3, eta_ttd_u_15_Parallel_R600_opt[68] - 0.32), xytext=(data_ttd_u_15_Parallel_R600_opt[68] - 0.3, eta_ttd_u_15_Parallel_R600_opt[68] - 0.32), fontsize='17')

plt.plot(data_ttd_u_20_Parallel_R600_opt[0], eta_ttd_u_20_Parallel_R600_opt[0], color='black', marker='x')
plt.annotate('160', xy=(data_ttd_u_20_Parallel_R600_opt[0] - 0.3, eta_ttd_u_20_Parallel_R600_opt[0] - 0.25), xytext=(data_ttd_u_20_Parallel_R600_opt[0] - 0.3, eta_ttd_u_20_Parallel_R600_opt[0] - 0.25), fontsize='17')
plt.plot(data_ttd_u_20_Parallel_R600_opt[20], eta_ttd_u_20_Parallel_R600_opt[20], color='black', marker='x')
plt.annotate('150', xy=(data_ttd_u_20_Parallel_R600_opt[20] - 0.27, eta_ttd_u_20_Parallel_R600_opt[20] - 0.33), xytext=(data_ttd_u_20_Parallel_R600_opt[20] - 0.27, eta_ttd_u_20_Parallel_R600_opt[20] - 0.33), fontsize='17')
plt.plot(data_ttd_u_20_Parallel_R600_opt[40], eta_ttd_u_20_Parallel_R600_opt[40], color='black', marker='x')
plt.annotate('140', xy=(data_ttd_u_20_Parallel_R600_opt[40] - 0.34, eta_ttd_u_20_Parallel_R600_opt[40] - 0.25), xytext=(data_ttd_u_20_Parallel_R600_opt[40] - 0.34, eta_ttd_u_20_Parallel_R600_opt[40] - 0.25), fontsize='17')


plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
plt.ylim(64.51, 73)
plt.legend(handles=[o_line, red_line, orange_line, green_line, blue_line], loc='upper center', ncol=7)
plt.grid()
plt.savefig('Senkeneintrittstemperatur Parallel R600 optimal.svg')
plt.show()

plt.plot(data_IHX_T160_R1336MZZZ, eta_IHX_T160_R1336MZZZ, color='black')
plt.annotate('160', xy=(35.05, 68.46), xytext=(35.05, 68.46))
plt.plot(data_IHX_T150_R1336MZZZ, eta_IHX_T150_R1336MZZZ, color='black', label='150°C IHX')
plt.annotate('150', xy=(40.05, 69.54), xytext=(40.05, 69.54))
plt.plot(data_IHX_T140_R1336MZZZ, eta_IHX_T140_R1336MZZZ,  color='black', label='140°C IHX')
plt.annotate('140', xy=(40.05, 70.9), xytext=(40.05, 70.9))
plt.plot(data_IHX_T130_R1336MZZZ, eta_IHX_T130_R1336MZZZ,  color='black', label='130°C IHX')
plt.annotate('130', xy=(40.05, 72.1), xytext=(40.05, 72.1))
plt.plot(data_IHX_T120_R1336MZZZ, eta_IHX_T120_R1336MZZZ,  color='black', label='120°C IHX')
plt.annotate('120', xy=(40.05, 73.22), xytext=(40.05, 73.22))

plt.plot(data_ttd_u_5_IHX_R1336MZZZ, eta_ttd_u_5_IHX_R1336MZZZ, linestyle='--', color='red')
plt.plot(data_ttd_u_10_IHX_R1336MZZZ, eta_ttd_u_10_IHX_R1336MZZZ, linestyle='--', color='orange')
plt.plot(data_ttd_u_15_IHX_R1336MZZZ, eta_ttd_u_15_IHX_R1336MZZZ, linestyle='--', color='green')
plt.plot(data_ttd_u_20_IHX_R1336MZZZ, eta_ttd_u_20_IHX_R1336MZZZ, linestyle='--', color='steelblue')
plt.plot(data_ttd_u_25_IHX_R1336MZZZ, eta_ttd_u_25_IHX_R1336MZZZ, linestyle='--', color='blueviolet')

plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
o_line = mlines.Line2D([], [], color='black', label=r'$T_{se,ein}$ [°C]          $ΔT_{GK,ob}$:')
s_line = mlines.Line2D([], [], color='black',  linestyle='--', label='ttd_gk,ob:')
red_line = mlines.Line2D([], [], color='red', linestyle='--', label='5 K')
orange_line = mlines.Line2D([], [], color='orange', linestyle='--', label='10 K')
green_line = mlines.Line2D([], [], color='green', linestyle='--', label='15 K')
blue_line = mlines.Line2D([], [], color='steelblue', linestyle='--', label='20 K')
black_line = mlines.Line2D([], [], color='blueviolet', linestyle='--', label='25 K')
plt.xlim(24, 41)
plt.legend(handles=[o_line, red_line, orange_line, green_line, blue_line, black_line], loc='lower center', fontsize='16', ncol=7)
plt.grid()
plt.savefig('Senkeneintrittstemperatur IWUE R1336MZZ(Z).svg')
plt.show()



plt.plot(data_Parallel_T160_R1336MZZZ, eta_Parallel_T160_R1336MZZZ, color='black', label='160°C Parallel')
plt.annotate('160', xy=(46.05, 69.1), xytext=(46.05, 69.1))
plt.plot(data_Parallel_T150_R1336MZZZ, eta_Parallel_T150_R1336MZZZ, color='black', label='150°C Parallel')
plt.annotate('150', xy=(46.05, 70.43), xytext=(46.05, 70.43))
plt.plot(data_Parallel_T140_R1336MZZZ, eta_Parallel_T140_R1336MZZZ, color='black', label='140°C Parallel')
plt.annotate('140', xy=(46.05, 71.56), xytext=(46.05, 71.56))
plt.plot(data_Parallel_T130_R1336MZZZ, eta_Parallel_T130_R1336MZZZ, color='black', label='130°C Parallel')
plt.annotate('130', xy=(46.05, 72.68), xytext=(46.05, 72.68))

plt.plot(data_ttd_u_5_Parallel_R1336MZZZ, eta_ttd_u_5_Parallel_R1336MZZZ, linestyle='--', color='red')
plt.plot(data_ttd_u_10_Parallel_R1336MZZZ, eta_ttd_u_10_Parallel_R1336MZZZ, linestyle='--', color='orange')
plt.plot(data_ttd_u_15_Parallel_R1336MZZZ, eta_ttd_u_15_Parallel_R1336MZZZ, linestyle='--', color='green')
plt.plot(data_ttd_u_20_Parallel_R1336MZZZ, eta_ttd_u_20_Parallel_R1336MZZZ, linestyle='--', color='steelblue')

plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')

plt.legend(handles=[o_line, red_line, orange_line, green_line, blue_line], loc='upper center', fontsize='16', ncol=7)
plt.xlim(30.01, 47)
plt.ylim(69, 75)
plt.grid()
plt.savefig('Senkeneintrittstemperatur Parallel R1336MZZ(Z).svg')
plt.show()

plt.plot(data_Parallel_T160_R1336MZZZ_opt, eta_Parallel_T160_R1336MZZZ_opt, color='black', label='160°C Parallel')
plt.annotate('160', xy=(46.05, 69.06), xytext=(46.05, 69.06))
plt.plot(data_Parallel_T150_R1336MZZZ_opt, eta_Parallel_T150_R1336MZZZ_opt, color='black', label='150°C Parallel')
plt.annotate('150', xy=(46.05, 70.13), xytext=(46.05, 70.13))
plt.plot(data_Parallel_T140_R1336MZZZ_opt, eta_Parallel_T140_R1336MZZZ_opt, color='black', label='140°C Parallel')
plt.annotate('140', xy=(46.05, 71.26), xytext=(46.05, 71.26))
plt.plot(data_Parallel_T130_R1336MZZZ_opt, eta_Parallel_T130_R1336MZZZ_opt, color='black', label='130°C Parallel')
plt.annotate('130', xy=(46.05, 72.54), xytext=(46.05, 72.54))

plt.plot(data_ttd_u_5_Parallel_R1336MZZZ_opt, eta_ttd_u_5_Parallel_R1336MZZZ_opt, linestyle='--', color='red')
plt.plot(data_ttd_u_10_Parallel_R1336MZZZ_opt, eta_ttd_u_10_Parallel_R1336MZZZ_opt, linestyle='--', color='orange')
plt.plot(data_ttd_u_15_Parallel_R1336MZZZ_opt, eta_ttd_u_15_Parallel_R1336MZZZ_opt, linestyle='--', color='green')
plt.plot(data_ttd_u_20_Parallel_R1336MZZZ_opt, eta_ttd_u_20_Parallel_R1336MZZZ_opt, linestyle='--', color='steelblue')

plt.plot(data_ttd_u_5_Parallel_R1336MZZZ_opt[0], eta_ttd_u_5_Parallel_R1336MZZZ_opt[0], color='black', marker='x')
plt.annotate('160', xy=(data_ttd_u_5_Parallel_R1336MZZZ_opt[0] - 0.22, eta_ttd_u_5_Parallel_R1336MZZZ_opt[0] - 0.24), xytext=(data_ttd_u_5_Parallel_R1336MZZZ_opt[0] - 0.22, eta_ttd_u_5_Parallel_R1336MZZZ_opt[0] - 0.24), fontsize='17')
plt.plot(data_ttd_u_5_Parallel_R1336MZZZ_opt[20], eta_ttd_u_5_Parallel_R1336MZZZ_opt[20], color='black', marker='x')
plt.annotate('150', xy=(data_ttd_u_5_Parallel_R1336MZZZ_opt[20] - 0.1, eta_ttd_u_5_Parallel_R1336MZZZ_opt[20] - 0.32), xytext=(data_ttd_u_5_Parallel_R1336MZZZ_opt[20] - 0.1, eta_ttd_u_5_Parallel_R1336MZZZ_opt[20] - 0.32), fontsize='17')
plt.plot(data_ttd_u_5_Parallel_R1336MZZZ_opt[40], eta_ttd_u_5_Parallel_R1336MZZZ_opt[40], color='black', marker='x')
plt.annotate('140', xy=(data_ttd_u_5_Parallel_R1336MZZZ_opt[40] - 0.19, eta_ttd_u_5_Parallel_R1336MZZZ_opt[40] - 0.25), xytext=(data_ttd_u_5_Parallel_R1336MZZZ_opt[40] - 0.19, eta_ttd_u_5_Parallel_R1336MZZZ_opt[40] - 0.25), fontsize='17')
plt.plot(data_ttd_u_5_Parallel_R1336MZZZ_opt[60], eta_ttd_u_5_Parallel_R1336MZZZ_opt[60], color='black', marker='x')
plt.annotate('130', xy=(data_ttd_u_5_Parallel_R1336MZZZ_opt[60] - 0.39, eta_ttd_u_5_Parallel_R1336MZZZ_opt[60] - 0.25), xytext=(data_ttd_u_5_Parallel_R1336MZZZ_opt[60] - 0.39, eta_ttd_u_5_Parallel_R1336MZZZ_opt[60] - 0.25), fontsize='17')

plt.plot(data_ttd_u_10_Parallel_R1336MZZZ_opt[0], eta_ttd_u_10_Parallel_R1336MZZZ_opt[0], color='black', marker='x')
plt.annotate('160', xy=(data_ttd_u_10_Parallel_R1336MZZZ_opt[0] - 0.3, eta_ttd_u_10_Parallel_R1336MZZZ_opt[0] - 0.25), xytext=(data_ttd_u_10_Parallel_R1336MZZZ_opt[0] - 0.3, eta_ttd_u_10_Parallel_R1336MZZZ_opt[0] - 0.25), fontsize='17')
plt.plot(data_ttd_u_10_Parallel_R1336MZZZ_opt[20], eta_ttd_u_10_Parallel_R1336MZZZ_opt[20], color='black', marker='x')
plt.annotate('150', xy=(data_ttd_u_10_Parallel_R1336MZZZ_opt[20] - 0.17, eta_ttd_u_10_Parallel_R1336MZZZ_opt[20] - 0.3), xytext=(data_ttd_u_10_Parallel_R1336MZZZ_opt[20] - 0.17, eta_ttd_u_10_Parallel_R1336MZZZ_opt[20] - 0.3), fontsize='17')
plt.plot(data_ttd_u_10_Parallel_R1336MZZZ_opt[56], eta_ttd_u_10_Parallel_R1336MZZZ_opt[56], color='black', marker='x')
plt.annotate('140', xy=(data_ttd_u_10_Parallel_R1336MZZZ_opt[56] - 0.2, eta_ttd_u_10_Parallel_R1336MZZZ_opt[56] - 0.25), xytext=(data_ttd_u_10_Parallel_R1336MZZZ_opt[56] - 0.2, eta_ttd_u_10_Parallel_R1336MZZZ_opt[56] - 0.25), fontsize='17')
plt.plot(data_ttd_u_10_Parallel_R1336MZZZ_opt[76], eta_ttd_u_10_Parallel_R1336MZZZ_opt[76], color='black', marker='x')
plt.annotate('130', xy=(data_ttd_u_10_Parallel_R1336MZZZ_opt[76] - 0.34, eta_ttd_u_10_Parallel_R1336MZZZ_opt[76] - 0.25), xytext=(data_ttd_u_10_Parallel_R1336MZZZ_opt[76] - 0.34, eta_ttd_u_10_Parallel_R1336MZZZ_opt[76] - 0.25), fontsize='17')

plt.plot(data_ttd_u_15_Parallel_R1336MZZZ_opt[0], eta_ttd_u_15_Parallel_R1336MZZZ_opt[0], color='black', marker='x')
plt.annotate('160', xy=(data_ttd_u_15_Parallel_R1336MZZZ_opt[0] - 0.3, eta_ttd_u_15_Parallel_R1336MZZZ_opt[0] - 0.25), xytext=(data_ttd_u_15_Parallel_R1336MZZZ_opt[0] - 0.3, eta_ttd_u_15_Parallel_R1336MZZZ_opt[0] - 0.25), fontsize='17')
plt.plot(data_ttd_u_15_Parallel_R1336MZZZ_opt[20], eta_ttd_u_15_Parallel_R1336MZZZ_opt[20], color='black', marker='x')
plt.annotate('150', xy=(data_ttd_u_15_Parallel_R1336MZZZ_opt[20] - 0.22, eta_ttd_u_15_Parallel_R1336MZZZ_opt[20] - 0.26), xytext=(data_ttd_u_15_Parallel_R1336MZZZ_opt[20] - 0.22, eta_ttd_u_15_Parallel_R1336MZZZ_opt[20] - 0.26), fontsize='17')
plt.plot(data_ttd_u_15_Parallel_R1336MZZZ_opt[56], eta_ttd_u_15_Parallel_R1336MZZZ_opt[56], color='black', marker='x')
plt.annotate('140', xy=(data_ttd_u_15_Parallel_R1336MZZZ_opt[56] - 0.3, eta_ttd_u_15_Parallel_R1336MZZZ_opt[56] - 0.23), xytext=(data_ttd_u_15_Parallel_R1336MZZZ_opt[56] - 0.3, eta_ttd_u_15_Parallel_R1336MZZZ_opt[56] - 0.23), fontsize='17')

plt.plot(data_ttd_u_20_Parallel_R1336MZZZ_opt[0], eta_ttd_u_20_Parallel_R1336MZZZ_opt[0], color='black', marker='x')
plt.annotate('160', xy=(data_ttd_u_20_Parallel_R1336MZZZ_opt[0] - 0.3, eta_ttd_u_20_Parallel_R1336MZZZ_opt[0] - 0.25), xytext=(data_ttd_u_20_Parallel_R1336MZZZ_opt[0] - 0.3, eta_ttd_u_20_Parallel_R1336MZZZ_opt[0] - 0.25), fontsize='17')
plt.plot(data_ttd_u_20_Parallel_R1336MZZZ_opt[20], eta_ttd_u_20_Parallel_R1336MZZZ_opt[20], color='black', marker='x')
plt.annotate('150', xy=(data_ttd_u_20_Parallel_R1336MZZZ_opt[20] - 0.24, eta_ttd_u_20_Parallel_R1336MZZZ_opt[20] - 0.28), xytext=(data_ttd_u_20_Parallel_R1336MZZZ_opt[20] - 0.24, eta_ttd_u_20_Parallel_R1336MZZZ_opt[20] - 0.28), fontsize='17')

plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
plt.xlim(30.01, 47)
plt.ylim(69, 75)
plt.legend(handles=[o_line, red_line, orange_line, green_line, blue_line], loc='lower center', fontsize='16', ncol=7)
plt.grid()
plt.savefig('Senkeneintrittstemperatur Parallel R1336MZZ(Z) optimal.svg')
plt.show()

plt.plot(data_IHX_T160_R601, eta_IHX_T160_R601, color='black', label='160°C IHX')
plt.annotate('160', xy=(40.05, 68.65), xytext=(40.05, 68.65))
plt.plot(data_IHX_T150_R601, eta_IHX_T150_R601, color='black', label='150°C IHX')
plt.annotate('150', xy=(40.05, 69.48), xytext=(40.05, 69.48))
plt.plot(data_IHX_T140_R601, eta_IHX_T140_R601,  color='black', label=' 140°C IHX')
plt.annotate('140', xy=(40.05, 70.19), xytext=(40.05, 70.19))
plt.plot(data_IHX_T130_R601, eta_IHX_T130_R601,  color='black', label='130°C IHX')
plt.annotate('130', xy=(40.05, 70.85), xytext=(40.05, 70.85))
plt.plot(data_IHX_T120_R601, eta_IHX_T120_R601,  color='black', label='120°C IHX')
plt.annotate('120', xy=(40.05, 71.57), xytext=(40.05, 71.57))
plt.plot(data_ttd_u_5_IHX_R601, eta_ttd_u_5_IHX_R601, linestyle='--', color='red')
plt.plot(data_ttd_u_10_IHX_R601, eta_ttd_u_10_IHX_R601, linestyle='--', color='orange')
plt.plot(data_ttd_u_15_IHX_R601, eta_ttd_u_15_IHX_R601, linestyle='--', color='green')
plt.plot(data_ttd_u_20_IHX_R601, eta_ttd_u_20_IHX_R601, linestyle='--', color='steelblue')
plt.plot(data_ttd_u_25_IHX_R601, eta_ttd_u_25_IHX_R601, linestyle='--', color='blueviolet')

plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
plt.xlim(24, 41)
plt.legend(handles=[o_line, red_line, orange_line, green_line, blue_line, black_line], loc='upper center', ncol=7)
plt.grid()
plt.savefig('Senkeneintrittstemperatur IWUE R601.svg')
plt.show()

plt.plot(data_Parallel_T160_R601, eta_Parallel_T160_R601, color='black', label='160°C IHX')
plt.annotate('160', xy=(40.05, 70.70), xytext=(40.05, 70.70))
plt.plot(data_Parallel_T155_R601, eta_Parallel_T155_R601, color='black', label='150°C IHX')
plt.annotate('155', xy=(40.05, 71.00), xytext=(40.05, 71.00))
plt.plot(data_Parallel_T150_R601, eta_Parallel_T150_R601,  color='black', label=' 140°C IHX')
plt.annotate('150', xy=(40.05, 71.25), xytext=(40.05, 71.25))
plt.plot(data_ttd_u_5_Parallel_R601, eta_ttd_u_5_Parallel_R601, linestyle='--', color='red')
plt.plot(data_ttd_u_10_Parallel_R601, eta_ttd_u_10_Parallel_R601, linestyle='--', color='orange')
plt.plot(data_ttd_u_15_Parallel_R601, eta_ttd_u_15_Parallel_R601, linestyle='--', color='green')
plt.plot(data_ttd_u_20_Parallel_R601, eta_ttd_u_20_Parallel_R601, linestyle='--', color='steelblue')

plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
plt.legend(handles=[o_line, red_line, orange_line, green_line, blue_line], loc='upper center', ncol=7)
plt.grid()
plt.savefig('Senkeneintrittstemperatur Parallel R601.svg')
plt.show()

plt.plot(data_Parallel_T160_R601_opt, eta_Parallel_T160_R601_opt, color='black', label='160°C IHX')
plt.annotate('160', xy=(37.55, 70.78), xytext=(37.55, 70.78))
plt.plot(data_Parallel_T155_R601_opt, eta_Parallel_T155_R601_opt, color='black', label='150°C IHX')
plt.annotate('155', xy=(37.6, 71.16), xytext=(37.6, 71.16))
plt.plot(data_Parallel_T150_R601_opt, eta_Parallel_T150_R601_opt,  color='black', label=' 140°C IHX')
plt.annotate('150', xy=(37.6, 71.50), xytext=(37.6, 71.50))
plt.plot(data_ttd_u_5_Parallel_R601_opt, eta_ttd_u_5_Parallel_R601_opt, linestyle='--', color='red')
plt.plot(data_ttd_u_10_Parallel_R601_opt, eta_ttd_u_10_Parallel_R601_opt, linestyle='--', color='orange')
plt.plot(data_ttd_u_15_Parallel_R601_opt, eta_ttd_u_15_Parallel_R601_opt, linestyle='--', color='green')
plt.plot(data_ttd_u_20_Parallel_R601_opt, eta_ttd_u_20_Parallel_R601_opt, linestyle='--', color='steelblue')

plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
plt.xlim(22, 38.3)
plt.legend(handles=[o_line, red_line, orange_line, green_line, blue_line], loc='upper center', ncol=7)
plt.grid()
plt.savefig('Senkeneintrittstemperatur Parallel R601 optimal.svg')
plt.show()



