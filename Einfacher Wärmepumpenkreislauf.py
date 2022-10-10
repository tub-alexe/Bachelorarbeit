#Import
from tespy.networks import Network
from tespy.components import (HeatExchanger, Sink, Source, CycleCloser, Compressor,Valve)
from tespy.connections import Connection


#Network

nw = Network(fluids=['R245FA', 'N2', 'O2', 'Ar', 'CO2', 'air'], T_unit='C', p_unit='bar',
             h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')
air = {'N2': 0.7551, 'O2': 0.2314, 'Ar': 0.129, 'CO2': 0.0006}
# Sink and Source
k_in = Source('Kondensator rein')
k_aus = Sink('Kondensator raus')
v_in = Source('Verdampfer rein')
v_aus = Sink ('Verdampfer raus')
closer = CycleCloser('Wärmepumpenkreislauf')

#Wärmepumpenkreislauf

kd = HeatExchanger('Kondensator')
vd = HeatExchanger('Verdampfer')
kp = Compressor('Kompressor')
va = Valve('Expansionsventil')

#Connections
c1 = Connection(closer, 'out1', vd, 'in2', label='1')
c2 = Connection(vd, 'out2', kp, 'in1', label='2')
c3 = Connection(kp, 'out1', kd, 'in1', label='3')
c4 = Connection(kd, 'out1', va, 'in1', label='4')
c0 = Connection(va, 'out1', closer, 'in1', label='0')
c5 = Connection(k_in, 'out1', vd, 'in1', label='5')
c6 = Connection(vd, 'out1', k_aus, 'in1', label='6')
c7 = Connection(v_in, 'out1', kd, 'in2', label='7')
c8 = Connection(kd, 'out2', v_aus, 'in1', label='8')
nw.add_conns(c1, c2, c3, c4, c0, c5, c6, c7, c8)

kd.set_attr(pr1=1, pr2=2, Q=750)
c2.set_attr(fluid={'R245FA': 1})
vd.set_attr(pr1=1, pr2=1)
kp.set_attr(eta_s=1)
c5.set_attr(T=65, fluid={'air': 1})
c8.set_attr(T=90, fluid={'air': 1})

nw.solve(mode='design')
nw.print_results()

print(f'COP = {abs(co.Q.val) / cp.P.val}')