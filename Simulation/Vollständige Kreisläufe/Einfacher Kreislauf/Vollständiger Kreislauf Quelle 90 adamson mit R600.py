from tespy.networks import Network
from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink)
from tespy.connections import Connection, Bus
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
from fluprodia import FluidPropertyDiagram

wf = 'R600'
si = 'H2O'
fld_wf = {wf: 1, si: 0}
fld_si = {wf: 0, si: 1}

nw = Network(fluids=[wf, si], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

# Components

gc = HeatExchanger('Gas cooler')
ev = HeatExchanger('Evaporator')
sup = HeatExchanger('Superheater')
va = Valve('Valve')
cp = Compressor('Compressor')

#Sources, Sinks and CycleCloser

si_in = Source('Sink in')
si_out = Sink('Sink out')

sou_in = Source('Source in')
sou_out = Sink('Source out')

cc = CycleCloser('CycleCloser')

# Connections Cycle

c1 = Connection(cc, 'out1', gc, 'in1', label="1")
c2 = Connection(gc, 'out1', va, 'in1', label="2")
c3 = Connection(va, 'out1', ev, 'in2', label="3")
c4 = Connection(ev, 'out2', sup, 'in2', label="4")
c5 = Connection(sup, 'out2', cp, 'in1', label="5")
c6 = Connection(cp, 'out1', cc, 'in1', label="6")

# Connections Sink

c7 = Connection(si_in, 'out1', gc, 'in2', label="7")
c8 = Connection(gc, 'out2', si_out, 'in1', label="8")

# Connections Source

c9 = Connection(sou_in, 'out1', sup, 'in1', label="9")
c10 = Connection(sup, 'out1', ev, 'in1', label="10")
c11 = Connection(ev, 'out1', sou_out, 'in1', label="11")
nw.add_conns(c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11)

# Starting Parameters Components

gc.set_attr(pr1=1, pr2=1)
ev.set_attr(pr1=1, pr2=1)
sup.set_attr(pr1=1, pr2=1)
cp.set_attr(eta_s=0.7)

# Starting Parameters Connections Cycle
h_gk_vor = CPSI("H", "P", 93 * 1e5, "T", 273.15+205, wf) * 1e-3
#c1.set_attr(h=h_gk_vor)

h_gk_nach = CPSI("H", "P", 93 * 1e5, "T", 273.15+105, wf) * 1e-3
c2.set_attr(h=h_gk_nach, p=93)

#h_verd = CPSI("H", "Q", 0, "T", 273.15+70, km) * 1e-3
c3.set_attr(p=8.1)

h_zw = CPSI("H", "Q", 1, "T", 273.15+70.05, wf) * 1e-3
c4.set_attr(h=h_zw)

h_uebe = CPSI("H", "P", 8.1 * 1e5, "T", 273.15+75, wf) * 1e-3
c5.set_attr(h=h_uebe, fluid=fld_wf)

# Starting Parameters Connection Sink
c7.set_attr(T=100, p=20, fluid=fld_si)
c8.set_attr(T=200)

# Starting Parameters Connection Source
c9.set_attr(T=80, m=5, p=5, fluid=fld_si)
c11.set_attr(T=75)

#Solve Model
nw.solve(mode='design')
nw.print_results()

# New Parameters
#c1.set_attr(h=None, T=204)
c2.set_attr(h=None, T=100.0175, p=57.1529)
c3.set_attr(p=9.0614)
c4.set_attr(h=None, x=1)
c5.set_attr(h=None, Td_bp=5)
c8.set_attr(T=None)
gc.set_attr(ttd_u=5)


# busses
power = Bus('power input')
power.add_comps(
    {'comp': cp, 'char': 1, 'base': 'bus'},
    {'comp': sou_in, 'base': 'bus'},
    {'comp': sou_out})


heat_product = Bus('heating')
heat_product.add_comps(
    {'comp': si_in, 'base': 'bus'},
    {'comp': si_out})

power_COP = Bus('power')
power_COP.add_comps(
        {'comp': cp, 'char': -1, 'base': 'bus'}
)

heat_product_COP = Bus('heat_product')
heat_product_COP.add_comps(
            {"comp": gc, "char": 1})

nw.add_busses(power, heat_product, power_COP, heat_product_COP)


nw.solve(mode='design')
nw.print_results()

#Exergy Analysis
pamb = 1
Tamb = 25

ean = ExergyAnalysis(nw, E_P=[heat_product], E_F=[power])
ean.analyse(pamb=pamb, Tamb=Tamb)
ean.print_results()
print(ean.network_data.loc['epsilon'])
#funktioniert noch nicht ganz mit dem Ersetzen der Enthalpien
#70 °C Problem, muss um mindestens 0,05 °C größer sein
#zweites Szenario funktioniert leider nicht

#log p,h diagram

result_dict = {}
result_dict.update({ev.label: ev.get_plotting_data()[2]})
result_dict.update({sup.label: sup.get_plotting_data()[2]})
result_dict.update({cp.label: cp.get_plotting_data()[1]})
result_dict.update({gc.label: gc.get_plotting_data()[1]})
result_dict.update({va.label: va.get_plotting_data()[1]})

diagram = FluidPropertyDiagram(wf)
diagram.set_unit_system(T='°C', p='bar', h='kJ/kg')

for key, data in result_dict.items():
    result_dict[key]['datapoints'] = diagram.calc_individual_isoline(**data)

diagram.calc_isolines()
diagram.set_limits(x_min=0, x_max=800, y_min=1e-1, y_max=2e2)
diagram.draw_isolines('logph')

for key in result_dict.keys():
    datapoints = result_dict[key]['datapoints']
    diagram.ax.plot(datapoints['h'], datapoints['p'], color='#ff0000')
    diagram.ax.scatter(datapoints['h'][0], datapoints['p'][0], color='#ff0000')


diagram.save('logph_R600.png', dpi=300)

#Parameter optmization
import matplotlib.pyplot as plt
import numpy as np

# make text reasonably sized
plt.rc('font', **{'size': 18})


data = {
    'p_verd': np.linspace(8.1, 9.1, 15),
    'p_kond': np.linspace(56, 98, 20),
    'T_kond': np.linspace(100.0061, 110, 10),
}
eta = {
    'p_verd': [],
    'p_kond': [],
    'T_kond': []
}
description = {
    'p_verd': 'Verdampferdruck in bar',
    'p_kond': 'Kondensatordruck in bar',
    'T_kond': 'Kondensatortemperatur in °C'
}

for p in data['p_verd']:
    c3.set_attr(p=p)
    nw.solve('design')
    ean.analyse(pamb=pamb, Tamb=Tamb)
    eta['p_verd'] += [ean.network_data.loc['epsilon']]

# reset to base pressure
c3.set_attr(p=8.1)

for p in data['p_kond']:
    c2.set_attr(p=p)
    nw.solve('design')
    ean.analyse(pamb=pamb, Tamb=Tamb)
    eta['p_kond'] += [ean.network_data.loc['epsilon']]

# reset to base temperature
c2.set_attr(p=93)

for T in data['T_kond']:
    c2.set_attr(T=T)
    nw.solve('design')
    ean.analyse(pamb=pamb, Tamb=Tamb)
    eta['T_kond'] += [ean.network_data.loc['epsilon']]

fig, ax = plt.subplots(1, 3, sharey=True, figsize=(16, 8))

[a.grid() for a in ax]

i = 0
for key in data:
    ax[i].scatter(data[key], eta[key], s=100, color="#1f567d")
    ax[i].set_xlabel(description[key])
    i += 1

ax[0].set_ylabel('eta of the heat pump')

plt.tight_layout()

fig.savefig('Optimierung R600.svg')