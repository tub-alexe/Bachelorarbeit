from tespy.networks import Network
from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink)
from tespy.connections import Connection, Bus
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
from fluprodia import FluidPropertyDiagram

wf1 = 'REFPROP::R1233ZD(E)'
wf2 = 'REFPROP::Pentane'
si = 'H2O'

nw = Network(fluids=[wf1, wf2, si], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

# Components
ca = HeatExchanger('Cascade HeatExchanger')
cp1 = Compressor('Compressor1')
gc1 = HeatExchanger('GasCooler1')
gc2 = HeatExchanger('GasCooler2')
cp2 = Compressor('Compressor2')
gc1 = HeatExchanger('GasCooler1')
gc2 = HeatExchanger('GasCooler2')
va1 = Valve('Valve1')
va2 = Valve('Valve2')
ev1 = HeatExchanger('Evaporator1')
sup1 = HeatExchanger('Superheater1')
ev2 = HeatExchanger('Evaporator2')
sup2 = HeatExchanger('Superheater2')

#Sources, Sinks and CycleCloser
si1 = Sink('Sink1')
si2 = Sink('Sink2')
sou1 = Source('Source1')
sou2 = Source('Source2')
si_in = Source('Sink in')
si_out = Sink('Sink out')
sou_in1 = Source('Source in1')
sou_out1 = Sink('Source out1')
sou_in2 = Source('Source in2')
sou_out2 = Sink('Source out2')

cc1 = CycleCloser('CycleCloser1')
cc2 = CycleCloser('CycleCloser2')

# Connections Cycle Top
c1 = Connection(gc2, 'out1', ca, 'in1', label="1")
c2 = Connection(ca, 'out1', va2, 'in1', label="2")
c3 = Connection(va2, 'out1', ev2, 'in2', label="3")
c3_sup = Connection(ev2, 'out2', sup2, 'in2', label="3_sup")
c4 = Connection(sup2, 'out2', cp2, 'in1', label="4")
c4_cc = Connection(cp2, 'out1', cc1, 'in1', label="4_cc")
c5 = Connection(cc1, 'out1', gc2, 'in1', label="5")

# Connections Cycle Bottom
c6 = Connection(cc2, 'out1', ca, 'in2', label="6")
c7 = Connection(ca, 'out2', cp1, 'in1', label="7")
c8 = Connection(cp1, 'out1', gc1, 'in1', label="8")
c9 = Connection(gc1, 'out1', va1, 'in1', label="9")
c10 = Connection(va1, 'out1', ev1, 'in2', label="10")
c10_sup = Connection(ev1, 'out2', sup1, 'in2', label="10_sup")
c11_cc = Connection(sup1, 'out2', cc2, 'in1', label="11_cc")

c11 = Connection(si_in, 'out1', gc1, 'in2', label="11")
c12 = Connection(gc1, 'out2', gc2, 'in2', label="12")
c13 = Connection(gc2, 'out2', si_out, 'in1', label="13")

c14 = Connection(sou_in2, 'out1', sup2, 'in1', label="14")
c15 = Connection(sup2, 'out1', ev2, 'in1', label="15")
c16 = Connection(ev2, 'out1', sou_out2, 'in1', label="16")
c17 = Connection(sou_in1, 'out1', sup1, 'in1', label="17")
c18 = Connection(sup1, 'out1', ev1, 'in1', label="18")
c19 = Connection(ev1, 'out1', sou_out1, 'in1', label="19")

nw.add_conns(c1, c2, c3, c3_sup, c4, c4_cc, c5, c6, c7, c8, c9, c10, c10_sup, c11_cc, c11, c12, c13, c14, c15, c16, c17,
             c18, c19)

# Starting Parameters Components
ca.set_attr(pr1=1, pr2=1)
cp1.set_attr(eta_s=0.7)
cp2.set_attr(eta_s=0.7)
gc1.set_attr(pr1=1, pr2=1)
gc2.set_attr(pr1=1, pr2=1)
ev1.set_attr(pr1=1, pr2=1)
sup1.set_attr(pr1=1, pr2=1)
ev2.set_attr(pr1=1, pr2=1)
sup2.set_attr(pr1=1, pr2=1)

h_c1 = CPSI("H", "P", 57.5 * 1e5, "T", 273.15+140, wf1) * 1e-3
c1.set_attr(h=h_c1, p=57.5, fluid={'R1233ZD(E)': 1, 'Pentane': 0, 'H2O': 0})

#h_c2 = CPSI("H", "P", 36 * 1e5, "T", 273.15+127, wf1) * 1e-3
#c2.set_attr(h=h_c2)

c3.set_attr(p=5.1)

h_c3_sup = CPSI("H", "Q", 1, "T", 273.15+70, wf1) * 1e-3
c3_sup.set_attr(h=h_c3_sup)

h_c4 = CPSI("H", "P", 5.1 * 1e5, "T", 273.15+75, wf1) * 1e-3
c4.set_attr(h=h_c4)

h_c6 = CPSI("H", "P", 2.8 * 1e5, "T", 273.15+75, wf2) * 1e-3
c6.set_attr(p=2.8, fluid={'R1233ZD(E)': 0, 'Pentane': 1, 'H2O': 0})

h_c7 = CPSI("H", "P", 2.8 * 1e5, "T", 273.15+95, wf2) * 1e-3
c7.set_attr(h=h_c7)

c8.set_attr(p=11.652)
h_c9 = CPSI("H", "P", 11.652 * 1e5, "T", 273.15+105, wf2) * 1e-3
c9.set_attr(h=h_c9)

h_c10_sup = CPSI("H", "Q", 1, "T", 273.15+70, wf2) * 1e-3
c10_sup.set_attr(h=h_c10_sup)

h_c11_cc = CPSI("H", "P", 2.8 * 1e5, "T", 273.15+75, wf2) * 1e-3
c11_cc.set_attr(h=h_c11_cc)

c11.set_attr(T=100, p=20, fluid={'R1233ZD(E)': 0, 'Pentane': 0, 'H2O': 1})
c12.set_attr(T=135)
c13.set_attr(T=200)

c14.set_attr(T=80, m=5, p=5, fluid={'R1233ZD(E)': 0, 'Pentane': 0, 'H2O': 1})
c16.set_attr(T=75)
c17.set_attr(T=80, p=5, fluid={'R1233ZD(E)': 0, 'Pentane': 0, 'H2O': 1})
c19.set_attr(T=75)

#Solve Model
nw.solve(mode='design')
nw.print_results()

#New Parameters
c1.set_attr(h=None, T=140, p=56)
c3.set_attr(p=5.1)
c3_sup.set_attr(h=None, x=1)
c4.set_attr(h=None, Td_bp=5)
c6.set_attr(p=2.8)
c7.set_attr(h=None, T=95)
c8.set_attr(p=11.652)
c9.set_attr(h=None, T=105)
c10_sup.set_attr(h=None, x=1)
c11_cc.set_attr(h=None, Td_bp=5)
c12.set_attr(T=None)
gc1.set_attr(ttd_u=10)
c13.set_attr(T=None)
gc2.set_attr(ttd_u=5)

# busses
power = Bus('power input')
power.add_comps(
    {'comp': cp1, 'char': 1, 'base': 'bus'},
    {'comp': cp2, 'char': 1, 'base': 'bus'},
    {'comp': sou_in1, 'base': 'bus'},
    {'comp': sou_in2, 'base': 'bus'},
    {'comp': sou_out1},
    {'comp': sou_out2})


heat_product = Bus('heating')
heat_product.add_comps(
    {'comp': si_in, 'base': 'bus'},
    {'comp': si_out})

power_COP = Bus('power')
power_COP.add_comps(
        {'comp': cp1, 'char': -1, 'base': 'bus'},
        {'comp': cp2, 'char': -1, 'base': 'bus'}
)

heat_product_COP = Bus('heat_product')
heat_product_COP.add_comps(
            {"comp": gc1, "char": 1},
            {"comp": gc2, "char": 1})

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

#Solve Model
nw.solve(mode='design')
nw.print_results()