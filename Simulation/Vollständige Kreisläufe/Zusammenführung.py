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
import matplotlib.lines as mlines


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

data_R601 = json.loads(read[13])
COP_R601 = json.loads(read[14])
eta_R601 = json.loads(read[15])

data_R601_Ursprung = json.loads(read[17])
COP_R601_Ursprung = json.loads(read[18])
eta_R601_Ursprung = json.loads(read[19])

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

data_R601_IHX = json.loads(read[13])
COP_R601_IHX = json.loads(read[14])
eta_R601_IHX = json.loads(read[15])

data_R601_IHX_Ursprung = json.loads(read[17])
COP_R601_IHX_Ursprung = json.loads(read[18])
eta_R601_IHX_Ursprung = json.loads(read[19])

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

data_R601_Parallel = json.loads(read[13])
COP_R601_Parallel = json.loads(read[14])
eta_R601_Parallel = json.loads(read[15])

data_R601_Parallel_Ursprung = json.loads(read[17])
COP_R601_Parallel_Ursprung = json.loads(read[18])
eta_R601_Parallel_Ursprung = json.loads(read[19])

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
COP_R1336MZZZ_Zweistufen= json.loads(read[10])
eta_R1336MZZZ_Zweistufen = json.loads(read[11])

data_R601_Zweistufen = json.loads(read[13])
COP_R601_Zweistufen= json.loads(read[14])
eta_R601_Zweistufen = json.loads(read[15])

data_R601_Zweistufen_Ursprung = json.loads(read[17])
COP_R601_Zweistufen_Ursprung = json.loads(read[18])
eta_R601_Zweistufen_Ursprung = json.loads(read[19])

print(data_R600)
print(COP_R600)

plt.rc('font', **{'size': 20})
plt.rcParams["figure.figsize"] = (20, 12)

"""plt.plot(data_R1233ZDE, eta_R1233ZDE, color='r', label='einfacher Kreislauf')
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
plt.savefig('Zusammenführung_eta_R1336mzz(Z).svg')"""


fig, ax = plt.subplots(1, 2)
ax[1].plot(data_R1233ZDE, eta_R1233ZDE, color='red', label='einfacher Kreislauf')
#ax[1].plot(51.73, 50.02, color='black', marker='x', markersize=12)
ax[0].plot(data_R1233ZDE_IHX, eta_R1233ZDE_IHX, color='steelblue', label='mit IWÜ')
ax[0].plot(data_R1233ZDE_Parallel, eta_R1233ZDE_Parallel, color='green', label='mit IWÜ und PK')
#ax[0].plot(39.3, 71.78, color='black', marker='x', markersize=12)
ax[0].plot(data_R1233ZDE_Zweistufen, eta_R1233ZDE_Zweistufen, color='orange', label='mit IWÜ und ZK')
#ax[0].plot(38.5455, 61.71, color='black', marker='x', markersize=12)
ax[0].set_xlabel('Gaskühlerdruck in bar')
ax[0].set_ylabel('exergetischer Wirkungsgrad')
red_line = mlines.Line2D([], [], color='red', label='einfacher Kreislauf')
green_line = mlines.Line2D([], [], color='green', label='Zweistufenkompression')
orange_line = mlines.Line2D([], [], color='orange', label='Parallelkompression')
blue_line = mlines.Line2D([], [], color='steelblue', label='Interne Wärmerückgewinnung')
#ax[0].legend(handles=[ red_line, green_line, black_line, blue_line], fontsize=14)
ax[0].legend(loc='upper right', fontsize=16)
ax[1].legend(loc='upper left', fontsize=16)
ax[1].set_xlabel('Gaskühlerdruck in bar')
ax[1].set_ylabel('exergetischer Wirkungsgrad')
ax[0].grid()
ax[1].grid()
plt.show()

