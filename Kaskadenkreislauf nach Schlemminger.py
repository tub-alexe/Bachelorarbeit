#Quelle 95, Schlemminger in Wu2021 zu finden

from tespy.networks import Network
from tespy.components import (HeatExchanger, Sink, Source, CycleCloser, Compressor, Valve)
from tespy.connections import Connection

nw = Network(fluids=['R600', 'R290', 'H2O'], T_unit='C', p_unit='bar',
             h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

#Quellen und Senken

k_in = Source('Kondensator rein')
k_aus = Sink('Kondensator raus')
v_in = Source('Verdampfer rein')
v_aus = Sink ('Verdampfer raus')
schluss1 = CycleCloser('Unterer Wärmepumpenkreislauf')
schluss2 = CycleCloser('Oberer Wärmepumpenkreislauf')

#Unterer Wärmepumpenkreislauf

vd = HeatExchanger('Verdampfer')
kp1 = Compressor('Unterer Kompressor')
exp1 = Valve('Unteres Expansionsventil')
iwt = HeatExchanger('Innerer Wärmeübertrager')

#Oberer Wärmepumpenkreislauf

kd = HeatExchanger('Kondensator')
kp2 = Compressor('Unterer Kompressor')
exp2 = Valve('Unteres Expansionsventil')

#Verbindungen unterer Kreislauf

c1 = Connection(schluss1, 'out1', vd, 'in2', label='1')
c2 = Connection(vd, 'out2', kp1, 'in1', label='2')
c3 = Connection(kp1, 'out1', iwt, 'in1', label='3')
c4 = Connection(iwt, 'out1', exp1, 'in1', label='4')
c5 = Connection(exp1, 'out1', schluss1, 'in1', label='5')
nw.add_conns(c1, c2, c3, c4, c5)
#Verbindungen oberer Kreislauf

c6 = Connection(schluss2, 'out1', kd, 'in1', label='6')
c7 = Connection(kd, 'out1', kp2, 'in1', label='7')
c8 = Connection(kp2, 'out1', iwt, 'in2', label='8')
c9 = Connection(iwt, 'out2', exp2, 'in1', label='9')
c10 = Connection(exp2, 'out1', schluss2, 'in1', label='10')
nw.add_conns(c6, c7, c8, c9, c10)
#Verbindungen Quellen und Senken

c11 = Connection(k_in, 'out1', kd, 'in2', label='11')
c12 = Connection(kd, 'out2', k_aus, 'in1', label='12')
c13 = Connection(v_in, 'out1', vd, 'in1', label='13')
c14 = Connection(vd, 'out1', v_aus, 'in1', label='14')
nw.add_conns(c11, c12, c13, c14)
#Parametrisierung

c1.set_attr(T=-1, fluid={'R290': 1})
c6.set_attr(T=113, fluid={'R600': 1})
c11.set_attr(T=85, fluid={'H2O': 1})
c12.set_attr(T=118, fluid={'H2O': 1})
c13.set_attr(T=10, fluid={'H2O': 1})
c14.set_attr(T=4, fluid={'H2O': 1})
vd.set_attr(pr1=1, pr2=2, Q=10)
kd.set_attr(pr1=1, pr2=2, Q=-20)
kp1.set_attr(eta_s=1)
kp2.set_attr(eta_s=1)

#Lösen

nw.solve(mode='design')
nw.print_results()

print(f'COP1 = {abs(iwt.Q.val) / kp1.P.val}')
print(f'COP2 = {abs(kd.Q.val) / kp2.P.val}')
print(f'COP = {abs(kd.Q.val) / (kp1.P.val+kp2.P.val)}')