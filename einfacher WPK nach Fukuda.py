#Quelle 114 einfacher WPK von Fukuda in apragus

from tespy.networks import Network
from tespy.components import (HeatExchanger, HeatExchangerSimple, Sink, Source, CycleCloser, Compressor,Valve)
from tespy.connections import Connection

nw = Network(fluids=['R1234ZE(Z)', 'H2O'], T_unit='C', p_unit='bar',
             h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

#Quellen und Senken

k_in = Source('Kondensator rein')
k_aus = Sink('Kondensator raus')
v_in = Source('Verdampfer rein')
v_aus = Sink ('Verdampfer raus')
schluss = CycleCloser('Wärmepumpenkreislauf')

#Komponenten

kd = HeatExchanger('Kondensator')
vd = HeatExchanger('Verdampfer')
kp = Compressor('Kompressor')
exp = Valve('Expansionsventil')

#Verbindungen

c1 = Connection(schluss, 'out1', vd, 'in2')
c2 = Connection(vd, 'out2', kp, 'in1')
c3 = Connection(kp, 'out1', kd, 'in1')
c4 = Connection(kd, 'out1', exp, 'in1')
c5 = Connection(exp, 'out1', schluss, 'in1')
c6 = Connection(k_in, 'out1', kd, 'in2')
c7 = Connection(kd, 'out2', k_aus, 'in1')
c8 = Connection(v_in, 'out1', vd, 'in1')
c9 = Connection(vd, 'out1', v_aus, 'in1')
nw.add_conns(c1, c2, c3, c4, c5, c6, c7, c8, c9)

#Parametrisierung

vd.set_attr(pr1=1, pr2=1)
kd.set_attr(pr1=1, pr2=2)
c1.set_attr(T=64, fluid={'R1234ZE(Z)': 1})
c3.set_attr(T=105, fluid={'R1234ZE(Z)': 1})
c6.set_attr(T=50, fluid={'H2O': 1})
c7.set_attr(T=75, fluid={'H2O': 1})
c8.set_attr(T=45, fluid={'H2O': 1})
c9.set_attr(T=39, fluid={'H2O': 1})
kp.set_attr(eta_s=0.74)

#Lösen

nw.solve(mode='design')
nw.print_results()

print(f'COP = {abs(ko.Q.val) / kp.P.val}')