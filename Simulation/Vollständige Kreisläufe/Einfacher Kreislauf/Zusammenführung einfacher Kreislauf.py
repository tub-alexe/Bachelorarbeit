from tespy.networks import Network
from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink)
from tespy.connections import Connection, Bus
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
from fluprodia import FluidPropertyDiagram
import math
import matplotlib.pyplot as plt
import numpy as np
from numpy import *


# importing the module
import json

# reading the data from the file
with open('Einfacher Kreislauf.txt') as f:
    read = f.readlines()

data_R601 = json.loads(read[1])
data_R601['p_kond'] = np.array(data_R601['p_kond'])
COP_R601 = json.loads(read[2])
eta_R601 = json.loads(read[3])

data_R1233ZDE = json.loads(read[5])
data_R1233ZDE['p_kond'] = np.array(data_R1233ZDE['p_kond'])
COP_R1233ZDE = json.loads(read[6])
eta_R1233ZDE = json.loads(read[7])

data_R600 = json.loads(read[9])
data_R600['p_kond'] = np.array(data_R600['p_kond'])
COP_R600 = json.loads(read[10])
eta_R600 = json.loads(read[11])

data_R1336MZZZ = json.loads(read[13])
data_R1336MZZZ['p_kond'] = np.array(data_R1336MZZZ['p_kond'])
COP_R1336MZZZ = json.loads(read[14])
eta_R1336MZZZ = json.loads(read[15])

plt.rc('font', **{'size': 18})

for key in data_R601:
    plt.scatter(data_R601[key], COP_R601[key], s=100, color="blue", label='R601')

for key in data_R1233ZDE:
    plt.scatter(data_R1233ZDE[key], COP_R1233ZDE[key], s=100, color="red", label='R1233ZDE')

for key in data_R600:
    plt.scatter(data_R600[key], COP_R600[key], s=100, color="greenyellow", label='R600')

for key in data_R1336MZZZ:
    plt.scatter(data_R1336MZZZ[key], COP_R1336MZZZ[key], s=100, color="black", label='R1336MZZZ')
plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('COP')
#plt.ylim([44, 60])
plt.legend(loc='upper right')
plt.grid()
plt.show()
plt.savefig('Zusammenführung einfacher Kreislauf_COP.svg')

plt.rc('font', **{'size': 18})

for key in data_R601:
    plt.scatter(data_R601[key], eta_R601[key], s=100, color="blue", label='R601')

for key in data_R1233ZDE:
    plt.scatter(data_R1233ZDE[key], eta_R1233ZDE[key], s=100, color="red", label='R1233ZDE')

for key in data_R600:
    plt.scatter(data_R600[key], eta_R600[key], s=100, color="greenyellow", label='R600')

for key in data_R1336MZZZ:
    plt.scatter(data_R1336MZZZ[key], eta_R1336MZZZ[key], s=100, color="black", label='R1336MZZZ')
plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('eta')
plt.legend(loc='upper right')
plt.grid()
plt.show()
plt.savefig('Zusammenführung einfacher Kreislauf_eta.svg')