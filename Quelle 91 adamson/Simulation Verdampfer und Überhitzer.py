from tespy.components import HeatExchanger
from tespy.connections import Connection

nw = Network(fluids=['R1234ZE(Z)', 'H2O'], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

vd_in = Source('Verdampfer rein')
ue_aus = Sink ('Überhitzer raus')
vd = HeatExchanger('Verdampfer')
ue = HeatExchanger('Überhitzer')

#Verbindungen

c1 = Connection(vd_in, 'out1', vd, 'in1')
c2 = Connection(vd, 'out2', ue, 'in2')
c3 = Connection(ue, 'out1', ue_aus, 'in1')

#Parametrisierung

c1.set_attr(T=80, m=0.2, fluid={'H2O': 1})
c2.set_attr(x=1, fluid={'R1234ZE(Z)': 1})
c3.set_attr(T=70, m=0.2, fluid={'H2O': 1})
vd.set_attr(ttd_l=2)
ue.set_attr(ttd_u=5)