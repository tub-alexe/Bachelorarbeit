from tespy.networks import Network
from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink)
from tespy.connections import Connection, Bus
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
from fluprodia import FluidPropertyDiagram
import math
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
from numpy import *


# importing the module
import json

with open('Einfacher Kreislauf mit IHX\Senkentemperatur.txt') as f:
    read = f.readlines()

data_IHX_T160_R1336MZZZ = json.loads(read[1])
COP_IHX_T160_R1336MZZZ = json.loads(read[2])
eta_IHX_T160_R1336MZZZ = json.loads(read[3])

data_IHX_T150_R1336MZZZ = json.loads(read[5])
COP_IHX_T150_R1336MZZZ = json.loads(read[6])
eta_IHX_T150_R1336MZZZ = json.loads(read[7])

data_IHX_T140_R1336MZZZ = json.loads(read[9])
COP_IHX_T140_R1336MZZZ = json.loads(read[10])
eta_IHX_T140_R1336MZZZ = json.loads(read[11])

data_IHX_T130_R1336MZZZ = json.loads(read[13])
COP_IHX_T130_R1336MZZZ = json.loads(read[14])
eta_IHX_T130_R1336MZZZ = json.loads(read[15])

data_IHX_T120_R1336MZZZ = json.loads(read[17])
COP_IHX_T120_R1336MZZZ = json.loads(read[18])
eta_IHX_T120_R1336MZZZ = json.loads(read[19])

data_IHX_T160_R1233ZDE = json.loads(read[21])
COP_IHX_T160_R1233ZDE = json.loads(read[22])
eta_IHX_T160_R1233ZDE = json.loads(read[23])

data_IHX_T150_R1233ZDE = json.loads(read[25])
COP_IHX_T150_R1233ZDE = json.loads(read[26])
eta_IHX_T150_R1233ZDE = json.loads(read[27])

data_IHX_T140_R1233ZDE = json.loads(read[29])
COP_IHX_T140_R1233ZDE = json.loads(read[30])
eta_IHX_T140_R1233ZDE = json.loads(read[31])

data_IHX_T130_R1233ZDE = json.loads(read[33])
COP_IHX_T130_R1233ZDE = json.loads(read[34])
eta_IHX_T130_R1233ZDE = json.loads(read[35])

data_IHX_T120_R1233ZDE = json.loads(read[37])
COP_IHX_T120_R1233ZDE = json.loads(read[38])
eta_IHX_T120_R1233ZDE = json.loads(read[39])

data_ttd_u_5_IHX_R1233ZDE = json.loads(read[41])
eta_ttd_u_5_IHX_R1233ZDE = json.loads(read[42])

data_ttd_u_10_IHX_R1233ZDE = json.loads(read[44])
eta_ttd_u_10_IHX_R1233ZDE = json.loads(read[45])

data_ttd_u_15_IHX_R1233ZDE = json.loads(read[47])
eta_ttd_u_15_IHX_R1233ZDE = json.loads(read[48])

data_ttd_u_20_IHX_R1233ZDE = json.loads(read[50])
eta_ttd_u_20_IHX_R1233ZDE = json.loads(read[51])

data_ttd_u_25_IHX_R1233ZDE = json.loads(read[53])
eta_ttd_u_25_IHX_R1233ZDE = json.loads(read[54])


with open('Parallelkompression\Senkentemperatur.txt') as f:
    read = f.readlines()

data_Parallel_T160_R1336MZZZ = json.loads(read[1])
COP_Parallel_T160_R1336MZZZ = json.loads(read[2])
eta_Parallel_T160_R1336MZZZ = json.loads(read[3])

data_Parallel_T150_R1336MZZZ = json.loads(read[5])
COP_Parallel_T150_R1336MZZZ = json.loads(read[6])
eta_Parallel_T150_R1336MZZZ = json.loads(read[7])

data_Parallel_T140_R1336MZZZ = json.loads(read[9])
COP_Parallel_T140_R1336MZZZ = json.loads(read[10])
eta_Parallel_T140_R1336MZZZ = json.loads(read[11])

data_Parallel_T130_R1336MZZZ = json.loads(read[13])
COP_Parallel_T130_R1336MZZZ = json.loads(read[14])
eta_Parallel_T130_R1336MZZZ = json.loads(read[15])

