#Import
from tespy.networks import Network
from tespy.components import (Sink, Source, Compressor)
from tespy.connections import Connection

# general
nw = Network(fluids=['R245FA'], T_unit='C', p_unit='bar',
             h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

# sources and sinks
src_fluid = Source('fluid-in')
snk_fluid = Sink ('fluid-out')

# components
cmp_COMP = Compressor('Compressor')

#Connections
c1 = Connection(src_fluid, 'out1', cmp_COMP, 'in1', label='1')
c2 = Connection(cmp_COMP, 'out1', snk_fluid, 'in1', label='2')
nw.add_conns(c1, c2)

c1.set_attr(fluid={'R245FA': 1},p=1,T=25,m=1)
c2.set_attr(p=10)
cmp_COMP.set_attr(eta_s=0.9)

nw.solve(mode='design')
nw.print_results()