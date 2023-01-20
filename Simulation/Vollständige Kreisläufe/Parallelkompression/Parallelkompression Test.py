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


c1 = Connection(Sou, 'out1', va_1, 'in1')
c2 = Connection(va_1, 'out1', sp, 'in1')
c3 = Connection(sp, 'out1', Si, 'in1')
c4 = Connection(sp, 'out2', Si2, 'in1')

nw.add_conns(c1, c2, c3, c4)

ihx_1.set_attr(pr1=1, pr2=1)
ihx_2.set_attr(pr1=1, pr2=1)

h_c1 = CPSI("H", "P", 41 * 1e5, "T", 273.15+118, wf) * 1e-3
c1.set_attr(h=h_c1-0.1, p=41, m=10, fluid=fld_wf)

c2.set_attr(p=8.1)
#ohne Phasentrenner bis 12.6 möglich, mit Phasentrenner erst ab 8 bar möglich

nw.solve(mode='design')
nw.print_results()

#log p,h- diagram
result_dict = {}
result_dict.update({va_1.label: va_1.get_plotting_data()[1]})


diagram = FluidPropertyDiagram(wf)
diagram.set_unit_system(T='°C', p='bar', h='kJ/kg')

for key, data in result_dict.items():
    result_dict[key]['datapoints'] = diagram.calc_individual_isoline(**data)

diagram.calc_isolines()
diagram.set_limits(x_min=0, x_max=900, y_min=1e-1, y_max=2e2)
diagram.draw_isolines('logph')

for key in result_dict.keys():
    datapoints = result_dict[key]['datapoints']
    diagram.ax.plot(datapoints['h'], datapoints['p'], color='#ff0000')
    diagram.ax.scatter(datapoints['h'][0], datapoints['p'][0], color='#ff0000')


diagram.save('Test2.png', dpi=300)
