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

with open('Einfacher Kreislauf\Einfacher Kreislauf.txt') as f:
    read = f.readlines()

data_R1233ZDE = json.loads(read[1])
#data_R1233ZDE['p_kond'] = np.array(data_R1233ZDE['p_kond'])
COP_R1233ZDE = json.loads(read[2])
eta_R1233ZDE = json.loads(read[3])

data_R600 = json.loads(read[5])
#data_R600['p_kond'] = np.array(data_R600['p_kond'])
COP_R600 = json.loads(read[6])
eta_R600 = json.loads(read[7])

data_R1336MZZZ = json.loads(read[9])
#data_R1336MZZZ['p_kond'] = np.array(data_R1336MZZZ['p_kond'])
COP_R1336MZZZ = json.loads(read[10])
eta_R1336MZZZ = json.loads(read[11])

with open('Einfacher Kreislauf mit IHX\IHX.txt') as f:
    read = f.readlines()

data_R1233ZDE_IHX = json.loads(read[1])
#data_R1233ZDE_IHX['p_kond'] = np.array(data_R1233ZDE_IHX['p_kond'])
COP_R1233ZDE_IHX = json.loads(read[2])
eta_R1233ZDE_IHX = json.loads(read[3])

data_R600_IHX = json.loads(read[5])
#data_R600_IHX['p_kond'] = np.array(data_R600_IHX['p_kond'])
COP_R600_IHX = json.loads(read[6])
eta_R600_IHX = json.loads(read[7])

data_R1336MZZZ_IHX = json.loads(read[9])
#data_R1336MZZZ_IHX['p_kond'] = np.array(data_R1336MZZZ_IHX['p_kond'])
COP_R1336MZZZ_IHX = json.loads(read[10])
eta_R1336MZZZ_IHX = json.loads(read[11])

with open('Parallelkompression\Parallelkompression.txt') as f:
    read = f.readlines()

data_R1233ZDE_Parallel = json.loads(read[1])
#data_R1233ZDE_Parallel['p_kond'] = np.array(data_R1233ZDE_Parallel['p_kond'])
COP_R1233ZDE_Parallel = json.loads(read[2])
eta_R1233ZDE_Parallel = json.loads(read[3])

data_R600_Parallel = json.loads(read[5])
#data_R600_Parallel['p_kond'] = np.array(data_R600_Parallel['p_kond'])
COP_R600_Parallel = json.loads(read[6])
eta_R600_Parallel = json.loads(read[7])

data_R1336MZZZ_Parallel = json.loads(read[9])
#data_R1336MZZZ_Parallel['p_kond'] = np.array(data_R1336MZZZ_Parallel['p_kond'])
COP_R1336MZZZ_Parallel = json.loads(read[10])
eta_R1336MZZZ_Parallel = json.loads(read[11])

with open('Zweistufenkompression mit Zwischenkühlung\Zweistufenkompression.txt') as f:
    read = f.readlines()

data_R1233ZDE_Zweistufen = json.loads(read[1])
#data_R1233ZDE_Zweistufen['p_kond'] = np.array(data_R1233ZDE_Zweistufen['p_kond'])
COP_R1233ZDE_Zweistufen = json.loads(read[2])
eta_R1233ZDE_Zweistufen = json.loads(read[3])

data_R600_Zweistufen = json.loads(read[5])
#data_R600_Zweistufen['p_kond'] = np.array(data_R600_Zweistufen['p_kond'])
COP_R600_Zweistufen = json.loads(read[6])
eta_R600_Zweistufen = json.loads(read[7])

data_R1336MZZZ_Zweistufen = json.loads(read[9])
#data_R1336MZZZ_Zweistufen['p_kond'] = np.array(data_R1336MZZZ_Zweistufen['p_kond'])
COP_R1336MZZZ_Zweistufen= json.loads(read[10])
eta_R1336MZZZ_Zweistufen = json.loads(read[11])

print(data_R600)
print(COP_R600)

plt.rc('font', **{'size': 18})

plt.plot(data_R1233ZDE, eta_R1233ZDE, color='r', label='einfacher Kreislauf')
plt.plot(data_R1233ZDE_IHX, eta_R1233ZDE_IHX, color='darkolivegreen', label='Interne Wärmerückgewinnung')
plt.plot(data_R1233ZDE_Parallel, eta_R1233ZDE_Parallel, color='black', label='Parallelkompression')
plt.plot(data_R1233ZDE_Zweistufen, eta_R1233ZDE_Zweistufen, color='royalblue', label='Zweistufenkompression')
plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('exergetischer Wirkungsgrad')
plt.legend(loc='upper right')
plt.grid()
plt.show()
plt.savefig('Zusammenführung_eta_R1233ZD(E).svg')

plt.plot(data_R600, eta_R600, color='r', label='einfacher Kreislauf')
plt.plot(data_R600_IHX, eta_R600_IHX, color='darkolivegreen', label='Interne Wärmerückgewinnung')
plt.plot(data_R600_Parallel, eta_R600_Parallel, color='black', label='Parallelkompression')
plt.plot(data_R600_Zweistufen, eta_R600_Zweistufen, color='royalblue', label='Zweistufenkompression')
plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('exergetischer Wirkungsgrad')
plt.legend(loc='upper right')
plt.grid()
plt.show()
plt.savefig('Zusammenführung_eta_R600.svg')

