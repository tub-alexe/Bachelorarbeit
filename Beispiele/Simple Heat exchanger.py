from tespy.networks import Network
from tespy.components import (HeatExchangerSimple, Source, Sink,)
from tespy.connections import Connection

nw = Network(fluids=['H2O'], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

# Komponenten

vd_in = Source('Verdampfer rein')
vd_aus = Sink ('Verdampfer raus')
vd = HeatExchangerSimple('Verdampfer')


# Verbindungen heiße Seite

c1 = Connection(vd_in, 'out1', vd, 'in1')
c2 = Connection(vd, 'out1', vd_aus, 'in1')
nw.add_conns(c1, c2)

# Parameter

vd.set_attr(pr=1, Q=2)
c1.set_attr(T=70, p=4, fluid={'H2O': 1})
c2.set_attr(T=80)

# Lösen

nw.solve(mode='design')
nw.print_results()