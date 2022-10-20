from tespy.networks import Network
from tespy.components import (HeatExchanger, Source, Sink)
from tespy.connections import Connection

nw = Network(fluids=['R1234ZE(Z)', 'H2O'], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

vd_in = Source('Verdampfer rein')
ue_aus = Sink ('Überhitzer raus')
vd = HeatExchanger('Verdampfer')
ue = HeatExchanger('Überhitzer')
anfang = Source('Umgebung Eintritt')
ende = Sink('Umgebung Austritt')

#Verbindungen heiße Seite

c1 = Connection(vd_in, 'out1', vd, 'in1')
c2 = Connection(vd, 'out1', ue, 'in1')
c3 = Connection(ue, 'out1', ue_aus, 'in1')

#Verbindungen kalte Seite

c4 = Connection(anfang, 'out1', vd, 'in2')
c5 = Connection(vd, 'out2', ue, 'in2')
c6 = Connection(ue, 'out2', ende, 'in1')
nw.add_conns(c1, c2, c3, c4, c5, c6)

#Parametrisierung

vd.set_attr(pr1=1, pr2=1, ttd_l=2)
ue.set_attr(pr1=1, pr2=1, ttd_u=5)
c1.set_attr(T=80, fluid={'H2O': 1})
c3.set_attr(T=70)
c4.set_attr(fluid={'R1234ZE(Z)': 1})
c5.set_attr(x=1)

#Lösen

nw.solve(mode='design')
nw.print_results()

# leider immer noch nicht genug Parameter. Anstatt der Temperaturdifferenzen könnten die Temperaturen
# aufgeschrieben werden.
# So könnte man noch für c5 die gleiche Temperatur wie für c4 notieren und hätte einen Parameter mehr.
# Selbst bei einer Vorgabe der Wärmemenge fehlen leider immer noch drei Parameter