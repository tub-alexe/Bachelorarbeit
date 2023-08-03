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
with open('../Simulation/Vollständige Kreisläufe/Parallelkompression/Senkeneintrittstemperatur.txt') as f:
    read = f.readlines()

data_T160 = json.loads(read[1])
COP_T160 = json.loads(read[2])
eta_T160 = json.loads(read[3])

data_T150 = json.loads(read[5])
COP_T150 = json.loads(read[6])
eta_T150 = json.loads(read[7])

data_T140 = json.loads(read[9])
COP_T140 = json.loads(read[10])
eta_T140 = json.loads(read[11])

plt.rc('font', **{'size': 18})

plt.plot(data_T160, eta_T160, color='r', label='160°C')
plt.plot(data_T150, eta_T150, color='darkolivegreen', label='150°C')
plt.plot(data_T140, eta_T140, color='peru', label='140°C')
plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('exergetischer Wirkungsgrad')
plt.legend(loc='upper right')
plt.grid()
plt.show()
#plt.savefig('Zwischendruck.svg')