data_Parallel_T160_R1233ZDE = json.loads(read[17])
COP_Parallel_T160_R1233ZDE = json.loads(read[18])
eta_Parallel_T160_R1233ZDE = json.loads(read[19])

data_Parallel_T150_R1233ZDE = json.loads(read[21])
COP_Parallel_T150_R1233ZDE = json.loads(read[22])
eta_Parallel_T150_R1233ZDE = json.loads(read[23])

data_Parallel_T140_R1233ZDE = json.loads(read[25])
COP_Parallel_T140_R1233ZDE = json.loads(read[26])
eta_Parallel_T140_R1233ZDE = json.loads(read[27])

data_Parallel_T130_R1233ZDE = json.loads(read[29])
COP_Parallel_T130_R1233ZDE = json.loads(read[30])
eta_Parallel_T130_R1233ZDE = json.loads(read[31])

plt.rc('font', **{'size': 20})
plt.rcParams["figure.figsize"] = (20, 13)

plt.plot(data_IHX_T160_R1336MZZZ, eta_IHX_T160_R1336MZZZ, marker='o', color='red')
plt.plot(data_IHX_T150_R1336MZZZ, eta_IHX_T150_R1336MZZZ, marker='o', color='orange', label='150°C IHX')
plt.plot(data_IHX_T140_R1336MZZZ, eta_IHX_T140_R1336MZZZ, marker='o',  color='green', label='140°C IHX')
plt.plot(26.13, 75.67, color='black', marker='x', markersize=12)
plt.plot(data_IHX_T130_R1336MZZZ, eta_IHX_T130_R1336MZZZ, marker='o',  color='steelblue', label='130°C IHX')
plt.plot(31.05, 74.81, color='black', marker='x', markersize=12)
plt.plot(data_IHX_T120_R1336MZZZ, eta_IHX_T120_R1336MZZZ, marker='o',  color='blueviolet', label='120°C IHX')
plt.plot(35.34, 74.51, color='black', marker='x', markersize=12)
#plt.plot(data_Parallel_T160_R1336MZZZ, eta_Parallel_T160_R1336MZZZ, marker='s', color='red', label='160°C Parallel')
#plt.plot(32.78, 72.59, color='black', marker='x', markersize=12)
#plt.plot(data_Parallel_T150_R1336MZZZ, eta_Parallel_T150_R1336MZZZ, marker='s', color='orange', label='150°C Parallel')
#plt.plot(34.98, 73.25, color='black', marker='x', markersize=12)
#plt.plot(data_Parallel_T140_R1336MZZZ, eta_Parallel_T140_R1336MZZZ, marker='s', color='green', label='140°C Parallel')
#plt.plot(37.26, 73.62, color='black', marker='x', markersize=12)
#plt.plot(data_Parallel_T130_R1336MZZZ, eta_Parallel_T130_R1336MZZZ, marker='s', color='steelblue', label='130°C Parallel')
#plt.plot(39.62, 74.05, color='black', marker='x', markersize=12)
plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('exergetischer Wirkungsgrad')
#plt.legend(loc='upper right', fontsize='13')
o_line = mlines.Line2D([], [], color='red', marker='o',
                          markersize=5, label='mit IWÜ')
s_line = mlines.Line2D([], [], color='red', marker='s',
                          markersize=5, label='mit IWÜ und PK')
red_line = mlines.Line2D([], [], color='red', label='160°C')
yellow_line = mlines.Line2D([], [], color='orange', label='150°C')
green_line = mlines.Line2D([], [], color='green', label='140°C')
blue_line = mlines.Line2D([], [], color='steelblue', label='130°C')

black_line = mlines.Line2D([], [], color='blueviolet', label='120°C')
plt.legend(handles=[o_line, s_line, red_line, yellow_line, green_line, blue_line, black_line], loc='upper right', fontsize='16')
plt.grid()
plt.show()
plt.savefig('Senkentemperatur.svg')


