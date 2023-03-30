from tespy.networks import Network
from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink, Merge, DropletSeparator)
from tespy.connections import Connection, Bus
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
from fluprodia import FluidPropertyDiagram
import math

wf = 'REFPROP::Pentane'
si = 'H2O'
fld_wf = {wf: 1, si: 0}
fld_si = {wf: 0, si: 1}

nw = Network(fluids=[wf, si], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

# Components

gc = HeatExchanger('Gas cooler')
ev = HeatExchanger('Evaporator')
va_1 = Valve('Valve 1')
va_2 = Valve('Valve 2')
cp_1 = Compressor('Compressor 1')
cp_2 = Compressor('Compressor 2')
ihx = HeatExchanger("Internal Heat Exchanger")
fl = DropletSeparator('Flash Tank')
mg = Merge('Merge', num_in=2)

#Sources, Sinks and CycleCloser

si_in = Source('Sink in')
si_out = Sink('Sink out')

sou_in = Source('Source in')
sou_out = Sink('Source out')
sou_cool = Source('Source Cooling')
si_cool = Sink('Sink Cooling')

cc = CycleCloser('CycleCloser')


# Connections Cycle
c1 = Connection(ihx, 'out2', cp_1, 'in1', label="1")
c2 = Connection(cp_1, 'out1', mg, 'in1', label="2")
c3 = Connection(fl, 'out2', mg, 'in2', label="3")
c4 = Connection(mg, 'out1', cp_2, 'in1', label="4")
c4cc = Connection(cp_2, 'out1', cc, 'in1', label="4cc")
c5 = Connection(cc, 'out1', gc, 'in1', label="5")
c6 = Connection(gc, 'out1', ihx, 'in1', label="6")
c7 = Connection(ihx, 'out1', va_1, 'in1', label="7")
c8 = Connection(va_1, 'out1', fl, 'in1', label="8")
c9 = Connection(fl, 'out1', va_2, 'in1', label="9")
c10 = Connection(va_2, 'out1', ev, 'in2', label="10")
c11 = Connection(ev, 'out2', ihx, 'in2', label="11")

# Connections Sink
c12 = Connection(si_in, 'out1', gc, 'in2', label="12")
c13 = Connection(gc, 'out2', si_out, 'in1', label="13")

#Connection Source
c14 = Connection(sou_in, 'out1', ev, 'in1', label="14")
c15 = Connection(ev, 'out1', sou_out, 'in1', label="15")

nw.add_conns(c1, c2, c3, c4, c4cc, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15)

# Starting Parameters Components
gc.set_attr(pr1=1, pr2=1, Q=-1e7)
ihx.set_attr(pr1=1, pr2=1)
ev.set_attr(pr1=1, pr2=1)
cp_1.set_attr(eta_s=0.76)
cp_2.set_attr(eta_s=0.76)

# Starting Parameters Connections Cycle
h_c1 = CPSI("H", "P", 4.706 * 1e5, "T", 273.15+155, wf) * 1e-3
c1.set_attr(h=h_c1, p=4.706, fluid={'Pentane': 1, 'H2O': 0})

c2.set_attr(p=8)

h_c6 = CPSI("H", "P", 26 * 1e5, "T", 273.15+169, wf) * 1e-3
c6.set_attr(h=h_c6, p=26)

h_c11 = CPSI("H", "P", 4.706 * 1e5, "T", 273.15+90.1, wf) * 1e-3
c11.set_attr(h=h_c11)

c12.set_attr(T=168, p=35, fluid={'Pentane': 0, 'H2O': 1})
c13.set_attr(T=190)

# Starting Parameters Connection Source
c14.set_attr(T=95, p=5, fluid={'Pentane': 0, 'H2O': 1})
c15.set_attr(T=90)

#Solve Model
nw.solve(mode='design')
nw.print_results()

#Final Parameters
c1.set_attr(p=None, h=None)
ev.set_attr(ttd_l=5)
ihx.set_attr(ttd_u=15)
c2.set_attr(p=5)
c6.set_attr(h=None, p=29)
gc.set_attr(ttd_l=10)
c11.set_attr(h=None, Td_bp=0.1)

# busses
power = Bus('power')
power.add_comps(
    {'comp': cp_1, 'char': 1, 'base': 'bus'},
    {'comp': cp_2, 'char': 1, 'base': 'bus'})

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
        {'comp': cp_1, 'char': -1, 'base': 'bus'},
        {'comp': cp_2, 'char': -1, 'base': 'bus'}
)

