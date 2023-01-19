import numpy as np
import pygmo as pg

from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink, Splitter, DropletSeparator, Separator)
from tespy.connections import Bus
from tespy.connections import Connection
from tespy.networks import Network
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
from tespy.tools.optimization import OptimizationProblem
from fluprodia import FluidPropertyDiagram


wf = 'R1233ZD(E)'
si = 'H2O'
fld_wf = {wf: 1, si: 0}
fld_si = {wf: 0, si: 1}

nw = Network(fluids=[wf, si], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

Sou = Source('Source')
Si = Sink('Sink')
Si2 = Sink('Sink2')
va_1 = Valve('Valve 1')
va_2 = Valve('Valve 2')
sp = DropletSeparator('Seperator')
ihx_1 = HeatExchanger('Internal Heat Exchanger 1')
ihx_2 = HeatExchanger('Internal Heat Exchanger 2')


c1 = Connection(Sou, 'out1', Si, 'in1')
#c2 = Connection(ihx_2, 'out1', va_2, 'in1')
#c3 = Connection(va_2, 'out1', sp, 'in1')
#c4 = Connection(sp, 'out2', ihx_2, 'in2')
#c5 = Connection(ihx_2, 'out2', Si2, 'in1')
#c6 = Connection(sp, 'out1', Si, 'in1')
#c7 = Connection(ihx_1, 'out1', Si, 'in1')
nw.add_conns(c1)

#ihx_1.set_attr(pr1=1, pr2=1)
#ihx_2.set_attr(pr1=1, pr2=1)

print(CPSI("H", "P", 13.9 * 1e5, "Q", 0, wf) * 1e-3)

h_c1 = CPSI("H", "P", 13.9 * 1e5, "Q", 0, wf) * 1e-3
c1.set_attr(h=h_c1, p=13.9, m=10, fluid=fld_wf)

#h_c2 = CPSI("H", "P", 41 * 1e5, "T", 273.15+118, wf) * 1e-3
#c2.set_attr(h=h_c2)
#c3.set_attr(p=8)
#h_c5 = CPSI("H", "P", 8 * 1e5, "T", 273.15+114, wf) * 1e-3
#c5.set_attr(h=h_c5)

nw.solve(mode='design')
nw.print_results()





