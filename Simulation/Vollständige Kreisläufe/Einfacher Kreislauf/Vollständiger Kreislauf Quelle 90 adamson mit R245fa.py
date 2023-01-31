from tespy.networks import Network
from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink)
from tespy.connections import Connection, Bus
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
from fluprodia import FluidPropertyDiagram

wf = 'REFPROP::R245fa'
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
c4 = Connection(ev, 'out2', sup, 'in2', label="4")
c5 = Connection(sup, 'out2', cp, 'in1', label="5")
c6 = Connection(cp, 'out1', cc, 'in1', label="6")

# Connections Sink

c7 = Connection(si_in, 'out1', gc, 'in2', label="7")
c8 = Connection(gc, 'out2', si_out, 'in1', label="8")

# Connections Source

c9 = Connection(sou_in, 'out1', sup, 'in1', label="9")
c10 = Connection(sup, 'out1', ev, 'in1', label="10")
c11 = Connection(ev, 'out1', sou_out, 'in1', label="11")
nw.add_conns(c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11)

# Starting Parameters Components

gc.set_attr(pr1=1, pr2=1)
ev.set_attr(pr1=1, pr2=1)
sup.set_attr(pr1=1, pr2=1)
cp.set_attr(eta_s=0.7)

# Starting Parameters Connections Cycle

#h_gk_vor = CPSI("H", "P", 36 * 1e5, "T", 273.15+200.734, km) * 1e-3
#c1.set_attr(h=h_gk_vor)

h_gk_nach = CPSI("H", "P", 89 * 1e5, "T", 273.15+105, wf) * 1e-3
c2.set_attr(h=h_gk_nach, p=89)

#h_verd = CPSI("H", "Q", 0, "T", 273.15+70, km) * 1e-3
c3.set_attr(p=6.1)

h_zw = CPSI("H", "P", 6.1 * 1e5, "T", 273.15+70, wf) * 1e-3
c4.set_attr(h=h_zw)

h_uebe = CPSI("H", "P", 6.1 * 1e5, "T", 273.15+75, wf) * 1e-3
c5.set_attr(h=h_uebe, fluid={'R245fa': 1, 'H2O': 0})

# Starting Parameters Connection Sink
c7.set_attr(T=100, p=20, fluid={'R245fa': 0, 'H2O': 1})
c8.set_attr(T=200)

# Starting Parameters Connection Source
c9.set_attr(T=80, m=5, p=5, fluid={'R245fa': 0, 'H2O': 1})
c11.set_attr(T=75)

#Solve Model

nw.solve(mode='design')
nw.print_results()