ttd_u_5_p = [39.3, 39.07, 38.91, 38.81, 38.77, 38.76, 38.82, 38.99, 39.19, 39.39, 39.855, 40.09, 40.33, 40.82, 41.33, 41.84, 42.37, 43.44, 45.1]
ttd_u_5_eta = [71.78, 72.53, 73.10, 73.51, 73.83, 73.96, 74.07, 74.24, 74.36, 74.44, 74.55, 74.58, 74.61, 74.63, 74.63, 74.62, 74.6, 74.56, 74.47]

ttd_u_10_p = [41.50, 41.47, 41.48, 41.50, 41.55, 41.58, 41.70, 41.97, 42.24, 42.50, 43.04, 43.30, 43.57, 44.11, 44.66, 45.21, 45.77, 46.91, 48.69]
ttd_u_10_eta = [72.01, 72.32, 72.58, 72.79, 72.97, 73.04, 73.11, 73.21, 73.28, 73.34, 73.41, 73.44, 73.46, 73.5, 73.51, 73.52, 73.52, 73.51, 73.49]

ttd_u_15_p = [44.36, 44.42, 44.49, 44.57, 44.68, 44.73, 44.89, 45.23, 45.56, 45.86, 46.48, 46.77, 47.07, 47.65, 48.25, 48.85, 49.45, 50.69, 52.64]
ttd_u_15_eta = [71.42, 71.60, 71.76, 71.90, 72.02, 72.08, 72.12, 72.19, 72.25, 72.29, 72.36, 72.39, 72.41, 72.45, 72.48, 72.50, 72.52, 72.54, 72.55]

ttd_u_20_p = [47.63, 47.73, 47.84, 47.96, 48.10, 48.17, 48.36, 48.77, 49.15, 49.51, 50.19, 50.52, 50.85, 51.49, 52.15, 52.80, 53.13, 54.83]
ttd_u_20_eta = [70.64, 70.77, 70.89, 70.99, 71.09, 71.13, 71.17, 71.23, 71.28, 71.32, 71.38, 71.41, 71.44, 71.48, 71.52, 71.55, 71.57, 71.61]

plt.plot(data_IHX_T160_R1233ZDE, eta_IHX_T160_R1233ZDE, color='black', label='160°C IHX')
plt.annotate('160', xy=(54.1, 66.68), xytext=(54.1, 66.68))
plt.plot(data_IHX_T150_R1233ZDE, eta_IHX_T150_R1233ZDE, color='black', label='150°C IHX')
plt.annotate('150', xy=(54.1, 68.27), xytext=(54.1, 68.27))
plt.plot(data_IHX_T140_R1233ZDE, eta_IHX_T140_R1233ZDE,  color='black', label=' 140°C IHX')
plt.annotate('140', xy=(54.1, 69.46), xytext=(54.1, 69.46))
plt.plot(data_IHX_T130_R1233ZDE, eta_IHX_T130_R1233ZDE,  color='black', label='130°C IHX')
plt.annotate('130', xy=(54.1, 70.46), xytext=(54.1, 70.46))
#plt.plot(33.165, 77.17, color='black', marker='x', markersize=12)
plt.plot(data_IHX_T120_R1233ZDE, eta_IHX_T120_R1233ZDE,  color='black', label='120°C IHX')
plt.annotate('120', xy=(54.1, 70.32), xytext=(54.1, 71.32))
#plt.plot(38.37, 75.84, color='black', marker='x', markersize=12)
plt.plot(data_ttd_u_5_IHX_R1233ZDE, eta_ttd_u_5_IHX_R1233ZDE, linestyle='--', color='red')
plt.plot(data_ttd_u_10_IHX_R1233ZDE, eta_ttd_u_10_IHX_R1233ZDE, linestyle='--', color='orange')
plt.plot(data_ttd_u_15_IHX_R1233ZDE, eta_ttd_u_15_IHX_R1233ZDE, linestyle='--', color='green')
plt.plot(data_ttd_u_20_IHX_R1233ZDE, eta_ttd_u_20_IHX_R1233ZDE, linestyle='--', color='steelblue')
plt.plot(data_ttd_u_25_IHX_R1233ZDE, eta_ttd_u_25_IHX_R1233ZDE, linestyle='--', color='blueviolet')

