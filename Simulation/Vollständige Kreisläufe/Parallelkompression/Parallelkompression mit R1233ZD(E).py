from tespy.networks import Network
from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink, DropletSeparator, Merge)
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

#Components
fl = DropletSeparator('Phasentrenner')
cp_1 = Compressor('Kompressor 1')
cp_2 = Compressor('Kompressor 2')
va_1 = Valve('Drossel 1')
va_2 = Valve('Drossel 2')
ev = HeatExchanger('Verdampfer')
sup = HeatExchanger('Superheater')
gc = HeatExchanger('Gaskühler')
ihx_1 = HeatExchanger('Interner Wärmeübertrager 1')
ihx_2 = HeatExchanger('Interner Wärmeübertrager 2')
src_wf = Source('Source Working Fluid')
src_wf_2 = Source('Source Working Fluid 2')
snk_wf = Sink('Sink Working Fluid')
snk_wf_2 = Sink('Sink Working Fluid 2')
sou_in = Source('Source in')
sou_out = Sink('Source out')
si_in = Source('Sink in')
si_out = Sink('Sink out')
mg = Merge('Zusammenführung', num_in=2)
cc = CycleCloser('CycleCloser')

#Connections
#Main Cycle
c21 = Connection(cc, 'out1', gc, 'in1', label="21")
c22 = Connection(gc, 'out1', ihx_2, 'in1', label="22")
c23 = Connection(ihx_2, 'out1', va_1, 'in1', label="23")
c24 = Connection(va_1, 'out1', fl, 'in1', label="24")
c25 = Connection(fl, 'out1', ihx_1, 'in1', label="25")
c26 = Connection(ihx_1, 'out1', va_2, 'in1', label="26")
c27 = Connection(va_2, 'out1', ev, 'in2', label="27")
c28 = Connection(ev, 'out2', ihx_1, 'in2', label="28")
c29 = Connection(ihx_1, 'out2', cp_1, 'in1', label="29")
c30 = Connection(cp_1, 'out1', mg, 'in1', label="30")
c31 = Connection(fl, 'out2', ihx_2, 'in2', label="31")
c32 = Connection(ihx_2, 'out2', cp_2, 'in1', label="32")
c33 = Connection(cp_2, 'out1', mg, 'in2', label="33")
c21_cc = Connection(mg, 'out1', cc, 'in1', label="21_cc")



#Source
c11 = Connection(sou_in, 'out1', ev, 'in1', label="11")
c12 = Connection(ev, 'out1', sou_out, 'in1', label="12")

#Sink
c13 = Connection(si_in, 'out1', gc, 'in2', label="13")
c14 = Connection(gc, 'out2', si_out, 'in1', label="14")

nw.add_conns(c21, c22, c23, c24, c25, c26, c27, c28, c29, c30, c31, c32, c33, c21_cc, c11, c12, c13, c14)

#Parameters Components
ev.set_attr(pr1=1, pr2=1)
sup.set_attr(pr1=1, pr2=1)
gc.set_attr(pr1=1, pr2=1, Q=-1e7)
ihx_1.set_attr(pr1=1, pr2=1)
ihx_2.set_attr(pr1=1, pr2=1)
cp_1.set_attr(eta_s=0.76)
cp_2.set_attr(eta_s=0.76)

#Paramters Connections
#Main Cycle
h_c22 = CPSI("H", "P", 48 * 1e5, "T", 273.15 + 165, wf) * 1e-3
c22.set_attr(h=h_c22, p=48)

c24.set_attr(p=29, fluid={'R1233ZD(E)': 1, 'H2O': 0})

c27.set_attr(p=8.334)

h_c28 = CPSI("H", "P", 8.334 * 1e5, "T", 273.15 + 90.1, wf) * 1e-3
c28.set_attr(h=h_c28)

h_c29 = CPSI("H", "P", 8.334 * 1e5, "T", 273.15 + 150, wf) * 1e-3
c29.set_attr(h=h_c29)

