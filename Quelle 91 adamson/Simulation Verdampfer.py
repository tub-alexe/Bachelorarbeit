from tespy.networks import Network
from tespy.components import (HeatExchanger, Source, Sink,)
from tespy.connections import Connection

nw = Network(fluids=['R1234ZE(Z)', 'H2O'], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

# Komponenten

vd_in = Source('Verdampfer rein')
vd_aus = Sink ('Verdampfer raus')
vd = HeatExchanger('Verdampfer')
um_ein = Source('Umgebung Eintritt')
um_aus = Sink('Umgebung Austritt')

# Verbindungen heiße Seite

c1 = Connection(vd_in, 'out1', vd, 'in1')
c2 = Connection(vd, 'out1', vd_aus, 'in1')

# Verbindungen kalte Seite

c3 = Connection(um_ein, 'out1', vd, 'in2')
c4 = Connection(vd, 'out2', um_aus, 'in1')
nw.add_conns(c1, c2, c3, c4)

# Parameter

vd.set_attr(pr1=1, pr2=1, ttd_l=2, ttd_u=5)
c1.set_attr(T=80, fluid={'H2O': 1})
c2.set_attr(T=70, fluid={'H2O': 1})
c3.set_attr(fluid={'R1234ZE(Z)': 1})
c4.set_attr(fluid={'R1234ZE(Z)': 1})

# Lösen

nw.solve(mode='design')
nw.print_results()

