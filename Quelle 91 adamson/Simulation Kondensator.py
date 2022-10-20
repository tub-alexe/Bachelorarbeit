from tespy.networks import Network
from tespy.components import (HeatExchanger, Source, Sink)
from tespy.connections import Connection

nw = Network(fluids=['R1234ZE(Z)', 'H2O'], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

# Komponenten

ko_ein = Source('Kondensator rein')
ko_aus = Sink('Kondensator raus')
ko = HeatExchanger('Kondensator')
k_ein = Source('Kreislauf rein')
k_aus = Sink('Kreislauf raus')

#Verbindungen heiße Seite

c1 = Connection(k_ein, 'out1', ko, 'in1')
c2 = Connection(ko, 'out1', k_aus, 'in1')

#Verbindungen kalte Seite

c3 = Connection(ko_ein, 'out1', ko, 'in2')
c4 = Connection(ko, 'out2', ko_aus, 'in1')
nw.add_conns(c1, c2, c3, c4)

# Parametrisierung

ko.set_attr(pr1=1, pr2=1, ttd_l=5)
c1.set_attr(fluid={'R1234ZE(Z)': 1})
c3.set_attr(T=70, m=0.2, fluid={'H2O': 1})
c4.set_attr(T=160)

#Lösen

nw.solve(mode='design')
nw.print_results()

# ebenfalls wieder zu wenig Parameter