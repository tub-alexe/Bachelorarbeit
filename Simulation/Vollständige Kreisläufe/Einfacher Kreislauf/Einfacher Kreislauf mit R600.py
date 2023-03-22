from tespy.networks import Network
from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink)
from tespy.connections import Connection, Bus
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
from fluprodia import FluidPropertyDiagram
import math

wf = 'REFPROP::Butane'
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
c4 = Connection(ev, 'out2', cp, 'in1', label="4")
c5 = Connection(cp, 'out1', cc, 'in1', label="5")

# Connections Sink

c6 = Connection(si_in, 'out1', gc, 'in2', label="6")
c7 = Connection(gc, 'out2', si_out, 'in1', label="7")

# Connections Source

c8 = Connection(sou_in, 'out1', ev, 'in1', label="8")
c9 = Connection(ev, 'out1', sou_out, 'in1', label="9")
nw.add_conns(c1, c2, c3, c4, c5, c6, c7, c8, c9)

# Starting Parameters Components
gc.set_attr(pr1=1, pr2=1, Q=-1e7)
ev.set_attr(pr1=1, pr2=1)
sup.set_attr(pr1=1, pr2=1)
cp.set_attr(eta_s=0.76)

# Starting Parameters Connections Cycle
h_c2 = CPSI("H", "P", 93 * 1e5, "T", 273.15+165, wf) * 1e-3
c2.set_attr(h=h_c2, p=93)

c3.set_attr(p=12.492)

h_c4 = CPSI("H", "P", 12.492 * 1e5, "T", 273.15+90.1, wf) * 1e-3
c4.set_attr(h=h_c4, fluid={'Butane': 1, 'H2O': 0})

# Starting Parameters Connection Sink
c6.set_attr(T=160, p=30, fluid={'Butane': 0, 'H2O': 1})
c7.set_attr(T=200)

# Starting Parameters Connection Source
c8.set_attr(T=95, p=5, fluid={'Butane': 0, 'H2O': 1})
c9.set_attr(T=90)

#Solve Model
nw.solve(mode='design')
nw.print_results()

#Final Parameters
c2.set_attr(h=None, p=93)
gc.set_attr(ttd_l=5)
c3.set_attr(p=None)
ev.set_attr(ttd_l=5)
c4.set_attr(h=None, Td_bp=0.1)

# busses
power = Bus('power')
power.add_comps(
    {'comp': cp, 'char': 1, 'base': 'bus'})

heat_source = Bus('heat_source')
heat_source.add_comps(
    {'comp': sou_in, 'base': 'bus'},
    {'comp': sou_out})

heat_product = Bus('heat_product')
heat_product.add_comps(
    {'comp': si_in, 'base': 'bus'},
    {'comp': si_out})


power_COP = Bus('power_COP')
power_COP.add_comps(
        {'comp': cp, 'char': -1, 'base': 'bus'}
)

heat_product_COP = Bus('heat_product_COP')
heat_product_COP.add_comps(
            {"comp": gc, "char": 1})

nw.add_busses(power, heat_product, heat_source, power_COP, heat_product_COP)

#Solve Model
nw.solve(mode='design')
nw.print_results()

#Exergy Analysis
pamb = 1
Tamb = 25

ean = ExergyAnalysis(nw, E_P=[heat_product], E_F=[power, heat_source])
ean.analyse(pamb=pamb, Tamb=Tamb)
ean.print_results()
print(ean.network_data.loc['epsilon'])

#log p,h diagram
result_dict = {}
result_dict.update({ev.label: ev.get_plotting_data()[2]})
result_dict.update({cp.label: cp.get_plotting_data()[1]})
result_dict.update({gc.label: gc.get_plotting_data()[1]})
result_dict.update({va.label: va.get_plotting_data()[1]})

diagram = FluidPropertyDiagram('Butane')
diagram.set_unit_system(T='°C', p='bar', h='kJ/kg')

