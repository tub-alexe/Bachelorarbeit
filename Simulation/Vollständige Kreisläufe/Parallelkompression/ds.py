from tespy.components import (Valve, Source, Sink, DropletSeparator)
from tespy.connections import Connection
from tespy.networks import Network
from CoolProp.CoolProp import PropsSI as CPSI

wf = 'R1233ZD(E)'
fld_wf = {wf: 1}

nw = Network(fluids=[wf], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s')

Sou = Source('Source')
Si1 = Sink('Sink1')
Si2 = Sink('Sink2')
va = Valve('Valve')
sp = DropletSeparator('Seperator')


c1 = Connection(Sou, 'out1', va, 'in1')
c2 = Connection(va, 'out1', sp, 'in1')
c3 = Connection(sp, 'out1', Si1, 'in1')
c4 = Connection(sp, 'out2', Si2, 'in1')

nw.add_conns(c1, c2, c3, c4)

h_c1 = CPSI("H", "P", 41 * 1e5, "T", 273.15+118, wf) * 1e-3
#h_c1 = CPSI("H", "P", 10 * 1e5, "Q", 0, wf) * 1e-3
c1.set_attr(h=h_c1-0.1, p=41, m=10, fluid=fld_wf)

c2.set_attr(p=8.1)

nw.solve(mode='design')
nw.print_results()
