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

with open('../Einfacher Kreislauf/Einfacher Kreislauf.txt') as f:
    read = f.readlines()

data_R1233ZDE = json.loads(read[3])
eta_R1233ZDE = json.loads(read[4])

data_R600 = json.loads(read[6])
eta_R600 = json.loads(read[7])

data_R1336MZZZ = json.loads(read[9])
eta_R1336MZZZ = json.loads(read[10])

data_R601 = json.loads(read[12])
eta_R601 = json.loads(read[13])

data_R601_neu = json.loads(read[15])
eta_R601_neu = json.loads(read[16])

with open('../Einfacher Kreislauf mit IHX/IHX.txt') as f:
    read = f.readlines()

data_R1233ZDE_IHX = json.loads(read[3])
eta_R1233ZDE_IHX = json.loads(read[4])

data_R600_IHX = json.loads(read[6])
eta_R600_IHX = json.loads(read[7])

data_R1336MZZZ_IHX = json.loads(read[9])
eta_R1336MZZZ_IHX = json.loads(read[10])

data_R601_IHX = json.loads(read[12])
eta_R601_IHX = json.loads(read[13])

data_R601_IHX_neu = json.loads(read[15])
eta_R601_IHX_neu = json.loads(read[16])

with open('../Parallelkompression/Parallelkompression.txt') as f:
    read = f.readlines()

data_R1233ZDE_Parallel = json.loads(read[3])
eta_R1233ZDE_Parallel = json.loads(read[4])

data_R600_Parallel = json.loads(read[6])
eta_R600_Parallel = json.loads(read[7])

data_R1336MZZZ_Parallel = json.loads(read[9])
eta_R1336MZZZ_Parallel = json.loads(read[10])

data_R601_Parallel = json.loads(read[12])
eta_R601_Parallel = json.loads(read[13])

data_R601_Parallel_neu = json.loads(read[15])
eta_R601_Parallel_neu = json.loads(read[16])

with open('../Zweistufenkompression mit Zwischenkühlung/Zweistufenkompression.txt') as f:
    read = f.readlines()

data_R1233ZDE_Zweistufen = json.loads(read[3])
eta_R1233ZDE_Zweistufen = json.loads(read[4])

data_R600_Zweistufen = json.loads(read[6])
eta_R600_Zweistufen = json.loads(read[7])

data_R1336MZZZ_Zweistufen = json.loads(read[9])
eta_R1336MZZZ_Zweistufen = json.loads(read[10])

data_R601_Zweistufen = json.loads(read[12])
eta_R601_Zweistufen = json.loads(read[13])

data_R601_Zweistufen_neu = json.loads(read[15])
eta_R601_Zweistufen_neu = json.loads(read[16])

plt.rc('font', **{'size': 20})
plt.rcParams["figure.figsize"] = (20, 12)

plt.plot(data_R601, eta_R601, color='red', label='R601')
#plt.plot(32.88, 52.99, color='black', marker='x', markersize=12)
plt.plot(data_R1233ZDE, eta_R1233ZDE, color='steelblue', label='R1233zd(E)')
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


plt.plot(data_R601_IHX, eta_R601_IHX, color='red', label='R601')
plt.plot(data_R1233ZDE_IHX, eta_R1233ZDE_IHX, color='steelblue', label='R1233zd(E)')
plt.plot(data_R600_IHX, eta_R600_IHX, color='orange', label='R600')
plt.plot(data_R1336MZZZ_IHX, eta_R1336MZZZ_IHX, color='green', label='R1336mzz(Z)')
plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
plt.legend(loc='upper right')
plt.ylim(62, 74)
plt.grid()
plt.savefig('Hochdruck interne Wärmerückgewinnung.svg')
plt.show()

plt.plot(data_R601_Parallel, eta_R601_Parallel, color='red', label='R601')
plt.plot(data_R1233ZDE_Parallel, eta_R1233ZDE_Parallel, color='steelblue', label='R1233zd(E)')
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

plt.plot(data_R601_Zweistufen, eta_R601_Zweistufen, color='red', label='R601')
plt.plot(data_R1233ZDE_Zweistufen, eta_R1233ZDE_Zweistufen, color='steelblue', label='R1233zd(E)')
#plt.plot(38.5455, 61.71, color='black', marker='x', markersize=12)
plt.plot(data_R600_Zweistufen, eta_R600_Zweistufen, color='orange', label='R600')
#plt.plot(53.636, 58.62, color='black', marker='x', markersize=12)
plt.plot(data_R1336MZZZ_Zweistufen, eta_R1336MZZZ_Zweistufen, color='green', label='R1336mzz(Z)')
plt.xlabel('Gaskühlerdruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
plt.legend(loc='upper right')
plt.ylim(58, 74)
plt.grid()
plt.savefig('Hochdruck interne Wärmerückgewinnung mit Zwischenkühlung.svg')
plt.show()

plt.rc('font', **{'size': 20})
plt.rcParams["figure.figsize"] = (20, 12)

fig, ax = plt.subplots(1, 2)
ax[1].plot(data_R601_neu, eta_R601_neu, color='r', label='einfacher Kreislauf')
ax[0].plot(data_R601_IHX_neu, eta_R601_IHX_neu, color='steelblue', label='mit IWÜ')
ax[0].plot(data_R601_Parallel_neu, eta_R601_Parallel_neu, color='green', label='mit IWÜ und PK')
ax[0].plot(data_R601_Zweistufen_neu, eta_R601_Zweistufen_neu, color='orange', label='mit IWÜ und ZK')
ax[0].set_xlabel('Gaskühlerdruck in bar')
ax[0].set_ylabel('exergetischer Wirkungsgrad')
red_line = mlines.Line2D([], [], color='red', label='einfacher Kreislauf')
green_line = mlines.Line2D([], [], color='steelblue', label='Interne Wärmerückgewinnung')
black_line = mlines.Line2D([], [], color='orange', label='Parallelkompression')
blue_line = mlines.Line2D([], [], color='green', label='Zweistufenkompression')
ax[0].set_xlim([30.01, 40])
ax[0].set_ylim([63, 69])
ax[1].set_xlim([119.99, 140])
ax[1].set_ylim([38.981, 39.04])
ax[0].legend(loc='upper right')
ax[1].legend(loc='upper left')
ax[0].set_xlabel('Gaskühlerdruck [bar]')
ax[0].set_ylabel('exergetischer Wirkungsgrad [%]')
ax[1].set_xlabel('Gaskühlerdruck [bar]')
ax[1].set_ylabel('exergetischer Wirkungsgrad [%]')
ax[0].grid()
ax[1].grid()
plt.tight_layout()
plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.3, hspace=0.35)
plt.savefig('Hochdruck R601 neu.svg')
plt.show()

