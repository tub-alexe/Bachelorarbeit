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

data_zw8einhalb = json.loads(read[1])
COP_zw8einhalb = json.loads(read[2])
eta_zw8einhalb= json.loads(read[3])

data_zw9einhalb = json.loads(read[5])
COP_zw9einhalb = json.loads(read[6])
eta_zw9einhalb = json.loads(read[7])

data_zw_opt = json.loads(read[9])
COP_zw_opt = json.loads(read[10])
eta_zw_opt = json.loads(read[11])

data_zw12 = json.loads(read[13])
COP_zw12 = json.loads(read[14])
eta_zw12 = json.loads(read[15])


plt.rc('font', **{'size': 18})

plt.plot(data_zw8einhalb, eta_zw8einhalb, color='r', label='Zwischendruck 8.5 bar')
plt.plot(data_zw9einhalb, eta_zw9einhalb, color='darkolivegreen', label='Zwischendruck 9.5 bar')
plt.plot(data_zw_opt, eta_zw_opt, color='royalblue', label='Zwischendruck 11.83 bar')
plt.plot(data_zw12, eta_zw12, color='peru', label='Zwischendruck 12 bar')
plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('exergetischer Wirkungsgrad')
plt.legend(loc='upper right')
plt.grid()
plt.show()
plt.savefig('Zwischendruck.svg')