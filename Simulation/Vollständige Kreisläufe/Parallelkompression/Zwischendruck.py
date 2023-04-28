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

data_zw21 = json.loads(read[17])
COP_zw21 = json.loads(read[18])
eta_zw21 = json.loads(read[19])

plt.rc('font', **{'size': 18})

plt.plot(data_zw8, eta_zw8, color='r', label='Zwischendruck 8 bar')
plt.plot(34.12, 65.99, color='black', marker='x', markersize=12)
plt.plot(data_zw11, eta_zw11, color='darkolivegreen', label='Zwischendruck 11 bar')
plt.plot(34.27, 69.4, color='black', marker='x', markersize=12)
plt.plot(data_zw19, eta_zw19, color='royalblue', label='Zwischendruck 18,16 bar')
plt.plot(32.775, 72.59, color='black', marker='x', markersize=12)
plt.plot(data_zw21, eta_zw21, color='peru', label='Zwischendruck 21 bar')
plt.plot(31.805, 72.36, color='black', marker='x', markersize=12)
plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('exergetischer Wirkungsgrad')
plt.legend(loc='upper right')
plt.grid()
plt.show()
plt.savefig('Zwischendruck.svg')