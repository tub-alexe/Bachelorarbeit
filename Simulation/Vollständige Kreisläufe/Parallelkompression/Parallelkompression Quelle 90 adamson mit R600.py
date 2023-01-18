from tespy.networks import Network
from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink, DropletSeparator, Merge)
from tespy.connections import Connection, Bus
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
from fluprodia import FluidPropertyDiagram

wf = 'R600'
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
gc = HeatExchanger('Gas Cooler')
ihx_1 = HeatExchanger('Internal Heat Exchanger 1')
ihx_2 = HeatExchanger('Internal Heat Exchanger 2')

sou_in = Source('Source in')
sou_out = Sink('Source out')
si_in = Source('Sink in')
si_out = Sink('Sink out')
mg = Merge('merge', num_in=2)
cc = CycleCloser('CycleCloser')

#Connections
#Main Cycle
gc_ihx_2 = Connection(gc, 'out1', ihx_2, 'in1')
ihx_2_va_2 = Connection(ihx_2, 'out1', va_2, 'in1')
va_2_fl = Connection(va_2, 'out1', fl, 'in1')
fl_ihx_1 = Connection(fl, 'out1', ihx_1, 'in1')
ihx_1_va_1 = Connection(ihx_1, 'out1', va_1, 'in1')
va_1_ev = Connection(va_1, 'out1', ev, 'in2')
ev_sup = Connection(ev, 'out2', sup, 'in2')
sup_ihx_1 = Connection(sup, 'out2', ihx_1, 'in2')
ihx_1_cp_1 = Connection(ihx_1, 'out2', cp_1, 'in1')
cp_1_mg = Connection(cp_1, 'out1', mg, 'in1')
fl_ihx_2 = Connection(fl, 'out2', ihx_2, 'in2')
ihx_2_cp_2 = Connection(ihx_2, 'out2', cp_2, 'in1')
cp_2_mg = Connection(cp_2, 'out1', mg, 'in2')
mg_cc = Connection(mg, 'out1', cc, 'in1')
cc_gc = Connection(cc, 'out1', gc, 'in1')


#Source
sou_in_sup = Connection(sou_in, 'out1', sup, 'in1')
ev_sup_sou = Connection(sup, 'out1', ev, 'in1')
ev_sou_out = Connection(ev, 'out1', sou_out, 'in1')

#Sink
si_in_gc = Connection(si_in, 'out1', gc, 'in2')
gc_si_out = Connection(gc, 'out2', si_out, 'in1')

nw.add_conns(gc_ihx_2, ihx_2_va_2, va_2_fl, fl_ihx_1, ihx_1_va_1, va_1_ev, ev_sup, sup_ihx_1, ihx_1_cp_1, cp_1_mg,
             fl_ihx_2, ihx_2_cp_2, cp_2_mg, mg_cc, cc_gc, sou_in_sup, ev_sup_sou, ev_sou_out, si_in_gc, gc_si_out)

#Parameters Components
ev.set_attr(pr1=1, pr2=1)
sup.set_attr(pr1=1, pr2=1)
gc.set_attr(pr1=1, pr2=1)
ihx_1.set_attr(pr1=1, pr2=1)
ihx_2.set_attr(pr1=1, pr2=1)
cp_1.set_attr(eta_s=0.7)
cp_2.set_attr(eta_s=0.7)


#Paramters Connections
#Main Cycle
h_gc_ihx_2 = CPSI("H", "P", 68 * 1e5, "T", 273.15 + 105, wf) * 1e-3
gc_ihx_2.set_attr(h=h_gc_ihx_2, p=68)

# h_va_2_fl = CPSI("H", "P", 7.3 * 1e5, "Q", 0.4, wf) * 1e-3
va_2_fl.set_attr(p=15.2, fluid=fld_wf)

h_ihx_2_cp_2 = CPSI("H", "P", 15.2 * 1e5, "T", 273.15 + 100, wf) * 1e-3
ihx_2_cp_2.set_attr(h=h_ihx_2_cp_2)

h_ev_sup = CPSI("H", "Q", 1, "T", 273.15 + 70, wf) * 1e-3
ev_sup.set_attr(h=h_ev_sup, p=8.1)