h_c32 = CPSI("H", "P", 29 * 1e5, "T", 273.15 + 155, wf) * 1e-3
c32.set_attr(h=h_c32)

# Source
c11.set_attr(T=95, p=10, fluid={'R1233ZD(E)': 0, 'H2O': 1})
c12.set_attr(T=90)

# Sink
c13.set_attr(T=160, p=20, fluid={'R1233ZD(E)': 0, 'H2O': 1})
c14.set_attr(T=190)

#Solve Model
nw.solve(mode='design')
nw.print_results()
#Final Parameters
c22.set_attr(h=None, p=40.49)
gc.set_attr(ttd_l=10)
c24.set_attr(p=24.47)
c27.set_attr(p=None)
ev.set_attr(ttd_l=5)
c28.set_attr(h=None, Td_bp=0.1)
c29.set_attr(h=None)
ihx_1.set_attr(ttd_u=15)
c32.set_attr(h=None)
ihx_2.set_attr(ttd_u=15)


# busses
power = Bus('elektrische Leistung')
power.add_comps(
    {'comp': cp_1, 'char': 1, 'base': 'bus'},
    {'comp': cp_2, 'char': 1, 'base': 'bus'})

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
        {'comp': cp_1, 'char': -1, 'base': 'bus'},
        {'comp': cp_2, 'char': -1, 'base': 'bus'}
)

heat_product_COP = Bus('heat_product_COP')
heat_product_COP.add_comps(
            {"comp": gc, "char": 1})

nw.add_busses(power, heat_source, heat_product, power_COP, heat_product_COP)

nw.solve(mode='design')
nw.print_results()

print('COP', heat_product_COP.P.val / power_COP.P.val)
print(f'COP = {abs(gc.Q.val) / (cp_1.P.val + cp_2.P.val)}')

# Exergy Analysis
pamb = 1
Tamb = 25

ean = ExergyAnalysis(nw, E_P=[heat_product], E_F=[power, heat_source])
ean.analyse(pamb=pamb, Tamb=Tamb)
ean.print_results()
print(ean.network_data.loc['epsilon'] * 100)

#log p,h- diagram
result_dict = {}
result_dict.update({ev.label: ev.get_plotting_data()[2]})
result_dict.update({ihx_1.label: ihx_1.get_plotting_data()[2]})
result_dict.update({cp_1.label: cp_1.get_plotting_data()[1]})
result_dict.update({mg.label: mg.get_plotting_data()[1]})
result_dict.update({gc.label: gc.get_plotting_data()[1]})
result_dict.update({ihx_2.label: ihx_2.get_plotting_data()[1]})
result_dict.update({va_2.label: va_2.get_plotting_data()[1]})
result_dict.update({fl.label: fl.get_plotting_data()[2]})
result_dict.update({ihx_2.label: ihx_2.get_plotting_data()[2]})
result_dict.update({cp_2.label: cp_2.get_plotting_data()[1]})
result_dict.update({mg.label: mg.get_plotting_data()[2]})
result_dict.update({fl.label: fl.get_plotting_data()[1]})
result_dict.update({ihx_1.label: ihx_1.get_plotting_data()[1]})
result_dict.update({va_1.label: va_1.get_plotting_data()[1]})

diagram = FluidPropertyDiagram('R1233ZD(E)')
diagram.set_unit_system(T='°C', p='bar', h='kJ/kg')

for key, data in result_dict.items():
    result_dict[key]['datapoints'] = diagram.calc_individual_isoline(**data)

diagram.calc_isolines()
diagram.set_limits(x_min=0, x_max=900, y_min=1e-1, y_max=2e2)
diagram.draw_isolines('logph')

for key in result_dict.keys():
    datapoints = result_dict[key]['datapoints']
    diagram.ax.plot(datapoints['h'], datapoints['p'], color='#ff0000')
    diagram.ax.scatter(datapoints['h'][0], datapoints['p'][0], color='#ff0000')


diagram.save('logph_Parallel_R1233ZD(E).png', dpi=300)

# grassmann diagram

