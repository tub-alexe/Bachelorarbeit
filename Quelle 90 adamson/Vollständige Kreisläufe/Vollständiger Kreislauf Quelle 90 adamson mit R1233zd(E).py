from tespy.networks import Network
from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink)
from tespy.connections import Connection, Bus
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
from fluprodia import FluidPropertyDiagram

km = 'R1233ZD(E)'
se = 'H2O'
fld_km = {km: 1, se: 0}
fld_se = {km: 0, se: 1}

nw = Network(fluids=[km, se], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

# Komponenten

gk = HeatExchanger('Gaskühler')
se_ein = Source('Senke ein')
se_aus = Sink('Senke aus')

ue_in = Source('Verdampfer rein')
vd_aus = Sink('Überhitzer raus')
vd = HeatExchanger('Verdampfer')
ue = HeatExchanger('Überhitzer')

exp = Valve('Expansionsventil')
kp = Compressor('Verdichter')
cc = CycleCloser('Kreislauf_Ende')

#Verbindungen Kreislauf

c1 = Connection(cc, 'out1', gk, 'in1')
c2 = Connection(gk, 'out1', exp, 'in1')
c3 = Connection(exp, 'out1', vd, 'in2')
c4 = Connection(vd, 'out2', ue, 'in2')
c5 = Connection(ue, 'out2', kp, 'in1')
c6 = Connection(kp, 'out1', cc, 'in1')

#Verbindungen kalte Seite Gaskühler

c7 = Connection(se_ein, 'out1', gk, 'in2')
c8 = Connection(gk, 'out2', se_aus, 'in1')


#Verbindungen heiße Seite Verdampfer und Überhitzer
c9 = Connection(ue_in, 'out1', ue, 'in1')
c10 = Connection(ue, 'out1', vd, 'in1')
c11 = Connection(vd, 'out1', vd_aus, 'in1')
nw.add_conns(c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11)

#Parametrisierung Komponenten

gk.set_attr(pr1=1, pr2=1)
vd.set_attr(pr1=1, pr2=1)
ue.set_attr(pr1=1, pr2=1)
kp.set_attr(eta_s=0.7)
# Parametrisierung heiße Seite, vor dem Gaskühler

h_gk_vor = CPSI("H", "P", 56 * 1e5, "T", 273.15+205, km) * 1e-3
#c1.set_attr(h=h_gk_vor)

# Parametrisierung heiße Seite, nach dem Gaskühler, Druck bleibt konstant im Gaskühler

h_gk_nach = CPSI("H", "P", 56 * 1e5, "T", 273.15+105, km) * 1e-3
c2.set_attr(h=h_gk_nach, p=56)

# Parameter kalte Seite
# Vor dem Verdampfer

#h_verd = CPSI("H", "Q", 0, "T", 273.15+70, km) * 1e-3
c3.set_attr(p=5.1)

# Zwischen Verdampfer und Überhitzer
h_zw = CPSI("H", "Q", 1, "T", 273.15+70, km) * 1e-3
c4.set_attr(h=h_zw)

# Nach dem Überhitzer
h_uebe = CPSI("H", "P", 5.1 * 1e5, "T", 273.15+75, km) * 1e-3
c5.set_attr(h=h_uebe, fluid=fld_km)

#Parametrisierung kalte Seite Gaskühler

c7.set_attr(T=100, p=20, fluid=fld_se)
c8.set_attr(T=200)

#Parameter heiße Seite Verdampfer
c9.set_attr(T=80, m=5, p=5, fluid=fld_se)
c11.set_attr(T=75)

#Lösen

nw.solve(mode='design')
nw.print_results()

#c1.set_attr(h=None, T=205)
c2.set_attr(h=None, T=105)
#c3.set_attr(p=3.237)
c4.set_attr(h=None, x=1)
c5.set_attr(h=None, Td_bp=5)
c8.set_attr(T=None)
gk.set_attr(ttd_u=5)

# busses
power = Bus('power input')
power.add_comps(
    {'comp': kp, 'char': 1, 'base': 'bus'},
    {'comp': ue_in, 'base': 'bus'},
    {'comp': vd_aus})


heat_product = Bus('heating')
heat_product.add_comps(
    {'comp': se_ein, 'base': 'bus'},
    {'comp': se_aus})

power_COP = Bus('power')
power_COP.add_comps(
        {'comp': kp, 'char': -1, 'base': 'bus'}
)

heat_product_COP = Bus('heat_product')
heat_product_COP.add_comps(
            {"comp": gk, "char": 1})

nw.add_busses(power, heat_product, power_COP, heat_product_COP)

nw.solve(mode='design')
nw.print_results()
print('COP', heat_product_COP.P.val / power_COP.P.val)
print('COP', nw.busses["heat_product"].P.val / nw.busses["power"].P.val)

# Implementierung Exergie Analyse

pamb = 1
Tamb = 25

ean = ExergyAnalysis(nw, E_P=[heat_product], E_F=[power])
ean.analyse(pamb=pamb, Tamb=Tamb)
ean.print_results()
print(ean.network_data.loc['epsilon'])

#zweites Szenario funktioniert leider nicht

import matplotlib.pyplot as plt
import numpy as np

# make text reasonably sized
plt.rc('font', **{'size': 18})


data = {
    'p_verd': np.linspace(3, 5.8, 15),
    'p_kond': np.linspace(53, 72, 20),
    'T_kond': np.linspace(100.0061, 110, 10)
}
eta = {
    'p_verd': [],
    'p_kond': [],
    'T_kond': []
}
description = {
    'p_verd': 'Verdampferdruck in bar',
    'p_kond': 'Kondensatordruck in bar',
    'T_kond': 'Kondensatortemperatur in Celsius'
}

for p in data['p_verd']:
    c3.set_attr(p=p)
    nw.solve('design')
    ean.analyse(pamb=pamb, Tamb=Tamb)
    eta['p_verd'] += [ean.network_data.loc['epsilon']]

# reset to base temperature
c3.set_attr(p=5.1)

for p in data['p_kond']:
    c2.set_attr(p=p)
    nw.solve('design')
    ean.analyse(pamb=pamb, Tamb=Tamb)
    eta['p_kond'] += [ean.network_data.loc['epsilon']]

# reset to base temperature
c2.set_attr(p=56)

for T in data['T_kond']:
    c2.set_attr(T=T)
    nw.solve('design')
    ean.analyse(pamb=pamb, Tamb=Tamb)
    eta['T_kond'] += [ean.network_data.loc['epsilon']]

c2.set_attr(T=105)

fig, ax = plt.subplots(1, 3, sharey=True, figsize=(16, 8))

[a.grid() for a in ax]

i = 0
for key in data:
    ax[i].scatter(data[key], eta[key], s=100, color="#1f567d")
    ax[i].set_xlabel(description[key])
    i += 1

ax[0].set_ylabel('eta of the Heat Pump')

plt.tight_layout()

fig.savefig('Optimierung R1233ZD(E).svg')