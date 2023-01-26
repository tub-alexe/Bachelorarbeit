from tespy.networks import Network
from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink)
from tespy.connections import Connection, Bus
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
from fluprodia import FluidPropertyDiagram

wf = 'R1233ZD(E)'
si = 'H2O'
fld_wf = {wf: 1, si: 0}
fld_si = {wf: 0, si: 1}

nw = Network(fluids=[wf, si], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s')

# Components

gc = HeatExchanger('Gas cooler')
ev = HeatExchanger('Evaporator')
sup = HeatExchanger('Superheater')
cool = HeatExchanger('Cooling')
va = Valve('Valve')
cp1 = Compressor('Compressor1')
cp2 = Compressor('Compressor2')
ihx = HeatExchanger("Internal Heat Exchanger")

#Sources, Sinks and CycleCloser

si_in = Source('Sink in')
si_out = Sink('Sink out')

sou_in = Source('Source in')
sou_out = Sink('Source out')
sou_cool = Source('Source Cooling')
si_cool = Sink('Sink Cooling')

cc = CycleCloser('CycleCloser')


# Connections Cycle
c1 = Connection(ihx, 'out2', cp1, 'in1')
c1_co = Connection(cp1, 'out1', cool, 'in1')
c2 = Connection(cool, 'out1', cp2, 'in1')
c2cc = Connection(cp2, 'out1', cc, 'in1')
c3 = Connection(cc, 'out1', gc, 'in1')
c4 = Connection(gc, 'out1', ihx, 'in1')
c5 = Connection(ihx, 'out1', va, 'in1')
c6 = Connection(va, 'out1', ev, 'in2')
c6_ue = Connection(ev, 'out2', sup, 'in2')
c7 = Connection(sup, 'out2', ihx, 'in2')

# Connections Source
c8 = Connection(si_in, 'out1', gc, 'in2')
c9 = Connection(gc, 'out2', si_out, 'in1')
c10 = Connection(sou_in, 'out1', sup, 'in1')
c11 = Connection(sup, 'out1', ev, 'in1')
c12 = Connection(ev, 'out1', sou_out, 'in1')
c13 = Connection(sou_cool, 'out1', cool, 'in2')
c14 = Connection(cool, 'out2', si_cool, 'in1')
nw.add_conns(c1, c1_co, c2, c2cc, c3, c4, c5, c6_ue, c6, c7, c8, c9, c10, c11, c12, c13, c14)

# Starting Parameters Components
gc.set_attr(pr1=1, pr2=1)
ihx.set_attr(pr1=1, pr2=1)
ev.set_attr(pr1=1, pr2=1)
sup.set_attr(pr1=1, pr2=1)
cp1.set_attr(eta_s=0.7)
cp2.set_attr(eta_s=0.7)
cool.set_attr(pr1=1, pr2=1)

# Starting Parameters Connections Cycle
h_ihx_h_nach = CPSI("H", "P", 5.1 * 1e5, "T", 273.15+101, wf) * 1e-3
c1.set_attr(h=h_ihx_h_nach, p=5.1, fluid={'R1233ZD(E)': 1, 'H2O': 0})


c1_co.set_attr(p=25)
h_c2 = CPSI("H", "P", 25 * 1e5, "T", 273.15+166, wf) * 1e-3
c2.set_attr(h=h_c2)


h_ihx_k_vor = CPSI("H", "P", 44 * 1e5, "T", 273.15+106, wf) * 1e-3
c4.set_attr(h=h_ihx_k_vor, p=44)

h_zw = CPSI("H", "P", 5.1 *1e5, "Q", 1, wf) * 1e-3
c6_ue.set_attr(h=h_zw)

h_ihx_k_nach = CPSI("H", "P", 5.1 * 1e5, "T", 273.15+75, wf) * 1e-3
c7.set_attr(h=h_ihx_k_nach)

c8.set_attr(T=100, p=20, fluid={'R1233ZD(E)': 0, 'H2O': 1})
c9.set_attr(T=200)

# Starting Parameters Connection Source
c10.set_attr(T=80, m=5, p=5, fluid={'R1233ZD(E)': 0, 'H2O': 1})
c12.set_attr(T=75)
c13.set_attr(T=100, m=10, p=10, fluid={'R1233ZD(E)': 0, 'H2O': 1})

#Solve Model
nw.solve(mode='design')
nw.print_results()

c1.set_attr(p=5.1, h=None)
c1_co.set_attr(p=25)
ihx.set_attr(ttd_u=5)
c4.set_attr(h=None, p=44, T=106)
c6_ue.set_attr(h=None, x=1)
c7.set_attr(h=None, Td_bp=5)
c9.set_attr(T=None)
gc.set_attr(ttd_u=7)
c13.set_attr(T=None)
cool.set_attr(ttd_l=5)

# busses
power = Bus('power input')
power.add_comps(
    {'comp': cp1, 'char': 1, 'base': 'bus'},
    {'comp': cp2, 'char': 1, 'base': 'bus'},
    {'comp': sou_in, 'base': 'bus'},
    {'comp': sou_out})


heat_product = Bus('heating')
heat_product.add_comps(
    {'comp': si_in, 'base': 'bus'},
    {'comp': si_out})

power_COP = Bus('power')
power_COP.add_comps(
        {'comp': cp1, 'char': 1, 'base': 'bus'},
        {'comp': cp2, 'char': 1, 'base': 'bus'}
)

cooling = Bus('cooling')
cooling.add_comps(
    {'comp': sou_cool, 'base': 'bus'},
    {'comp': si_cool})


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

ean = ExergyAnalysis(nw, E_P=[heat_product], E_F=[power], E_L=[cooling])
ean.analyse(pamb=pamb, Tamb=Tamb)
ean.print_results()
print(ean.network_data.loc['epsilon'])

#log p,h- diagram

result_dict = {}
result_dict.update({ev.label: ev.get_plotting_data()[2]})
result_dict.update({sup.label: sup.get_plotting_data()[2]})
result_dict.update({ihx.label: ihx.get_plotting_data()[2]})
result_dict.update({cp1.label: cp1.get_plotting_data()[1]})
result_dict.update({cool.label: cool.get_plotting_data()[1]})
result_dict.update({cp2.label: cp2.get_plotting_data()[1]})
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

diagram.save('Test.png', dpi=300)