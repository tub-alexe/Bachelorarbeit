from tespy.networks import Network
from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink)
from tespy.connections import Connection, Bus
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
from fluprodia import FluidPropertyDiagram

wf = 'REFPROP::R1233ZD(E)'
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
ihx = HeatExchanger("Internal Heat Exchanger")

#Sources, Sinks and CycleCloser

si_in = Source('Sink in')
si_out = Sink('Sink out')

sou_in = Source('Source in')
sou_out = Sink('Source out')

cc = CycleCloser('CycleCloser')


# Connections Cycle
c1 = Connection(ihx, 'out2', cp, 'in1')
c2cc = Connection(cp, 'out1', cc, 'in1')
c2 = Connection(cc, 'out1', gc, 'in1')
c3 = Connection(gc, 'out1', ihx, 'in1')
c4 = Connection(ihx, 'out1', va, 'in1')
c5 = Connection(va, 'out1', ev, 'in2')
c5_ue = Connection(ev, 'out2', sup, 'in2')
c6 = Connection(sup, 'out2', ihx, 'in2')


# Connections Sink
c7 = Connection(si_in, 'out1', gc, 'in2')
c8 = Connection(gc, 'out2', si_out, 'in1')

# Connections Source
c9 = Connection(sou_in, 'out1', sup, 'in1')
c10 = Connection(sup, 'out1', ev, 'in1')
c11 = Connection(ev, 'out1', sou_out, 'in1')

nw.add_conns(c1, c2, c2cc, c3, c4, c5, c5_ue, c6, c7, c8, c9, c10, c11)

# Starting Parameters Components
gc.set_attr(pr1=1, pr2=1, Q=-1e7)
ihx.set_attr(pr1=1, pr2=1)
ev.set_attr(pr1=1, pr2=1)
sup.set_attr(pr1=1, pr2=1)
cp.set_attr(eta_s=0.76)

# Starting Parameters Connections Cycle
h_ihx_h_nach = CPSI("H", "P", 8.33 * 1e5, "T", 273.15+160, wf) * 1e-3
c1.set_attr(h=h_ihx_h_nach, p=8.33, fluid={'R1233ZD(E)': 1, 'H2O': 0})


h_ihx_k_vor = CPSI("H", "P", 44 * 1e5, "T", 273.15+165, wf) * 1e-3
c3.set_attr(h=h_ihx_k_vor, p=44)

h_zw = CPSI("H", "P", 8.33 * 1e5, "T", 273.15+90, wf) * 1e-3
c5_ue.set_attr(h=h_zw)

h_ihx_k_nach = CPSI("H", "P", 8.33 * 1e5, "T", 273.15+90.1, wf) * 1e-3
c6.set_attr(h=h_ihx_k_nach)

# Starting Parameters Connection Sink
c7.set_attr(T=160, p=20, fluid={'R1233ZD(E)': 0, 'H2O': 1})
c8.set_attr(T=200)

# Starting Parameters Connection Source
c9.set_attr(T=95, p=5, fluid={'R1233ZD(E)': 0, 'H2O': 1})
c11.set_attr(T=90)

#Solve Model
nw.solve(mode='design')
nw.print_results()
print(f'COP = {abs(gc.Q.val) / cp.P.val}')

# New Parameters
c1.set_attr(p=8.33, h=None)
ihx.set_attr(ttd_u=5)
c3.set_attr(h=None, p=44, T=165)
c5_ue.set_attr(h=None, x=1)
c6.set_attr(h=None, Td_bp=0.1)
c8.set_attr(T=None)
gc.set_attr(ttd_u=39)

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

nw.add_busses(power, heat_product, power_COP, heat_product_COP)

nw.solve(mode='design')
nw.print_results()
print('COP', heat_product_COP.P.val / power_COP.P.val)
print('COP', nw.busses["heat_product_COP"].P.val / nw.busses["power_COP"].P.val)

# Implementierung Exergie Analyse

pamb = 1
Tamb = 25

ean = ExergyAnalysis(nw, E_P=[heat_product], E_F=[power, heat_source])
ean.analyse(pamb=pamb, Tamb=Tamb)
ean.print_results()
print(ean.network_data.loc['epsilon'])

#log p,h

result_dict = {}
result_dict.update({ev.label: ev.get_plotting_data()[2]})
result_dict.update({sup.label: sup.get_plotting_data()[2]})
result_dict.update({ihx.label: ihx.get_plotting_data()[2]})
result_dict.update({cp.label: cp.get_plotting_data()[1]})
result_dict.update({gc.label: gc.get_plotting_data()[1]})
result_dict.update({ihx.label: ihx.get_plotting_data()[1]})
result_dict.update({va.label: va.get_plotting_data()[1]})

diagram = FluidPropertyDiagram('R1233ZD(E)')
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


diagram.save('logph_IHX_R601.png', dpi=300)

#parameter optimization
import matplotlib.pyplot as plt
import numpy as np

# make text reasonably sized
plt.rc('font', **{'size': 18})


data = {
    'p_kond': np.linspace(36, 50, 40)
}
COP = {
    'p_kond': []
}
description = {
    'p_kond': 'Kondensatordruck in bar',
}

for p in data['p_kond']:
    c3.set_attr(p=p)
    nw.solve('design')
    nw.print_results()
    ean.analyse(pamb=pamb, Tamb=Tamb)
    COP['p_kond'] += [nw.busses["heat_product_COP"].P.val / nw.busses["power_COP"].P.val]


fig, ax = plt.subplots(1, 2, sharey=True, figsize=(16, 8))

[a.grid() for a in ax]

i = 0
for key in data:
    ax[i].scatter(data[key], COP[key], s=100, color="#1f567d")
    ax[i].set_xlabel(description[key])
    i += 1

ax[0].set_ylabel('COP of the Heat Pump')

plt.tight_layout()
plt.show()
fig.savefig('Optimierung COP R1233ZD(E).svg')

c3.set_attr(p=44)

# make text reasonably sized
plt.rc('font', **{'size': 18})


data = {
    'p_kond': np.linspace(36, 50, 40)
}
eta = {
    'p_kond': []
}
description = {
    'p_kond': 'Kondensatordruck in bar',
}

for p in data['p_kond']:
    c3.set_attr(p=p)
    nw.solve('design')
    ean.analyse(pamb=pamb, Tamb=Tamb)
    eta['p_kond'] += [ean.network_data.loc['epsilon'] * 100]


fig, ax = plt.subplots(1, 2, sharey=True, figsize=(16, 8))

[a.grid() for a in ax]

i = 0
for key in data:
    ax[i].scatter(data[key], eta[key], s=100, color="#1f567d")
    ax[i].set_xlabel(description[key])
    i += 1

ax[0].set_ylabel('eta of the Heat Pump')

plt.tight_layout()
plt.show()
fig.savefig('Optimierung eta R1233ZD(E).svg')