fig, ax = plt.subplots(1, 2)
ax[1].plot(data_R600, eta_R600, color='r', label='einfacher Kreislauf')
ax[1].plot(79.82, 40.85, color='black', marker='x', markersize=12)
ax[0].plot(data_R600_IHX, eta_R600_IHX, color='steelblue', label='mit IWÜ')
ax[0].plot(data_R600_Parallel, eta_R600_Parallel, color='green', label='mit IWÜ und PK')
ax[0].plot(53.956, 66.74, color='black', marker='x', markersize=12)
ax[0].plot(data_R600_Zweistufen, eta_R600_Zweistufen, color='orange', label='mit IWÜ und ZK')
ax[0].plot(53.636, 58.62, color='black', marker='x', markersize=12)
ax[0].set_xlabel('Gaskühlerdruck in bar')
ax[0].set_ylabel('exergetischer Wirkungsgrad')
red_line = mlines.Line2D([], [], color='red', label='einfacher Kreislauf')
green_line = mlines.Line2D([], [], color='steelblue', label='Interne Wärmerückgewinnung')
black_line = mlines.Line2D([], [], color='green', label='Parallelkompression')
blue_line = mlines.Line2D([], [], color='orange', label='Zweistufenkompression')
#ax[0].legend(handles=[ red_line, green_line, black_line, blue_line], fontsize=14)
ax[0].legend(loc='upper right', fontsize=16)
ax[1].legend(loc='upper left', fontsize=16)
ax[1].set_xlabel('Gaskühlerdruck in bar')
ax[1].set_ylabel('exergetischer Wirkungsgrad')
#ax[0].set_xlim([50, 77])
#ax[0].set_ylim([62, 68])
ax[0].grid()
ax[1].grid()
plt.show()

fig, ax = plt.subplots(1, 2)
ax[1].plot(data_R1336MZZZ, eta_R1336MZZZ, color='r', label='einfacher Kreislauf')
ax[1].plot(50.47, 43.97, color='black', marker='x', markersize=12)
ax[0].plot(data_R1336MZZZ_IHX, eta_R1336MZZZ_IHX, color='steelblue', label='mit IWÜ')
ax[0].plot(data_R1336MZZZ_Parallel, eta_R1336MZZZ_Parallel, color='green', label='mit IWÜ und PK')
ax[0].plot(34.12, 65.99, color='black', marker='x', markersize=12)
ax[0].plot(data_R1336MZZZ_Zweistufen, eta_R1336MZZZ_Zweistufen, color='orange', label='mit IWÜ und ZK')
ax[0].set_xlabel('Gaskühlerdruck in bar')
ax[0].set_ylabel('exergetischer Wirkungsgrad')
red_line = mlines.Line2D([], [], color='red', label='einfacher Kreislauf')
green_line = mlines.Line2D([], [], color='darkolivegreen', label='Interne Wärmerückgewinnung')
black_line = mlines.Line2D([], [], color='black', label='Parallelkompression')
blue_line = mlines.Line2D([], [], color='royalblue', label='Zweistufenkompression')
#ax[0].legend(handles=[ red_line, green_line, black_line, blue_line], fontsize=14)
ax[0].legend(loc='upper right', fontsize=16)
ax[1].legend(loc='upper left', fontsize=16)
ax[1].set_xlabel('Gaskühlerdruck in bar')
ax[1].set_ylabel('exergetischer Wirkungsgrad')
ax[0].grid()
ax[1].grid()
plt.show()

fig, ax = plt.subplots(1, 2)
ax[1].plot(data_R601, eta_R601, color='r', label='einfacher Kreislauf')
ax[0].plot(data_R601_IHX, eta_R601_IHX, color='steelblue', label='mit IWÜ')
ax[0].plot(data_R601_Parallel, eta_R601_Parallel, color='green', label='mit IWÜ und PK')
#ax[0].plot(31.1, 63.73, color='black', marker='x', markersize=12)
ax[0].plot(data_R601_Zweistufen, eta_R601_Zweistufen, color='orange', label='mit IWÜ und ZK')
ax[0].set_xlabel('Gaskühlerdruck in bar')
ax[0].set_ylabel('exergetischer Wirkungsgrad')
red_line = mlines.Line2D([], [], color='red', label='einfacher Kreislauf')
green_line = mlines.Line2D([], [], color='steelblue', label='Interne Wärmerückgewinnung')
black_line = mlines.Line2D([], [], color='orange', label='Parallelkompression')
blue_line = mlines.Line2D([], [], color='green', label='Zweistufenkompression')
#ax[0].legend(handles=[ red_line, green_line, black_line, blue_line], fontsize=14)
ax[0].legend(loc='upper right')
ax[1].legend(loc='upper left')
ax[0].set_xlabel('Gaskühlerdruck [bar]')
ax[0].set_ylabel('exergetischer Wirkungsgrad [%]')
ax[1].set_xlabel('Gaskühlerdruck [bar]')
ax[1].set_ylabel('exergetischer Wirkungsgrad [%]')
ax[0].grid()
ax[0].set_ylim([63, 69.2])
ax[1].grid()
plt.savefig('Hochdruck R601 Ursprung.svg')
plt.show()

