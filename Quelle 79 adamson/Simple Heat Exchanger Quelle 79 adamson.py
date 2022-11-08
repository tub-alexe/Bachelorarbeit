from tespy.networks import Network
from tespy.components import (HeatExchangerSimple, Source, Sink, Compressor, Valve, Drum)
from tespy.connections import Connection
from CoolProp.CoolProp import PropsSI as CPSI

nw = Network(fluids=['H2O'], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

# Komponenten


vd = HeatExchangerSimple('Verdampfer')
vd_in = Source("Verdampfer rein")
vd_aus = Sink("Verdampfer raus")
dr = Drum("Dampftrommel")

# Verbindungen
c1 = Connection(vd_in, 'out1', dr, 'in1')
c2 = Connection(dr, 'out1', vd, 'in1')
c3 = Connection(vd, 'out1', dr, 'in2')
c4 = Connection(dr, 'out2', vd_aus, 'in1')
nw.add_conns(c1, c2, c3, c4)

# Parameter
#funktioniert wenn man aus dem c1 ein c2 macht, leider ist x bei c1 eigentlich unbekannt
vd.set_attr(pr=1, Q=240)

h_sat = CPSI("H", "Q", 0, "T", 273.15 + 75, 'H2O') / 1e3
c2.set_attr(h=h_sat)

p_vd = CPSI("P", "Q", 0.7, "T", 273.15 + 75, 'H2O') / 1e5
# enthalpy drum
h_dr = CPSI("H", "Q", 0.7, "T", 273.15 + 75, 'H2O') / 1e3
c3.set_attr(h=h_dr, p=p_vd, fluid={'H2O': 1})
#c2.set_attr(T=75, fluid={'H2O': 1})
#c3.set_attr(x=0.7)

# Lösen

nw.solve(mode='design')
nw.print_results()