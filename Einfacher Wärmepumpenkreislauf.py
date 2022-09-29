#Import

from tespy.components import (Condenser, HeatExchanger, Sink, Source, CycleCloser, Compressor,Valve)
from tespy.connections import Connection
from tespy.networks import network

#Network

nw = Network(fluids=[], T_unit='C', p_unit='bar',
             h_unit='kJ / kg', m_unit='kg / s')

# Sink and Source
k_in = Source('Kondensator rein')
k_aus = Sink('Kondensator raus')
v_in = Source('Verdampfer rein')
v-aus = Sink ('Verdampfer raus')
closer = CycleCloser('Wärmepumpenkreislauf')

#Wärmepumpenkreislauf

kd = Condenser('Kondensator')
vd = HeatExchanger('Verdampfer')
kp = Compressor('Kompressor')
va = valve('Expansionsventil')

#Connections
vd_kp = Connection(vd, 'out2', kp, 'in1')
k_in_vd = Connection(k_in, 'out1', vd, 'in1')
vd_k_aus = Connection(vd, 'out1', k_aus, 'in1')
kp_kd = Connection(kp, 'out1', kd, 'in2')
v_in_kd = Connection(v_in, 'out1', kd, 'in1')
kd_v_aus = Connection(kd, 'out1', v_in, 'in1')
kd_closer = Connection(kd, 'out2', closer, 'in1')
closer_va = Connection(closer, 'out1', va, 'in1')
va_vd = Connection(va, 'out1', vd 'in1')