plt.plot(data_R1336MZZZ, eta_R1336MZZZ, color='r', label='einfacher Kreislauf') # plotting t, a separately
plt.plot(data_R1336MZZZ_IHX, eta_R1336MZZZ_IHX, color='darkolivegreen', label='Interne Wärmerückgewinnung')
plt.plot(data_R1336MZZZ_Parallel, eta_R1336MZZZ_Parallel, color='black', label='Parallelkompression')
plt.plot(data_R1336MZZZ_Zweistufen, eta_R1336MZZZ_Zweistufen, color='royalblue', label='Zweistufenkompression')
plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('exergetischer Wirkungsgrad')
plt.legend(loc='upper right')
plt.grid()
plt.show()
plt.savefig('Zusammenführung_eta_R1336mzz(Z).svg')

"""plt.rc('font', **{'size': 18})

#for key in data_R601:
    #plt.scatter(data_R601[key], COP_R601[key], s=100, color="blue", label='R601')

for key in data_R1233ZDE:
    plt.scatter(data_R1233ZDE[key], COP_R1233ZDE[key], s=100, color="red", label='R1233ZDE')

for key in data_R1233ZDE_IHX:
    plt.scatter(data_R1233ZDE_IHX[key], COP_R1233ZDE_IHX[key], s=100, color="red", label='R1233ZDE')

for key in data_R1233ZDE_Parallel:
    plt.scatter(data_R1233ZDE_Parallel[key], COP_R1233ZDE_Parallel[key], s=100, color="red", label='R1233ZDE')

plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('COP')
#plt.ylim([2.5, 3.3])
plt.legend(loc='upper right')
plt.grid()
plt.show()
plt.savefig('Zusammenführung_IHX_COP_R1233ZD(E).svg')

for key in data_R600:
    plt.scatter(data_R600[key], COP_R600[key], s=100, color="greenyellow", label='R600')

for key in data_R600_IHX:
    plt.scatter(data_R600_IHX[key], COP_R600_IHX[key], s=100, color="greenyellow", label='R600')

for key in data_R600_Parallel:
    plt.scatter(data_R600_Parallel[key], COP_R600_Parallel[key], s=100, color="greenyellow", label='R600')

plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('COP')
#plt.ylim([2.5, 3.3])
plt.legend(loc='upper right')
plt.grid()
plt.show()
plt.savefig('Zusammenführung_IHX_COP_R600.svg')

for key in data_R1336MZZZ:
    plt.scatter(data_R1336MZZZ[key], COP_R1336MZZZ[key], s=100, color="black", label='R1336MZZZ')

for key in data_R1336MZZZ_IHX:
    plt.scatter(data_R1336MZZZ_IHX[key], COP_R1336MZZZ_IHX[key], s=100, color="black", label='R1336MZZZ')

for key in data_R1336MZZZ_Parallel:
    plt.scatter(data_R1336MZZZ_Parallel[key], COP_R1336MZZZ_Parallel[key], s=100, color="black", label='R1336MZZZ')

plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('COP')
#plt.ylim([2.5, 3.3])
plt.legend(loc='upper right')
plt.grid()
plt.show()
plt.savefig('Zusammenführung_IHX_COP_R1336MZZ(Z).svg')

plt.rc('font', **{'size': 18})

for key in data_R1233ZDE:
    plt.scatter(data_R1233ZDE[key], eta_R1233ZDE[key], s=100, color="red", label='R1233ZDE')

for key in data_R1233ZDE_IHX:
    plt.scatter(data_R1233ZDE_IHX[key], eta_R1233ZDE_IHX[key], s=100, color="red", label='R1233ZDE')

for key in data_R1233ZDE_Parallel:
    plt.scatter(data_R1233ZDE_Parallel[key], eta_R1233ZDE_Parallel[key], s=100, color="red", label='R1233ZDE')

plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('COP')
#plt.ylim([2.5, 3.3])
plt.legend(loc='upper right')
plt.grid()
plt.show()
plt.savefig('Zusammenführung_IHX_eta_R1233ZD(E).svg')

for key in data_R600:
    plt.scatter(data_R600[key], eta_R600[key], s=100, color="greenyellow", label='R600')

for key in data_R600_IHX:
    plt.scatter(data_R600_IHX[key], eta_R600_IHX[key], s=100, color="greenyellow", label='R600')

for key in data_R600_Parallel:
    plt.scatter(data_R600_Parallel[key], eta_R600_Parallel[key], s=100, color="greenyellow", label='R600')

plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('COP')
#plt.ylim([2.5, 3.3])
plt.legend(loc='upper right')
plt.grid()
plt.show()
plt.savefig('Zusammenführung_IHX_eta_R600.svg')

for key in data_R1336MZZZ:
    plt.scatter(data_R1336MZZZ[key], eta_R1336MZZZ[key], s=100, color="black", label='R1336MZZZ')

for key in data_R1336MZZZ_IHX:
    plt.scatter(data_R1336MZZZ_IHX[key], eta_R1336MZZZ_IHX[key], s=100, color="black", label='R1336MZZZ')

for key in data_R1336MZZZ_Parallel:
    plt.scatter(data_R1336MZZZ_Parallel[key], eta_R1336MZZZ_Parallel[key], s=100, color="black", label='R1336MZZZ')

plt.xlabel('Gaskühlerdruck in bar')
plt.ylabel('COP')
#plt.ylim([2.5, 3.3])
plt.legend(loc='upper right')
plt.grid()
plt.show()
plt.savefig('Zusammenführung_IHX_eta_R1336mzz(Z).svg')"""
