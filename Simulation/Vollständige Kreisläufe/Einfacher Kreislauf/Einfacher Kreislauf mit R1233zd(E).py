from tespy.networks import Network
from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink)
from tespy.connections import Connection, Bus
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
from fluprodia import FluidPropertyDiagram
import math
import plotly.graph_objects as go

wf = 'REFPROP::R1233ZD(E)'
si = 'H2O'
fld_wf = {wf: 1, si: 0}
fld_si = {wf: 0, si: 1}

nw = Network(fluids=[wf, si], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

# Components
gc = HeatExchanger('Gaskühler')
ev = HeatExchanger('Verdampfer')
sup = HeatExchanger('Superheater')
va = Valve('Drossel')
cp = Compressor('Kompressor')

#Sources, Sinks and CycleCloser
si_in = Source('Sink in')
si_out = Sink('Sink out')

sou_in = Source('Source in')
sou_out = Sink('Source out')

cc = CycleCloser('CycleCloser')

# Connections Cycle
c21 = Connection(cc, 'out1', gc, 'in1', label="21")
c22 = Connection(gc, 'out1', va, 'in1', label="22")
c23 = Connection(va, 'out1', ev, 'in2', label="23")
c24 = Connection(ev, 'out2', cp, 'in1', label="24")
c21_cc = Connection(cp, 'out1', cc, 'in1', label="21_cc")

# Connections Source
c11 = Connection(sou_in, 'out1', ev, 'in1', label="11")
c12 = Connection(ev, 'out1', sou_out, 'in1', label="12")

# Connections Sink
c13 = Connection(si_in, 'out1', gc, 'in2', label="13")
c14 = Connection(gc, 'out2', si_out, 'in1', label="14")

nw.add_conns(c21, c22, c23, c24, c21_cc, c11, c12, c13, c14)


# Starting Parameters Components
gc.set_attr(pr1=1, pr2=1, Q=-1e7)
ev.set_attr(pr1=1, pr2=1)
cp.set_attr(eta_s=0.76)

# Starting Parameters Connections Cycle
h_c22 = CPSI("H", "P", 57 * 1e5, "T", 273.15+165, wf) * 1e-3
c22.set_attr(h=h_c22, p=57)

c23.set_attr(p=8.334)

h_c24 = CPSI("H", "P", 8.334 * 1e5, "T", 273.15+90.1, wf) * 1e-3
c24.set_attr(h=h_c24, fluid={'R1233ZD(E)': 1, 'H2O': 0})

# Starting Parameters Connection Source
c11.set_attr(T=95, p=5, fluid={'R1233ZD(E)': 0, 'H2O': 1})
c12.set_attr(T=90)

# Starting Parameters Connection Sink
c13.set_attr(T=160, p=20, fluid={'R1233ZD(E)': 0, 'H2O': 1})
c14.set_attr(T=190)


#Solve Model
nw.solve(mode='design')
nw.print_results()

#Final Parameters
c22.set_attr(h=None, p=80.18)
gc.set_attr(ttd_l=10)
c23.set_attr(p=None)
ev.set_attr(ttd_l=5)
c24.set_attr(h=None, Td_bp=0.1)

# busses
power = Bus('power')
power.add_comps(
    {'comp': cp, 'char': 1, 'base': 'bus'})

heat_source = Bus('Wärmequelle')
heat_source.add_comps(
    {'comp': sou_in, 'base': 'bus'},
    {'comp': sou_out})

heat_product = Bus('Wärmesenke')
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

nw.solve(mode='design')
nw.print_results()
print('COP', heat_product_COP.P.val / power_COP.P.val)

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


diagram.save('logph_R1233zd(E).png', dpi=300)

# grassmann diagram

links, nodes = ean.generate_plotly_sankey_input()
fig = go.Figure(go.Sankey(
    arrangement="snap",
    node={
        "label": nodes,
        'pad': 11,
        'color': 'orange'},
    link=links),
    layout=go.Layout({'width': 1450})
    )
fig.update_layout(
    #title_text="Basic Sankey Diagram",
    #font_family="Courier New",
    #font_color="blue",
    font_size=20,
    #title_font_family="Times New Roman",
    #title_font_color="red",
)
fig.show()

#COP, eta, Lorenz-COP and E_D - high pressure diagrams
import matplotlib.pyplot as plt
import numpy as np

# make text reasonably sized
plt.rc('font', **{'size': 18})
iterations = 30

#bei Veränderung der minimalen Temeraturdifferenzen beim Gaskühler muss der Druckbereich gegebenfalls verkleinert werden
data = {
    'p_kond': np.linspace(50, 110, iterations)
}

COP = {
    'p_kond': []
}

eta = {
    'p_kond': []
}
e_d_ev = []
e_d_ihx = []
e_d_va = []
e_d_cp = []
e_d_gc = []
pkond = []
Lorenz_COP = {
    'p_kond': []
}
description = {
    'p_kond': 'Kondensatordruck in bar',
}

for p in data['p_kond']:
    c22.set_attr(p=p)
    nw.solve('design')
    ean.analyse(pamb=pamb, Tamb=Tamb)
    COP['p_kond'] += [nw.busses["heat_product_COP"].P.val / nw.busses["power_COP"].P.val]
    eta['p_kond'] += [ean.network_data.loc['epsilon'] * 100]
    T_Hi = nw.get_conn("13").get_attr("T").val + 273.15
    T_Ho = nw.get_conn("14").get_attr("T").val + 273.15
    T_Ci = nw.get_conn("11").get_attr("T").val + 273.15
    T_Co = nw.get_conn("12").get_attr("T").val + 273.15
    diff_T_H = (T_Ho-T_Hi) / math.log(T_Ho / T_Hi)
    diff_T_C = (T_Ci-T_Co) / math.log(T_Ci / T_Co)
    Lorenz_COP['p_kond'] += [diff_T_H / (diff_T_H - diff_T_C)]
    e_d_ev += [ean.component_data['epsilon']['Evaporator'] * 100]
    e_d_va += [ean.component_data['epsilon']['Valve'] * 100]
    e_d_cp += [ean.component_data['epsilon']['Compressor'] * 100]
    e_d_gc += [ean.component_data['epsilon']['Gas cooler'] * 100]
    pkond += [nw.get_conn("22").get_attr("p").val]
    print('Massenstrom Kreislauf', nw.get_conn("22").get_attr("m").val)
    print('Massenstrom Quelle', nw.get_conn("11").get_attr("m").val)
    print('Massenstrom Senke', nw.get_conn("13").get_attr("m").val)
    print('Kompressorleistung=', nw.get_comp('Compressor').get_attr('P').val)
    print('Drossel =', ean.component_data['E_D']['Valve'] * 1e-3)
    print('Gaskühler =', ean.component_data['E_D']['Gas cooler'] * 1e-3)
    print('Gaskühler Wirkungsgrad =', ean.component_data['epsilon']['Gas cooler'] * 100)
    print('Kompressor =', ean.component_data['E_D']['Compressor'] * 1e-3)
    print('Kompressor Wirkungsgrad =', ean.component_data['epsilon']['Compressor'] * 100)
    print('Verdampfer =', ean.component_data['E_D']['Evaporator'] * 1e-3)
    print('epsilon = ', ean.network_data.loc['epsilon'] * 100)
    print('E_D gesamt = ', ean.network_data.loc['E_D'] * 1e-3)
    print('E_F gesamt = ', ean.network_data.loc['E_F'] * 1e-3)
    print('COP = ', heat_product_COP.P.val / power_COP.P.val)
    print('Verdampfer =', ean.component_data['E_F']['Evaporator'] * 1e-3)
    print('Verdampferleistung', nw.get_comp('Evaporator').get_attr('Q').val * 1e-3)


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
fig.savefig('Optimierung eta, COP, Lorenz-COP R1233ZD(E).svg')


plt.plot(pkond, e_d_va, color='red')
plt.plot(pkond, e_d_ev, color='blue')
plt.plot(pkond, e_d_cp, color='green')
plt.plot(pkond, e_d_gc, color='brown')
plt.show()
dat = tuple(data['p_kond'])
E_D_Lists = {}
for name in ['Valve']:
    E_D_List = []
    for p in data['p_kond']:
        c22.set_attr(p=p)
        nw.solve('design')
        ean.analyse(pamb=pamb, Tamb=Tamb)
        E_D_List += [ean.component_data['y_Dk'][name]]

    E_D_Lists[name] = E_D_List


width = 0.2

fig, ax = plt.subplots()
bottom = np.zeros(iterations)

for boolean, E_D_List in E_D_Lists.items():
    p = ax.bar(dat, E_D_List, width, label=boolean, bottom=bottom)
    bottom += E_D_List

ax.set_xlabel('Kondensatordruck in bar')
ax.set_ylabel('Exergievernichtungsquotient')
ax.legend(loc='lower right')
#plt.ylim(310 * 1e3, 330 * 1e3)

plt.show()
fig.savefig('Optimierung Exergievernichtung R1233ZD(E).svg')

import json

"""data = {
    'p_kond': list(np.linspace(48, 91, iterations))
}

with open('Einfacher Kreislauf.txt', 'a') as convert_file:
    convert_file.write(json.dumps(data)+"\n")

with open('Einfacher Kreislauf.txt', 'a') as convert_file:
    convert_file.write(json.dumps(COP)+"\n")

with open('Einfacher Kreislauf.txt', 'a') as convert_file:
    convert_file.write(json.dumps(eta)+"\n")

f = open("Einfacher Kreislauf.txt", "r")
print(f.read())"""

