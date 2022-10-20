from tespy.networks import Network
from tespy.components import (HeatExchanger, Source, Sink)
from tespy.connections import Connection

nw = Network(fluids=['R1234ZE(Z)', 'H2O'], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

# Komponenten

ent_ein = Source('Enthitzer rein')
unt_aus = Sink('Unterkühler raus')
ent = HeatExchanger('Enthitzer')
ko = HeatExchanger('Kondensator')
unt = HeatExchanger('Unterkühler')
k_ein = Source('Kreislauf rein')
k_aus = Sink('Kreislauf raus')

#Verbindungen heiße Seite

c1 = Connection(k_ein, 'out1', ent, 'in1')
c2 = Connection(ent, 'out1', ko, 'in1')
c3 = Connection(ko, 'out1', unt, 'in1')
c4 = Connection(unt, 'out1', k_aus, 'in1')

#Verbindungen kalte Seite

c5 = Connection(ent_ein, 'out1', ent, 'in2')
c6 = Connection(ent, 'out2', ko, 'in2')
c7 = Connection(ko, 'out2', unt, 'in2')
c8 = Connection(unt, 'out2', unt_aus, 'in1')
nw.add_conns(c1, c2, c3, c4, c5, c6, c7, c8)

# Parametrisierung

ent.set_attr(pr1=1, pr2=1, ttd_l=2)
ko.set_attr(pr1=1, pr2=1, ttd_u=2)
unt.set_attr(pr1=1, pr2=1, ttd_l=5)
c1.set_attr(fluid={'R1234ZE(Z)': 1})
c2.set_attr(x=1)
c3.set_attr(x=0)
c5.set_attr(T=70, m=0.2, fluid={'H2O': 1})
c8.set_attr(T=160)

#Lösen

nw.solve(mode='design')
nw.print_results()

# ebenfalls wieder zu wenig Parameter