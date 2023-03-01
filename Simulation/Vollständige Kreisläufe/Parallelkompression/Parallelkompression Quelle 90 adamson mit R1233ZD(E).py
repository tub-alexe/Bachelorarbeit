from tespy.networks import Network
from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink, DropletSeparator, Merge)
from tespy.connections import Connection, Bus
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
from fluprodia import FluidPropertyDiagram
import math

wf = 'REFPROP::R1233ZD(E)'
si = 'H2O'
fld_wf = {wf: 1, si: 0}
fld_si = {wf: 0, si: 1}

nw = Network(fluids=[wf, si], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

#Components
fl = DropletSeparator('Flash Tank')
cp_1 = Compressor('Compressor 1')
cp_2 = Compressor('Compressor 2')
va_1 = Valve('Valve 1')
va_2 = Valve('Valve 2')
ev = HeatExchanger('Evaporator')
sup = HeatExchanger('Superheater')
gc = HeatExchanger('Gas cooler')
ihx_1 = HeatExchanger('Internal Heat Exchanger 1')
ihx_2 = HeatExchanger('Internal Heat Exchanger 2')
src_wf = Source('Source Working Fluid')
src_wf_2 = Source('Source Working Fluid 2')
snk_wf = Sink('Sink Working Fluid')
snk_wf_2 = Sink('Sink Working Fluid 2')
sou_in = Source('Source in')
sou_out = Sink('Source out')
si_in = Source('Sink in')
si_out = Sink('Sink out')
mg = Merge('Merge', num_in=2)
cc = CycleCloser('CycleCloser')

#Connections
#Main Cycle
c1 = Connection(gc, 'out1', ihx_2, 'in1', label="1")
c2 = Connection(ihx_2, 'out1', va_2, 'in1', label="2")
c3 = Connection(va_2, 'out1', fl, 'in1', label="3")
c4 = Connection(fl, 'out1', ihx_1, 'in1', label="4")
c5 = Connection(ihx_1, 'out1', va_1, 'in1', label="5")
c6 = Connection(va_1, 'out1', ev, 'in2', label="6")
c7 = Connection(ev, 'out2', ihx_1, 'in2', label="7")
c8 = Connection(ihx_1, 'out2', cp_1, 'in1', label="8")
c9 = Connection(cp_1, 'out1', mg, 'in1', label="9")
c10 = Connection(fl, 'out2', ihx_2, 'in2', label="10")
c11 = Connection(ihx_2, 'out2', cp_2, 'in1', label="11")
c12 = Connection(cp_2, 'out1', mg, 'in2', label="12")
c13 = Connection(mg, 'out1', cc, 'in1', label="13")
c14 = Connection(cc, 'out1', gc, 'in1', label="14")


#Source
c15 = Connection(sou_in, 'out1', ev, 'in1', label="15")
c16 = Connection(ev, 'out1', sou_out, 'in1', label="16")

#Sink
c17 = Connection(si_in, 'out1', gc, 'in2', label="17")
c18 = Connection(gc, 'out2', si_out, 'in1', label="18")

nw.add_conns(c1, c2, c3, c4, c5, c6, c7, c8, c9,
             c10, c11, c12, c13, c14, c15, c16, c17, c18)

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
h_c1 = CPSI("H", "P", 41 * 1e5, "T", 273.15 + 165, wf) * 1e-3
c1.set_attr(h=h_c1, p=41)

c3.set_attr(p=29, fluid={'R1233ZD(E)': 1, 'H2O': 0})

c6.set_attr(p=8.33)

h_c7 = CPSI("H", "P", 8.33 * 1e5, "T", 273.15 + 90.1, wf) * 1e-3
c7.set_attr(h=h_c7)

h_c8 = CPSI("H", "P", 8.33 * 1e5, "T", 273.15 + 150, wf) * 1e-3
c8.set_attr(h=h_c8)

h_c11 = CPSI("H", "P", 29 * 1e5, "T", 273.15 + 155, wf) * 1e-3
c11.set_attr(h=h_c11)


# Source
c15.set_attr(T=95, p=5, fluid={'R1233ZD(E)': 0, 'H2O': 1})
c16.set_attr(T=94)

# Sink
c17.set_attr(T=160, p=20, fluid={'R1233ZD(E)': 0, 'H2O': 1})
c18.set_attr(T=200)

#Solve Model
nw.solve(mode='design')
nw.print_results()

c1.set_attr(h=None, T=165, p=41)
c3.set_attr(p=29)
c6.set_attr(p=8.33)
c7.set_attr(h=None, Td_bp=0.1)
c8.set_attr(h=None)
ihx_1.set_attr(ttd_u=10)
c11.set_attr(h=None)
ihx_2.set_attr(ttd_u=10)
c18.set_attr(T=None)
gc.set_attr(ttd_u=30)

nw.solve(mode='design')
nw.print_results()

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

nw.solve(mode='design')
nw.print_results()
print('COP', heat_product_COP.P.val / power_COP.P.val)
print('COP', nw.busses["heat_product"].P.val / nw.busses["power"].P.val)
print(f'COP = {abs(gc.Q.val) / (cp_1.P.val + cp_2.P.val)}')

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

#Parameter optmization

import matplotlib.pyplot as plt
import numpy as np

# make text reasonably sized
plt.rc('font', **{'size': 18})
iterations = 20

data = {
    'p_kond': np.linspace(36, 50, iterations)
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
    c1.set_attr(p=p)
    nw.solve('design')
    ean.analyse(pamb=pamb, Tamb=Tamb)
    COP['p_kond'] += [nw.busses["heat_product_COP"].P.val / nw.busses["power_COP"].P.val]
    eta['p_kond'] += [ean.network_data.loc['epsilon'] * 100]
    T_Hi = nw.get_conn("17").get_attr("T").val + 273.15
    T_Ho = nw.get_conn("18").get_attr("T").val + 273.15
    T_Ci = nw.get_conn("15").get_attr("T").val + 273.15
    T_Co = nw.get_conn("16").get_attr("T").val + 273.15
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
fig.savefig('Optimierung Parallel eta, COP, Lorenz-COP R1233ZD(E).svg')

c1.set_attr(p=41)

dat = tuple(data['p_kond'])
E_D_Lists = {}
for name in ['Gas cooler', 'Evaporator', 'Valve 1', 'Valve 2', 'Compressor 1', 'Compressor 2',
             'Internal Heat Exchanger 1', 'Internal Heat Exchanger 2', 'Merge']:
    E_D_List = []
    for p in data['p_kond']:
        c1.set_attr(p=p)
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
fig.savefig('Optimierung Parallel Exergievernichtung R1233ZD(E).svg')


