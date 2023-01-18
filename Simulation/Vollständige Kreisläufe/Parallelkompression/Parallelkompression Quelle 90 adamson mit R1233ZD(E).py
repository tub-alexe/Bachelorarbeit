from tespy.networks import Network
from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink, DropletSeparator, Merge)
from tespy.connections import Connection, Bus
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
from fluprodia import FluidPropertyDiagram

wf = 'R1233ZD(E)'
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
src_wf = Source('Source Working Fluid')
src_wf_2 = Source('Source Working Fluid 2')
snk_wf = Sink('Sink Working Fluid')
snk_wf_2 = Sink('Sink Working Fluid 2')
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
h_gc_ihx_2 = CPSI("H", "P", 47.8 * 1e5, "T", 273.15 + 119, wf) * 1e-3
gc_ihx_2.set_attr(h=h_gc_ihx_2, p=47.8)

# h_va_2_fl = CPSI("H", "P", 7.3 * 1e5, "Q", 0.4, wf) * 1e-3
va_2_fl.set_attr(p=8, fluid=fld_wf)

h_ihx_2_cp_2 = CPSI("H", "P", 8 * 1e5, "T", 273.15 + 114, wf) * 1e-3
ihx_2_cp_2.set_attr(h=h_ihx_2_cp_2)

h_ev_sup = CPSI("H", "Q", 1, "T", 273.15 + 70, wf) * 1e-3
ev_sup.set_attr(h=h_ev_sup, p=5.1)

h_sup_ihx_1 = CPSI("H", "P", 5.1 * 1e5, "T", 273.15 + 75, wf) * 1e-3
sup_ihx_1.set_attr(h=h_sup_ihx_1)

h_ihx_1_cp_1 = CPSI("H", "P", 5.1 * 1e5, "T", 273.15 + 82.23, wf) * 1e-3
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

gc_ihx_2.set_attr(h=None, T=119, p=47.8)
va_2_fl.set_attr(p=8)
ihx_2_cp_2.set_attr(h=None)
ihx_2.set_attr(ttd_u=5)
ev_sup.set_attr(h=None, x=1, p=5.1)
sup_ihx_1.set_attr(h=None, Td_bp=5)
ihx_1_cp_1.set_attr(h=None)
ihx_1.set_attr(ttd_u=6)
gc_si_out.set_attr(T=None)
gc.set_attr(ttd_u=5)

nw.solve(mode='design')
nw.print_results()

print(f'COP = {abs(gc.Q.val) / (cp_1.P.val + cp_2.P.val)}')


#log p,h- diagram
result_dict = {}
result_dict.update({gc.label: gc.get_plotting_data()[1]})
result_dict.update({ihx_2.label: ihx_2.get_plotting_data()[1]})
result_dict.update({va_2.label: va_2.get_plotting_data()[1]})
result_dict.update({ihx_2.label: ihx_2.get_plotting_data()[2]})

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


diagram.save('Test.png', dpi=300)
