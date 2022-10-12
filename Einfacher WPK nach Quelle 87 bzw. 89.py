#Quelle 87 aus adamson simuliert, einfache Wärmebereitstellung für einen spray dryer

from tespy.networks import Network
from tespy.components import (HeatExchanger, HeatExchangerSimple, Sink, Source, CycleCloser, Compressor,Valve)
from tespy.connections import Connection

nw = Network(fluids=['R134A', 'N2', 'O2', 'Ar', 'CO2', 'air'], T_unit='C', p_unit='bar',
             h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')
air = {'N2': 0.7551, 'O2': 0.2314, 'Ar': 0.129, 'CO2': 0.0006}
#Quellen und Senken

k_in = Source('Kondensator rein')
k_aus = Sink('Kondensator raus')
schluss = CycleCloser('Wärmepumpenkreislauf')

#Komponenten

kd = HeatExchanger('Kondensator')
vd = HeatExchangerSimple('Verdampfer')
kp = Compressor('Kompressor')
exp = Valve('Expansionsventil')

#Verbindungen

c1 = Connection(schluss, 'out1', vd, 'in1')
c2 = Connection(vd, 'out1', kp, 'in1')
c3 = Connection(kp, 'out1', kd, 'in1')
c4 = Connection(kd, 'out1', exp, 'in1')
c5 = Connection(exp, 'out1', schluss, 'in1')
c6 = Connection(k_in, 'out1', kd, 'in2')
c7 = Connection(kd, 'out2', k_aus, 'in1')
nw.add_conns(c1, c2, c3, c4, c0, c5, c6, c7)

#Parametrisierung

vd.set_attr(pr=1)
kd.set_attr(pr1=1, pr2=2)
c1.set_attr(T=30,fluid={'R134A': 1})
c4.set_attr(T=125,p=4,47, fluid={'R134A': 1})
c7.set_attr(T=113, fluid={'air': 1})
kp.set_attr(eta_s=1)

nw.solve(mode='design')
nw.print_results()

print(f'COP = {abs(co.Q.val) / cp.P.val}')