plt.plot(data_R601_Ursprung, eta_R601_Ursprung, color='red', label='R601')
#plt.plot(32.88, 52.99, color='black', marker='x', markersize=12)
plt.plot(data_R1233ZDE, eta_R1233ZDE, color='steelblue', label='R1233ZD(E)')
#plt.plot(51.73, 50.02, color='black', marker='x', markersize=12)
plt.plot(data_R600, eta_R600, color='orange', label='R600')
#plt.plot(79.82, 40.85, color='black', marker='x', markersize=12)
plt.plot(data_R1336MZZZ, eta_R1336MZZZ, color='green', label='R1336mzz(Z)')
#plt.plot(50.47, 43.97, color='black', marker='x', markersize=12)
plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
plt.legend(loc='upper right')
plt.grid()
plt.savefig('Hochdruck einfacher Kreislauf.svg')
plt.show()


plt.plot(data_R601_IHX_Ursprung, eta_R601_IHX_Ursprung, color='red', label='R601')
plt.plot(data_R1233ZDE_IHX, eta_R1233ZDE_IHX, color='steelblue', label='R1233ZD(E)')
plt.plot(data_R600_IHX, eta_R600_IHX, color='orange', label='R600')
plt.plot(data_R1336MZZZ_IHX, eta_R1336MZZZ_IHX, color='green', label='R1336mzz(Z)')
plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
plt.legend(loc='upper right')
plt.grid()
plt.savefig('Hochdruck interne Wärmerückgewinnung.svg')
plt.show()

plt.plot(data_R601_Parallel_Ursprung, eta_R601_Parallel_Ursprung, color='red', label='R601')
plt.plot(data_R1233ZDE_Parallel, eta_R1233ZDE_Parallel, color='steelblue', label='R1233ZD(E)')
#plt.plot(39.3, 71.78, color='black', marker='x', markersize=12)
plt.plot(data_R600_Parallel, eta_R600_Parallel, color='orange', label='R600')
#plt.plot(53.956, 66.74, color='black', marker='x', markersize=12)
plt.plot(data_R1336MZZZ_Parallel, eta_R1336MZZZ_Parallel, color='green', label='R1336mzz(Z)')
#plt.plot(34.12, 65.99, color='black', marker='x', markersize=12)
plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
plt.legend(loc='upper right')
plt.grid()
plt.savefig('Hochdruck interne Wärmerückgewinnung mit Parallelkompression.svg')
plt.show()

plt.plot(data_R601_Zweistufen_Ursprung, eta_R601_Zweistufen_Ursprung, color='red', label='R601')
plt.plot(data_R1233ZDE_Zweistufen, eta_R1233ZDE_Zweistufen, color='steelblue', label='R1233ZD(E)')
#plt.plot(38.5455, 61.71, color='black', marker='x', markersize=12)
plt.plot(data_R600_Zweistufen, eta_R600_Zweistufen, color='orange', label='R600')
#plt.plot(53.636, 58.62, color='black', marker='x', markersize=12)
plt.plot(data_R1336MZZZ_Zweistufen, eta_R1336MZZZ_Zweistufen, color='green', label='R1336mzz(Z)')
plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
plt.legend(loc='upper right')
plt.grid()
plt.savefig('Hochdruck interne Wärmerückgewinnung mit Zwischenkühlung.svg')
plt.show()

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
