from tespy.components import (Source, Sink)
from tespy.connections import Connection
from tespy.networks import Network
from CoolProp.CoolProp import PropsSI as CPSI

f = 'R1233ZD(E)'
fld_f = {f: 1}

nw = Network(fluids=[f], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s')

Sou = Source('Source')
Si = Sink('Sink')

c1 = Connection(Sou, 'out1', Si, 'in1')
nw.add_conns(c1)

print(CPSI("H", "P", 13.9 * 1e5, "Q", 0, f) * 1e-3)

h_c1 = CPSI("H", "P", 13.9 * 1e5, "Q", 0, f) * 1e-3
c1.set_attr(h=h_c1, p=13.9, m=10, fluid=fld_f)

nw.solve(mode='design')
nw.print_results()





