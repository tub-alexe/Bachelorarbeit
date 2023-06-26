from tespy.networks import Network
from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink)
from tespy.connections import Connection, Bus
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
from fluprodia import FluidPropertyDiagram
import math
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
from numpy import *


# importing the module
import json

# reading the data from the file
with open('Zwischendruck.txt') as f:
    read = f.readlines()

data_zw8 = json.loads(read[1])
COP_zw8 = json.loads(read[2])
eta_zw8 = json.loads(read[3])

data_zw11 = json.loads(read[5])
COP_zw11 = json.loads(read[6])
eta_zw11 = json.loads(read[7])

data_zw15 = json.loads(read[9])
COP_zw15 = json.loads(read[10])
eta_zw15 = json.loads(read[11])

data_zw19 = json.loads(read[13])
COP_zw19 = json.loads(read[14])
eta_zw19 = json.loads(read[15])

data_ttd_u_3 = json.loads(read[21])
eta_ttd_u_3 = json.loads(read[22])

data_ttd_u_5 = json.loads(read[24])
eta_ttd_u_5 = json.loads(read[25])

data_ttd_u_7 = json.loads(read[27])
eta_ttd_u_7 = json.loads(read[28])

data_ttd_u_10 = json.loads(read[30])
eta_ttd_u_10 = json.loads(read[31])

data_ttd_u_15 = json.loads(read[33])
eta_ttd_u_15 = json.loads(read[34])

data_ttd_u_20 = json.loads(read[36])
eta_ttd_u_20 = json.loads(read[37])

plt.rc('font', **{'size': 20})
plt.rcParams["figure.figsize"] = (20, 12)

plt.plot(data_zw8, eta_zw8, color='black', label='Zwischendruck 8 bar')
plt.annotate('8', xy=(30.5, 66.01), xytext=(30.5, 66.01))
#plt.plot(34.12, 65.99, color='black', marker='x', markersize=12)
plt.plot(data_zw11, eta_zw11, color='black', label='Zwischendruck 11 bar')
plt.annotate('11', xy=(30.8, 69.79), xytext=(30.8, 69.79))
#plt.plot(34.27, 69.4, color='black', marker='x', markersize=12)
plt.plot(data_zw15, eta_zw15, color='black', label='Zwischendruck 15 bar')
plt.annotate('15', xy=(30.4, 72.59), xytext=(30.4, 72.59))
#plt.plot(33.68, 71.9, color='black', marker='x', markersize=12)
plt.plot(data_zw19, eta_zw19, color='black', label='Zwischendruck 18,16 bar')
plt.annotate('18,16', xy=(30.1, 73.52), xytext=(30.1, 73.52))
#plt.plot(32.775, 72.59, color='black', marker='x', markersize=12)
#plt.plot(data_ttd_u_3, eta_ttd_u_3, linestyle='--', color='red')
plt.plot(data_ttd_u_5, eta_ttd_u_5, linestyle='--', color='red')
plt.plot(data_ttd_u_10, eta_ttd_u_10, linestyle='--', color='orange')
plt.plot(data_ttd_u_15, eta_ttd_u_15, linestyle='--', color='green')
plt.plot(data_ttd_u_20, eta_ttd_u_20, linestyle='--', color='steelblue')

'ttd_u=5'
plt.plot(data_ttd_u_5[0], eta_ttd_u_5[0], color='black', marker='x', markersize=12)
plt.annotate('8', xy=(33.9, 66.09), xytext=(33.9, 66.09))
plt.plot(34.27, 69.40, color='black', marker='x', markersize=12)
plt.annotate('11', xy=(33.85, 69.15), xytext=(33.85, 69.15))
plt.plot(33.68, 71.90, color='black', marker='x', markersize=12)
plt.annotate('15', xy=(33.25, 71.65), xytext=(33.25, 71.65))
plt.plot(32.78, 72.59, color='black', marker='x', markersize=12)
plt.annotate('18,16', xy=(32.74, 72.7), xytext=(32.74, 72.7))
'ttd_u=10'
plt.plot(data_ttd_u_10[0], eta_ttd_u_10[0], color='black', marker='x', markersize=12)
plt.annotate('8', xy=(37.3, 65.71), xytext=(37.3, 65.71))
plt.plot(37.59, 68.79, color='black', marker='x', markersize=12)
plt.annotate('11', xy=(37.1, 68.59), xytext=(37.1, 68.59))
plt.plot(36.82, 71.05, color='black', marker='x', markersize=12)
plt.annotate('15', xy=(36.4, 70.80), xytext=(36.4, 70.80))
plt.plot(35.69, 71.65, color='black', marker='x', markersize=12)
plt.annotate('18,16', xy=(35.65, 71.77), xytext=(35.65, 71.77))
'ttd_u=15'
plt.plot(data_ttd_u_15[0], eta_ttd_u_15[0], color='black', marker='x', markersize=12)
plt.annotate('8', xy=(41.08, 65.3), xytext=(41.08, 65.3))
plt.plot(41.24, 68.15, color='black', marker='x', markersize=12)
plt.annotate('11', xy=(40.85, 67.9), xytext=(40.85, 67.9))
plt.plot(40.27, 70.24, color='black', marker='x', markersize=12)
plt.annotate('15', xy=(39.80, 69.99), xytext=(39.80, 69.99))
plt.plot(38.90, 70.75, color='black', marker='x', markersize=12)
plt.annotate('18,16', xy=(38.87, 70.87), xytext=(38.87, 70.87))
'ttd_u=20'
plt.plot(44.14, 69.45, color='black', marker='x', markersize=12)
plt.annotate('15', xy=(43.74, 69.2), xytext=(43.74, 69.2))
plt.plot(42.47, 69.91, color='black', marker='x', markersize=12)
plt.annotate('18,16', xy=(42.44, 70.03), xytext=(42.44, 70.03))

plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
plt.xlim(30, 45)

o_line = mlines.Line2D([], [], color='black', label=r'$T_{se,ein}$ [C]          $ΔT_{gk,ob}$:')
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