heat_product_COP = Bus('heat_product_COP')
heat_product_COP.add_comps(
            {"comp": gc, "char": 1})

nw.add_busses(power, heat_source, heat_product, power_COP, heat_product_COP)

#Solve Model
nw.solve(mode='design')
nw.print_results()

print('COP', heat_product_COP.P.val / power_COP.P.val)

# Exergy Analysis
pamb = 1
Tamb = 25

ean = ExergyAnalysis(nw, E_P=[heat_product], E_F=[power, heat_source])
ean.analyse(pamb=pamb, Tamb=Tamb)
ean.print_results()
print(ean.network_data.loc['epsilon'])

#log p,h- diagram

result_dict = {}
result_dict.update({ev.label: ev.get_plotting_data()[2]})
result_dict.update({ihx.label: ihx.get_plotting_data()[2]})
result_dict.update({cp_1.label: cp_1.get_plotting_data()[1]})
result_dict.update({fl.label: fl.get_plotting_data()[2]})
result_dict.update({mg.label: mg.get_plotting_data()[1]})
result_dict.update({cp_2.label: cp_2.get_plotting_data()[1]})
result_dict.update({gc.label: gc.get_plotting_data()[1]})
result_dict.update({ihx.label: ihx.get_plotting_data()[1]})
result_dict.update({va_1.label: va_1.get_plotting_data()[1]})
result_dict.update({fl.label: fl.get_plotting_data()[1]})
result_dict.update({va_2.label: va_2.get_plotting_data()[1]})

diagram = FluidPropertyDiagram('Pentane')
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

diagram.save('Test.png', dpi=300)

#COP, eta, Lorenz-COP and E_D - high pressure diagrams
import matplotlib.pyplot as plt
import numpy as np

# make text reasonably sized
plt.rc('font', **{'size': 18})
iterations = 20

#bei Veränderung der minimalen Temeraturdifferenzen beim Gaskühler muss der Druckbereich gegebenfalls verkleinert werden
data = {
    'p_kond': np.linspace(29, 35, iterations)
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
    c6.set_attr(p=p)
    nw.solve('design')
    ean.analyse(pamb=pamb, Tamb=Tamb)
    COP['p_kond'] += [nw.busses["heat_product_COP"].P.val / nw.busses["power_COP"].P.val]
    eta['p_kond'] += [ean.network_data.loc['epsilon'] * 100]
    T_Hi = nw.get_conn("12").get_attr("T").val + 273.15
    T_Ho = nw.get_conn("13").get_attr("T").val + 273.15
    T_Ci = nw.get_conn("14").get_attr("T").val + 273.15
    T_Co = nw.get_conn("15").get_attr("T").val + 273.15
    diff_T_H = (T_Ho-T_Hi) / math.log(T_Ho / T_Hi)
    diff_T_C = (T_Ci-T_Co) / math.log(T_Ci / T_Co)
    Lorenz_COP['p_kond'] += [diff_T_H / (diff_T_H - diff_T_C)]


fig, ax = plt.subplots(1, 3, figsize=(16, 8))
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
fig.savefig('Optimierung Zwischenkühlung eta, COP, Lorenz-COP R601.svg')

dat = tuple(data['p_kond'])
E_D_Lists = {}
for name in ['Gas cooler', 'Evaporator', 'Valve 1', 'Valve 2', 'Compressor 1', 'Compressor 2',
             'Internal Heat Exchanger', 'Merge']:
    E_D_List = []
    for p in data['p_kond']:
        c6.set_attr(p=p)
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
ax.legend(loc='lower right')

plt.show()
fig.savefig('Optimierung Zwischenkühlung Exergievernichtung R601.svg')

import json

"""data = {
    'p_kond': list(np.linspace(25, 35, iterations))
}

with open('Zweistufenkompression.txt', 'w') as convert_file:
    convert_file.write(json.dumps(data)+"\n")

with open('Zweistufenkompression.txt', 'a') as convert_file:
    convert_file.write(json.dumps(COP)+"\n")

with open('Zweistufenkompression.txt', 'a') as convert_file:
    convert_file.write(json.dumps(eta)+"\n")

f = open("Zweistufenkompression.txt", "r")
print(f.read())"""