from tespy.networks import Network
from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink)
from tespy.connections import Connection, Bus
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
from fluprodia import FluidPropertyDiagram

km = 'R601'
se = 'H2O'
fld_km = {km: 1, se: 0}
fld_se = {km: 0, se: 1}

nw = Network(fluids=[km, se], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

# Komponenten

gk = HeatExchanger('Gaskühler')
se_ein = Source('Senke ein')
se_aus = Sink('Senke aus')

ue_ein = Source('Überhitzer rein')
vd_aus = Sink('Verdampfer raus')
vd = HeatExchanger('Verdampfer')
ue = HeatExchanger('Überhitzer')
ihx = HeatExchanger("Internal Heat Exchanger")
exp = Valve('Expansionsventil')
kp = Compressor('Kompressor')
cc = CycleCloser('Kreilaufzusammenschluss')
kr_ein = Source('Kreislauf ein')
kr_aus = Sink('Kreilauf aus')


#Verbindungen Kreislauf

c3 = Connection(gk, 'out1', ihx, 'in1')
c4 = Connection(ihx, 'out1', exp, 'in1')
c5 = Connection(exp, 'out1', vd, 'in2')
c5_ue = Connection(vd, 'out2', ue, 'in2')
c6 = Connection(ue, 'out2', ihx, 'in2')
c1 = Connection(ihx, 'out2', kp, 'in1')
c2cc = Connection(kp, 'out1', cc, 'in1')
c2 = Connection(cc, 'out1', gk, 'in1')

#kalte Seite Gaskühler
c7 = Connection(se_ein, 'out1', gk, 'in2')
c8 = Connection(gk, 'out2', se_aus, 'in1')

#Verbindungen heiße Seite

c9 = Connection(ue_ein, 'out1', ue, 'in1')
c10 = Connection(ue, 'out1', vd, 'in1')
c11 = Connection(vd, 'out1', vd_aus, 'in1')

nw.add_conns(c1, c2, c2cc, c3, c4, c5, c5_ue, c6, c7, c8, c9, c10, c11)

#Parametrisierung Komponenten
gk.set_attr(pr1=1, pr2=1)
ihx.set_attr(pr1=1, pr2=1)
vd.set_attr(pr1=1, pr2=1)
ue.set_attr(pr1=1, pr2=1)
kp.set_attr(eta_s=0.7)

#Parametrisierung Verbindungen
h_ihx_h_nach = CPSI("H", "P", 2.8 * 1e5, "T", 273.15+100, km) * 1e-3
c1.set_attr(h=h_ihx_h_nach, p=2.8, fluid=fld_km)


h_ihx_k_vor = CPSI("H", "P", 35 * 1e5, "T", 273.15+105, km) * 1e-3
c3.set_attr(h=h_ihx_k_vor, p=35)

h_zw = CPSI("H", "P", 2.8 * 1e5, "T", 273.15+70, km) * 1e-3
c5_ue.set_attr(h=h_zw)

h_ihx_k_nach = CPSI("H", "P", 2.8 * 1e5, "T", 273.15+75, km) * 1e-3
c6.set_attr(h=h_ihx_k_nach)

#kalte Seite Gaskühler
c7.set_attr(T=100, p=20, fluid=fld_se)
c8.set_attr(T=200)

#Parameter heiße Seite Verdampfer
c9.set_attr(T=80, m=5, p=5, fluid=fld_se)
c11.set_attr(T=75)

nw.solve(mode='design')
nw.print_results()
print(f'COP = {abs(gk.Q.val) / kp.P.val}')

c1.set_attr(p=2.8, h=None)
ihx.set_attr(ttd_u=5)
c3.set_attr(h=None, p=35, T=105)
c5_ue.set_attr(h=None, x=1)
c6.set_attr(h=None, Td_bp=5)
c8.set_attr(T=None)
gk.set_attr(ttd_u=4)
# busses
power = Bus('power input')
power.add_comps(
    {'comp': kp, 'char': 1, 'base': 'bus'},
    {'comp': ue_ein, 'base': 'bus'},
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

import matplotlib.pyplot as plt
import numpy as np

# make text reasonably sized
plt.rc('font', **{'size': 18})


data = {
    'p_verd': np.linspace(1.7, 3.25, 10),
    'p_kond': np.linspace(35, 45, 10),
    'T_kond': np.linspace(101, 110, 10)
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
    c1.set_attr(p=p)
    nw.solve('design')
    ean.analyse(pamb=pamb, Tamb=Tamb)
    eta['p_verd'] += [ean.network_data.loc['epsilon']]

# reset to base temperature
c1.set_attr(p=2.8)

for p in data['p_kond']:
    c3.set_attr(p=p)
    nw.solve('design')
    ean.analyse(pamb=pamb, Tamb=Tamb)
    eta['p_kond'] += [ean.network_data.loc['epsilon']]

# reset to base pressure
c3.set_attr(p=35)

for T in data['T_kond']:
    c3.set_attr(T=T)
    nw.solve('design')
    ean.analyse(pamb=pamb, Tamb=Tamb)
    eta['T_kond'] += [ean.network_data.loc['epsilon']]

c3.set_attr(T=105)

fig, ax = plt.subplots(1, 3, sharey=True, figsize=(16, 8))

[a.grid() for a in ax]

i = 0
for key in data:
    ax[i].scatter(data[key], eta[key], s=100, color="#1f567d")
    ax[i].set_xlabel(description[key])
    i += 1

ax[0].set_ylabel('eta of the Heat Pump')

plt.tight_layout()
plt.show()
#fig.savefig('Optimierung_IHX_R601.svg')