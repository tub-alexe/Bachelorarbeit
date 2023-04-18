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

data_IHX_T160 = json.loads(read[1])
COP_IHX_T160 = json.loads(read[2])
eta_IHX_T160 = json.loads(read[3])

data_IHX_T150 = json.loads(read[5])
COP_IHX_T150 = json.loads(read[6])
eta_IHX_T150 = json.loads(read[7])

data_IHX_T140 = json.loads(read[9])
COP_IHX_T140 = json.loads(read[10])
eta_IHX_T140 = json.loads(read[11])

data_IHX_T160_R1233ZDE = json.loads(read[13])
COP_IHX_T160_R1233ZDE = json.loads(read[14])
eta_IHX_T160_R1233ZDE = json.loads(read[15])

data_IHX_T150_R1233ZDE = json.loads(read[17])
COP_IHX_T150_R1233ZDE = json.loads(read[18])
eta_IHX_T150_R1233ZDE = json.loads(read[19])

data_IHX_T140_R1233ZDE = json.loads(read[21])
COP_IHX_T140_R1233ZDE = json.loads(read[22])
eta_IHX_T140_R1233ZDE = json.loads(read[23])

data_IHX_T130_R1233ZDE = json.loads(read[25])
COP_IHX_T130_R1233ZDE = json.loads(read[26])
eta_IHX_T130_R1233ZDE = json.loads(read[27])

with open('Parallelkompression\Senkentemperatur.txt') as f:
    read = f.readlines()

data_Parallel_T160 = json.loads(read[1])
COP_Parallel_T160 = json.loads(read[2])
eta_Parallel_T160 = json.loads(read[3])

data_Parallel_T150 = json.loads(read[5])
COP_Parallel_T150 = json.loads(read[6])
eta_Parallel_T150 = json.loads(read[7])

data_Parallel_T140 = json.loads(read[9])
COP_Parallel_T140 = json.loads(read[10])
eta_Parallel_T140 = json.loads(read[11])

data_Parallel_T160_R1233ZDE = json.loads(read[13])
COP_Parallel_T160_R1233ZDE = json.loads(read[14])
eta_Parallel_T160_R1233ZDE = json.loads(read[15])

data_Parallel_T150_R1233ZDE = json.loads(read[17])
COP_Parallel_T150_R1233ZDE = json.loads(read[18])
eta_Parallel_T150_R1233ZDE = json.loads(read[19])

data_Parallel_T140_R1233ZDE = json.loads(read[21])
COP_Parallel_T140_R1233ZDE = json.loads(read[22])
eta_Parallel_T140_R1233ZDE = json.loads(read[23])

data_Parallel_T130_R1233ZDE = json.loads(read[25])
COP_Parallel_T130_R1233ZDE = json.loads(read[26])
eta_Parallel_T130_R1233ZDE = json.loads(read[27])

plt.rc('font', **{'size': 18})

plt.plot(data_IHX_T160, eta_IHX_T160, marker='o', color='red')
plt.plot(data_IHX_T150, eta_IHX_T150, marker='o', color='darkcyan', label='150°C IHX')
plt.plot(data_IHX_T140, eta_IHX_T140, marker='o',  color='gold', label='140°C IHX')
plt.plot(data_Parallel_T160, eta_Parallel_T160, marker='s', color='red', label='160°C Parallel')
plt.plot(data_Parallel_T150, eta_Parallel_T150, marker='s', color='darkcyan', label='150°C Parallel')
plt.plot(data_Parallel_T140, eta_Parallel_T140, marker='s', color='gold', label='140°C Parallel')
plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('exergetischer Wirkungsgrad')
#plt.legend(loc='upper right', fontsize='13')
o_line = mlines.Line2D([], [], color='red', marker='o',
                          markersize=5, label='IHX')
s_line = mlines.Line2D([], [], color='red', marker='s',
                          markersize=5, label='Parallel')
red_line = mlines.Line2D([], [], color='red', label='160°C')
blue_line = mlines.Line2D([], [], color='darkcyan', label='150°C')
yellow_line = mlines.Line2D([], [], color='gold', label='140°C')
plt.legend(handles=[o_line, s_line, red_line, blue_line, yellow_line])
plt.grid()
plt.show()
plt.savefig('Senkentemperatur.svg')

plt.plot(data_IHX_T160_R1233ZDE, eta_IHX_T160_R1233ZDE, marker='o', color='red')
plt.plot(data_IHX_T150_R1233ZDE, eta_IHX_T150_R1233ZDE, marker='o', color='darkcyan', label='150°C IHX')
plt.plot(data_IHX_T140_R1233ZDE, eta_IHX_T140_R1233ZDE, marker='o',  color='gold', label='140°C IHX')
plt.plot(data_IHX_T130_R1233ZDE, eta_IHX_T130_R1233ZDE, marker='o',  color='green', label='130°C IHX')
plt.plot(data_Parallel_T160_R1233ZDE, eta_Parallel_T160_R1233ZDE, marker='s', color='red', label='160°C Parallel')
plt.plot(data_Parallel_T150_R1233ZDE, eta_Parallel_T150_R1233ZDE, marker='s', color='darkcyan', label='150°C Parallel')
plt.plot(data_Parallel_T140_R1233ZDE, eta_Parallel_T140_R1233ZDE, marker='s', color='gold', label='140°C Parallel')
plt.plot(data_Parallel_T130_R1233ZDE, eta_Parallel_T130_R1233ZDE, marker='s', color='green', label='130°C Parallel')
plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('exergetischer Wirkungsgrad')
#plt.legend(loc='upper right', fontsize='13')
o_line = mlines.Line2D([], [], color='red', marker='o',
                          markersize=5, label='IHX')
s_line = mlines.Line2D([], [], color='red', marker='s',
                          markersize=5, label='Parallel')
red_line = mlines.Line2D([], [], color='red', label='160°C')
blue_line = mlines.Line2D([], [], color='darkcyan', label='150°C')
yellow_line = mlines.Line2D([], [], color='gold', label='140°C')
plt.legend(handles=[o_line, s_line, red_line, blue_line, yellow_line])
plt.grid()
plt.show()