for key, data in result_dict.items():
    result_dict[key]['datapoints'] = diagram.calc_individual_isoline(**data)

diagram.calc_isolines()
diagram.set_limits(x_min=0, x_max=1000, y_min=1e-1, y_max=2e2)
diagram.draw_isolines('logph')

for key in result_dict.keys():
    datapoints = result_dict[key]['datapoints']
    diagram.ax.plot(datapoints['h'], datapoints['p'], color='#ff0000')
    diagram.ax.scatter(datapoints['h'][0], datapoints['p'][0], color='#ff0000')


diagram.save('logph_R600.png', dpi=300)

#COP, eta, Lorenz-COP and E_D - high pressure diagrams
import matplotlib.pyplot as plt
import numpy as np

# make text reasonably sized
plt.rc('font', **{'size': 18})
iterations = 20

#bei Veränderung der minimalen Temeraturdifferenzen beim Gaskühler muss der Druckbereich gegebenfalls verkleinert werden
data = {
    'p_kond': np.linspace(93, 145, iterations)
}

COP = {
    'p_kond': []
}

eta = {
    'p_kond': []
}

Lorenz_COP = {
    'p_kond': []
}
description = {
    'p_kond': 'Kondensatordruck in bar',
}

for p in data['p_kond']:
    c2.set_attr(p=p)
    nw.solve('design')
    ean.analyse(pamb=pamb, Tamb=Tamb)
    COP['p_kond'] += [nw.busses["heat_product_COP"].P.val / nw.busses["power_COP"].P.val]
    eta['p_kond'] += [ean.network_data.loc['epsilon'] * 100]
    T_Hi = nw.get_conn("6").get_attr("T").val + 273.15
    T_Ho = nw.get_conn("7").get_attr("T").val + 273.15
    T_Ci = nw.get_conn("8").get_attr("T").val + 273.15
    T_Co = nw.get_conn("9").get_attr("T").val + 273.15
    diff_T_H = (T_Ho-T_Hi) / math.log(T_Ho / T_Hi)
    diff_T_C = (T_Ci-T_Co) / math.log(T_Ci / T_Co)
    Lorenz_COP['p_kond'] += [diff_T_H / (diff_T_H - diff_T_C)]


fig, ax = plt.subplots(1, 3, figsize=(16, 8))
#ax = [ax]
[a.grid() for a in ax]

for i, dictionary in enumerate([COP, eta, Lorenz_COP]):

    for key in data:
        ax[i].scatter(data[key], dictionary[key], s=100, color="#1f567d")
        ax[i].set_xlabel(description[key])

ax[0].set_ylabel('COP of the Heat Pump')
ax[1].set_ylabel('eta of the Heat Pump')
ax[2].set_ylabel('Lorenz-COP of the Heat Pump')

plt.tight_layout()
plt.show()
fig.savefig('Optimierung eta, COP, Lorenz-COP R600.svg')

dat = tuple(data['p_kond'])
E_D_Lists = {}
for name in ['Gas cooler', 'Evaporator', 'Valve', 'Compressor']:
    E_D_List = []
    for p in data['p_kond']:
        c2.set_attr(p=p)
        nw.solve('design')
        ean.analyse(pamb=pamb, Tamb=Tamb)
        E_D_List += [ean.component_data['E_D'][name] * 1e-6]

    E_D_Lists[name] = E_D_List


width = 0.2

fig, ax = plt.subplots()
bottom = np.zeros(iterations)

for boolean, E_D_List in E_D_Lists.items():
    p = ax.bar(dat, E_D_List, width, label=boolean, bottom=bottom)
    bottom += E_D_List

ax.set_xlabel('Kondensatordruck in bar')
ax.set_ylabel('Exergievernichtung in MW')
ax.legend(loc="lower right")

plt.show()
fig.savefig('Optimierung Exergievernichtung R600.svg')