#plt.plot(data_Parallel_T160_R1233ZDE, eta_Parallel_T160_R1233ZDE, color='black', label='160°C Parallel')
#plt.annotate('160', xy=(54.1, 69.15), xytext=(54.1, 69.15))
#plt.plot(41.55, 72.97, color='black', marker='x', markersize=12)
#plt.plot(41.7, 73.11, color='black', marker='x', markersize=12)

#plt.plot(39.3, 71.78, color='black', marker='x', markersize=12)
#plt.plot(39.44, 71.81, color='black', marker='x', markersize=12) #bei Maximumsuche am unteren Ende
#plt.plot(39.07, 72.53, color='black', marker='x', markersize=12) #159
#plt.plot(38.91, 73.10, color='black', marker='x', markersize=12) #158
#plt.plot(38.81, 73.51, color='black', marker='x', markersize=12) #157
#plt.plot(38.77, 73.83, color='black', marker='x', markersize=12) #156
#plt.plot(38.82, 74.07, color='black', marker='x', markersize=12) #155
#plt.plot(38.99, 74.24, color='black', marker='x', markersize=12) #154
#plt.plot(39.19, 74.36, color='black', marker='x', markersize=12) #153
#plt.plot(39.39, 74.44, color='black', marker='x', markersize=12) #152
#plt.plot(40.09, 74.58, color='black', marker='x', markersize=12) #149
#plt.plot(40.33, 74.61, color='black', marker='x', markersize=12) #148
#plt.plot(40.82, 74.63, color='black', marker='x', markersize=12) #146
#plt.plot(41.33, 74.63, color='black', marker='x', markersize=12) #144
#plt.plot(41.84, 74.62, color='black', marker='x', markersize=12) #142
#plt.plot(43.44, 74.56, color='black', marker='x', markersize=12) #136
#plt.plot(data_Parallel_T150_R1233ZDE, eta_Parallel_T150_R1233ZDE, color='black', label='150°C Parallel')
#plt.annotate('150', xy=(54.1, 70.41), xytext=(54.1, 70.41))
#plt.plot(39.855, 74.55, color='black', marker='x', markersize=12)
#plt.plot(data_Parallel_T140_R1233ZDE, eta_Parallel_T140_R1233ZDE, color='black', label='140°C Parallel')
#plt.annotate('140', xy=(54.1, 71.35), xytext=(54.1, 71.35))
#plt.plot(42.37, 74.6, color='black', marker='x', markersize=12)
#plt.plot(data_Parallel_T130_R1233ZDE, eta_Parallel_T130_R1233ZDE, color='black', label='130°C Parallel')
#plt.annotate('130', xy=(54.1, 72.15), xytext=(54.1, 72.15))
#plt.plot(45.1, 74.47, color='black', marker='x', markersize=12)
#plt.plot(ttd_u_5_p, ttd_u_5_eta, color='red', linestyle='--')
#plt.plot(ttd_u_10_p, ttd_u_10_eta, color='orange', linestyle='--')
#plt.plot(ttd_u_15_p, ttd_u_15_eta, color='green', linestyle='--')
#plt.plot(ttd_u_20_p, ttd_u_20_eta, color='steelblue', linestyle='--')
plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
o_line = mlines.Line2D([], [], color='black', label=r'$T_{se,ein}$ [C]          $ttd_{gk,ob}$:')
s_line = mlines.Line2D([], [], color='black',  linestyle='--', label='ttd_gk,ob:')
red_line = mlines.Line2D([], [], color='red', linestyle='--', label='5 K')
yellow_line = mlines.Line2D([], [], color='orange', linestyle='--', label='10 K')
green_line = mlines.Line2D([], [], color='green', linestyle='--', label='15 K')
blue_line = mlines.Line2D([], [], color='steelblue', linestyle='--', label='20 K')
black_line = mlines.Line2D([], [], color='blueviolet', linestyle='--', label='25 K')
plt.legend(handles=[o_line, red_line, yellow_line, green_line, blue_line, black_line], loc='lower center', ncol=7)
#plt.legend(loc='lower left')
plt.ylim(65, 78)
plt.xlim(30, 55)
plt.grid()
plt.savefig('Senkeneintrittstemperatur IWUE R1233ZD(E).svg')
#plt.savefig('Senkeneintrittstemperatur Parallel R1233ZD(E).svg')
plt.show()


