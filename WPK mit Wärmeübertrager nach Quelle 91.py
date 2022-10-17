#Wärmepumpenkreislauf mit innerem Wärmeübertrager nach Quelle 91 von Fukuda in adamson

from tespy.networks import Network
from tespy.components import (HeatExchanger, HeatExchangerSimple, Sink, Source, CycleCloser, Compressor,Valve)
from tespy.connections import Connection

nw = Network(fluids=['R1234ZE', 'N2', 'O2', 'Ar', 'CO2', 'air', 'H2O'], T_unit='C', p_unit='bar',
             h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW', )
air = {'N2': 0.7551, 'O2': 0.2314, 'Ar': 0.129, 'CO2': 0.0006}

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
iwt = HeatExchanger('Innerer Wärmeübertrager')

#Verbindungen

c1 = Connection(schluss, 'out1', vd, 'in2')
c2 = Connection(vd, 'out2', iwt, 'in2')
c3 = Connection(iwt, 'out2', kp, 'in1')
c4 = Connection(kp, 'out1', kd, 'in1')
c5 = Connection(kd, 'out1', iwt, 'in1')
c6 = Connection(iwt, 'out1', exp, 'in1')
c7 = Connection(exp, 'out1', schluss, 'in1')
c8 = Connection(k_in, 'out1', kd, 'in2')
c9 = Connection(kd, 'out2', k_aus, 'in1')
c10 = Connection(v_in, 'out1', vd, 'in1')
c11 = Connection(vd, 'out1', v_aus, 'in1')
nw.add_conns(c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11)

#Parametrisierung

vd.set_attr(pr1=1, pr2=2)
kd.set_attr(pr1=1, pr2=2)
kp.set_attr(eta_s=0.85)
c8.set_attr(T=70, m=0.2, fluid={'H2O': 1})
c9.set_attr(T=180, m=0.2, fluid={'H2O': 1})
c10.set_attr(T=80, fluid={'air': 1})
c11.set_attr(T=70, fluid={'air': 1})

#Lösen

nw.solve(mode='design')
nw.print_results()

print(f'COP = {abs(kd.Q.val) / kp.P.val}')