links, nodes = ean.generate_plotly_sankey_input()
fig = go.Figure(go.Sankey(
    arrangement="snap",
    node={
        "label": nodes,
        'pad': 11,
        'color': 'orange'},
    link=links),
    layout=go.Layout({'width': 1100})
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
#plt.rc('font', **{'size': 18})
iterations = 20

#bei Veränderung der minimalen Temeraturdifferenzen beim Gaskühler muss der Druckbereich gegebenfalls verkleinert werden
data = {
    'p_kond': np.linspace(38.5, 39.5, iterations)
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

"""pkond = []
e_d_ev = []
e_d_ihx_1 = []
e_d_ihx_2 = []
e_d_va_1 = []
e_d_va_2 = []
e_d_cp_1 = []
e_d_cp_2 = []
e_d_gc = []
e_d_mg = []


p_ttd_u = {
    'p_kond': []
}
description = {
    'p_kond': 'Kondensatordruck in bar',
}

Temperatur = [190.00000000001666, 190.50000000001694, 191.00000000001774, 191.5000000000212, 192.00000000001137, 192.50000000000801, 193.00000000002206, 193.5000000000104, 194.00000000001324, 194.5000000000161, 195.00000000000568, 195.50000000001143, 196.00000000002507, 196.50000000000153, 196.99999999999812, 197.50000000000142, 198.000000000003, 198.50000000000085, 199.00000000000028, 199.49999999999937, 200.00000000000085, 200.4999999999996, 200.99999999999864, 201.499999999998, 202.0000000000009, 202.50000000000153, 202.99999999999983, 203.50000000000102, 204.00000000000148, 204.49999999999915, 204.99999999999966, 205.50000000000028, 206.00000000000085, 206.4999999999991, 206.99999999999807, 207.49999999999994, 208.0000000000016, 208.50000000000125, 209.00000000000307, 209.49999999999727, 210.00000000000034, 210.4999999999987, 210.999999999997, 211.500000000003, 212.000000000005, 212.4999999999983, 212.9999999999996, 213.5000000000045, 213.9999999999934, 214.49999999999488, 215.00000000000455, 215.5, 216.00000000000085, 216.50000000000568, 216.9999999999995, 217.50000000000261, 218.00000000000205, 218.5, 219.00000000000438, 219.49999999999568, 220.00000000000597]
Mitteldruck = [24.47272727272727, 24.47272727272727, 24.47272727272727, 24.47272727272727, 24.47272727272727, 24.47272727272727, 24.47272727272727, 24.47272727272727, 24.47272727272727, 24.47272727272727, 24.47272727272727, 24.47272727272727, 24.47272727272727, 24.47272727272727, 24.473737373737375, 24.473737373737375, 24.42323232323232, 24.322222222222226, 24.24646464646465, 24.120202020202022, 24.019191919191922, 23.943434343434344, 23.86767676767677, 23.79191919191919, 23.71616161616162, 23.640404040404043, 23.585510204081633, 23.515102040816323, 23.454897959183672, 23.39469387755102, 23.34469387755102, 23.28448979591837, 23.23448979591836, 23.184489795918363, 23.135102040816328, 23.085102040816324, 23.04530612244898, 22.99530612244898, 22.955510204081634, 22.91571428571428, 22.875918367346934, 22.836122448979594, 22.796326530612244, 22.766734693877552, 22.726938775510202, 22.687142857142856, 22.657551020408167, 22.627959183673468, 22.58816326530612, 22.558571428571426, 22.528979591836734, 22.489183673469388, 22.467435897435898, 22.4374358974359, 22.4074358974359, 22.3774358974359, 22.3474358974359, 22.316153846153846, 22.286153846153848, 22.266410256410254, 22.236410256410256]
Wirkungsgrad5 = []
Hochdruck5 = []
Wirkungsgrad10 = []
Hochdruck10 = []
Wirkungsgrad15 = []
Hochdruck15 = []
Wirkungsgrad20 = []
Hochdruck20 = []

for i, j in zip(Temperatur, Mitteldruck):
    c14.set_attr(T=i)
    c24.set_attr(p=j)
    gc.set_attr(ttd_u=5)
    nw.solve(mode='design')
    ean.analyse(pamb=pamb, Tamb=Tamb)
    Wirkungsgrad5 += [ean.network_data.loc['epsilon'] * 100]
    Hochdruck5 += [nw.get_conn("22").get_attr("p").val]
    gc.set_attr(ttd_u=10)
    nw.solve(mode='design')
    ean.analyse(pamb=pamb, Tamb=Tamb)
    Wirkungsgrad10 += [ean.network_data.loc['epsilon'] * 100]
    Hochdruck10 += [nw.get_conn("22").get_attr("p").val]
    gc.set_attr(ttd_u=15)
    nw.solve(mode='design')
    ean.analyse(pamb=pamb, Tamb=Tamb)
    Wirkungsgrad15 += [ean.network_data.loc['epsilon'] * 100]
    Hochdruck15 += [nw.get_conn("22").get_attr("p").val]
    gc.set_attr(ttd_u=20)
    nw.solve(mode='design')
    ean.analyse(pamb=pamb, Tamb=Tamb)
    Wirkungsgrad20 += [ean.network_data.loc['epsilon'] * 100]
    Hochdruck20 += [nw.get_conn("22").get_attr("p").val]

print('Fertig')
print(Hochdruck5)
print(Wirkungsgrad5)
print(Hochdruck10)
print(Wirkungsgrad10)
print(Hochdruck15)
print(Wirkungsgrad15)
print(Hochdruck20)
print(Wirkungsgrad20)"""

for p in data['p_kond']:
    c22.set_attr(p=p)
    nw.solve('design')
    ean.analyse(pamb=pamb, Tamb=Tamb)
    COP['p_kond'] += [nw.busses["heat_product_COP"].P.val / nw.busses["power_COP"].P.val]
    eta['p_kond'] += [ean.network_data.loc['epsilon'] * 100]
    p_ttd_u['p_kond'] += [nw.get_conn("22").get_attr("p").val]
    T_Hi = nw.get_conn("13").get_attr("T").val + 273.15
    T_Ho = nw.get_conn("14").get_attr("T").val + 273.15
    T_Ci = nw.get_conn("11").get_attr("T").val + 273.15
    T_Co = nw.get_conn("12").get_attr("T").val + 273.15
    pkond += [nw.get_conn("22").get_attr("p").val]
    e_d_ev += [ean.component_data['epsilon']['Evaporator'] * 100]
    e_d_ihx_1 += [ean.component_data['epsilon']['Internal Heat Exchanger 1'] * 100]
    e_d_ihx_2 += [ean.component_data['epsilon']['Internal Heat Exchanger 2'] * 100]
    e_d_va_1 += [ean.component_data['epsilon']['Valve 1'] * 100]
    e_d_va_2 += [ean.component_data['epsilon']['Valve 2'] * 100]
    e_d_cp_1 += [ean.component_data['epsilon']['Compressor 1'] * 100]
    e_d_cp_2 += [ean.component_data['epsilon']['Compressor 2'] * 100]
    e_d_gc += [ean.component_data['epsilon']['Gas cooler'] * 100]
    diff_T_H = (T_Ho-T_Hi) / math.log(T_Ho / T_Hi)
    diff_T_C = (T_Ci-T_Co) / math.log(T_Ci / T_Co)
    Lorenz_COP['p_kond'] += [diff_T_H / (diff_T_H - diff_T_C)]
    """print('Massenstrom Kreislauf', nw.get_conn("22").get_attr("m").val)
    print('Massenstrom Quelle', nw.get_conn("11").get_attr("m").val)
    print('Massenstrom Senke', nw.get_conn("13").get_attr("m").val)
    print('Kompressorleistung=', (nw.get_comp('Compressor 1').get_attr('P').val + nw.get_comp('Compressor 2').get_attr('P').val) * 1e-3)
    print('Drossel 1 =', ean.component_data['E_D']['Valve 1'] * 1e-3)
    print('Drossel 2 =', ean.component_data['E_D']['Valve 2'] * 1e-3)
    print('Gaskühler =', ean.component_data['E_D']['Gas cooler'] * 1e-3)
    print('Gaskühler Wirkungsgrad =', ean.component_data['epsilon']['Gas cooler'] * 100)
    print('Kompressor 1 =', ean.component_data['E_D']['Compressor 1'] * 1e-3)
    print('Kompressor 1 Wirkungsgrad =', ean.component_data['epsilon']['Compressor 1'] * 100)
    print('Kompressor 2 =', ean.component_data['E_D']['Compressor 2'] * 1e-3)
    print('Kompressor 2 Wirkungsgrad =', ean.component_data['epsilon']['Compressor 2'] * 100)
    print('Verdampfer =', ean.component_data['E_D']['Evaporator'] * 1e-3)
    print('IWÜ 1 =', ean.component_data['E_D']['Internal Heat Exchanger 1'] * 1e-3)
    print('IWÜ 1 Wirkungsgrad =', ean.component_data['epsilon']['Internal Heat Exchanger 1'] * 100)
    print('IWÜ 2 =', ean.component_data['E_D']['Internal Heat Exchanger 2'] * 1e-3)
    print('IWÜ 2 Wirkungsgrad =', ean.component_data['epsilon']['Internal Heat Exchanger 2'] * 100)
    print('epsilon = ', ean.network_data.loc['epsilon'] * 100)
    print('E_D gesamt = ', ean.network_data.loc['E_D'] * 1e-3)
    print('E_F gesamt = ', ean.network_data.loc['E_F'] * 1e-3)
    print('COP = ', heat_product_COP.P.val / power_COP.P.val)
    print('Verdampfer =', ean.component_data['E_F']['Evaporator'] * 1e-3)
    print('Verdampferleistung', nw.get_comp('Evaporator').get_attr('Q').val * 1e-3)"""

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
fig.savefig('Optimierung Parallel eta, COP, Lorenz-COP R1233ZD(E).svg')


plt.rc('font', **{'size': 20})
plt.rcParams["figure.figsize"] = (20, 13)

plt.plot(pkond, e_d_ihx_1, color='black')
plt.plot(pkond, e_d_ihx_2, color='grey')
plt.plot(pkond, e_d_va_1, color='red')
plt.plot(pkond, e_d_va_2, color='orange')
plt.plot(pkond, e_d_ev, color='blue')
plt.plot(pkond, e_d_cp_1, color='green')
plt.plot(pkond, e_d_cp_2, color='lime')
plt.plot(pkond, e_d_gc, color='brown')
plt.show()

import json

data = {
    'p_kond': list(np.linspace(42, 54, iterations))
}

with open('Senkentemperatur.txt', 'a') as convert_file:
    convert_file.write(json.dumps(data)+"\n")

with open('Senkentemperatur.txt', 'a') as convert_file:
    convert_file.write(json.dumps(COP)+"\n")

with open('Senkentemperatur.txt', 'a') as convert_file:
    convert_file.write(json.dumps(eta)+"\n")

#with open('Senkentemperatur.txt', 'a') as convert_file:
    #convert_file.write(json.dumps(p_ttd_u) + "\n")

f = open("Senkentemperatur.txt", "r")
print(f.read())



plt.rc('font', **{'size': 18})

dat = tuple(data['p_kond'])
E_D_Lists = {}
for name in ['Gas cooler', 'Evaporator', 'Valve 1', 'Valve 2', 'Compressor 1', 'Compressor 2',
             'Internal Heat Exchanger 1', 'Internal Heat Exchanger 2', 'Merge']:
    E_D_List = []
    for p in data['p_kond']:
        c22.set_attr(p=p)
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
ax.legend(fontsize="17", loc='lower right')

plt.show()
fig.savefig('Optimierung Parallel Exergievernichtung R1233ZD(E).png')