h_sup_ihx_1 = CPSI("H", "P", 8.1 * 1e5, "T", 273.15 + 75, wf) * 1e-3
sup_ihx_1.set_attr(h=h_sup_ihx_1)

h_ihx_1_cp_1 = CPSI("H", "P", 8.1 * 1e5, "T", 273.15 + 94.8, wf) * 1e-3
ihx_1_cp_1.set_attr(h=h_ihx_1_cp_1)

# Source
sou_in_sup.set_attr(T=80, m=5, p=5, fluid=fld_si)
ev_sou_out.set_attr(T=75)

# Sink
si_in_gc.set_attr(T=100, p=20, fluid=fld_si)
gc_si_out.set_attr(T=200)

#Solve Model
nw.solve(mode='design')
nw.print_results()
print(f'COP = {abs(gc.Q.val) / (cp_1.P.val + cp_2.P.val)}')

# New Parameters
gc_ihx_2.set_attr(h=None, T=105, p=68)
va_2_fl.set_attr(p=15.2)
ihx_2_cp_2.set_attr(h=None)
ihx_2.set_attr(ttd_u=5)
ev_sup.set_attr(h=None, x=1, p=8.1)
sup_ihx_1.set_attr(h=None, Td_bp=5)
ihx_1_cp_1.set_attr(h=None)
ihx_1.set_attr(ttd_u=5)
gc_si_out.set_attr(T=None)
gc.set_attr(ttd_u=10)


# busses
power = Bus('power input')
power.add_comps(
    {'comp': cp_1, 'char': 1, 'base': 'bus'},
    {'comp': cp_2, 'char': 1, 'base': 'bus'},
    {'comp': sou_in, 'base': 'bus'},
    {'comp': sou_out})


heat_product = Bus('heating')
heat_product.add_comps(
    {'comp': si_in, 'base': 'bus'},
    {'comp': si_out})

power_COP = Bus('power')
power_COP.add_comps(
        {'comp': cp_1, 'char': -1, 'base': 'bus'},
        {'comp': cp_2, 'char': -1, 'base': 'bus'}
)

heat_product_COP = Bus('heat_product')
heat_product_COP.add_comps(
            {"comp": gc, "char": 1})

nw.add_busses(power, heat_product, power_COP, heat_product_COP)

nw.solve(mode='design')
nw.print_results()
print('COP', heat_product_COP.P.val / power_COP.P.val)
print('COP', nw.busses["heat_product"].P.val / nw.busses["power"].P.val)

# Exergy Analysis

pamb = 1
Tamb = 25

ean = ExergyAnalysis(nw, E_P=[heat_product], E_F=[power])
ean.analyse(pamb=pamb, Tamb=Tamb)
ean.print_results()
print(ean.network_data.loc['epsilon'])

#log p,h- diagram
result_dict = {}
result_dict.update({ev.label: ev.get_plotting_data()[2]})
result_dict.update({sup.label: sup.get_plotting_data()[2]})
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



diagram = FluidPropertyDiagram(wf)
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


diagram.save('logph_Parallel_R600.png', dpi=300)

#parameter optimization
import matplotlib.pyplot as plt
import numpy as np

# make text reasonably sized
plt.rc('font', **{'size': 18})


data = {
    'p_verd': np.linspace(7, 8.2, 10),
    'p_kond': np.linspace(68, 78, 10),
    'T_kond': np.linspace(105, 115, 10)
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
    ev_sup.set_attr(p=p)
    nw.solve('design')
    ean.analyse(pamb=pamb, Tamb=Tamb)
    print(ean.network_data.loc['epsilon'])
    eta['p_verd'] += [ean.network_data.loc['epsilon']]

    ev_sup.set_attr(p=8.1)

    nw.solve(mode='design')

for p in data['p_kond']:
    gc_ihx_2.set_attr(p=p)
    nw.solve('design')
    ean.analyse(pamb=pamb, Tamb=Tamb)
    print(ean.network_data.loc['epsilon'])
    eta['p_kond'] += [ean.network_data.loc['epsilon']]

    # reset to base pressure
    gc_ihx_2.set_attr(p=41)

for T in data['T_kond']:
    gc_ihx_2.set_attr(T=T)
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

ax[0].set_ylabel('eta of the Heat Pump')

plt.tight_layout()
plt.show()
fig.savefig('Optimierung_Parallel_R600.svg')