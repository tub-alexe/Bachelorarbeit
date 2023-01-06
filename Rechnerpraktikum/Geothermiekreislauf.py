from tespy.networks import Network
from tespy.components import (Source, Sink, Valve, HeatExchanger, Compressor, CycleCloser, Pump, Turbine,
                              DropletSeparator, HeatExchangerSimple)
from tespy.connections import Connection, Bus
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
from fluprodia import FluidPropertyDiagram

#fluid definitions
wf = 'water'
sf = 'air'
fld_wf = {wf: 1, sf: 0}
fld_sf = {wf: 0, sf: 1}

#network
geo = Network(fluids=[wf, sf],  T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s')

#components
src_gh = Source('geothermy-source')
src_hea = Source('District Heat Source')
snk_wf = Sink('working-fluid-sink')
snk_wf_2 = Sink('working-fluid-sink 2')
cp = Compressor('Compressor')
tu = Turbine('Steam Turbine')
tu2 = Turbine('Steam Turbine 2')
ihx = HeatExchanger('Internal Heat Exchanger')
fl = DropletSeparator("Flash Tank")
pu = Pump('Pump')
cd = HeatExchangerSimple('Condenser')

c1 = Connection(src_gh, 'out1', fl, 'in1')
c2 = Connection(fl, 'out1', ihx, 'in1')
c3 = Connection(ihx, 'out1', snk_wf, 'in1')
c4 = Connection(fl, 'out2', tu, 'in1')
c5 = Connection(tu, 'out1', ihx, 'in2')
c6 = Connection(ihx, 'out2', tu2, 'in1')
c7 = Connection(tu2, 'out1', snk_wf_2, 'in1')

geo.add_conns(c1, c2, c3, c4, c5, c6, c7)

cd.set_attr(pr=1)
tu.set_attr(eta_s=0.9)
tu2.set_attr(eta_s=0.9)
pu.set_attr(eta_s=0.8)
ihx.set_attr(pr1=1, pr2=1)

h_c1 = CPSI("H", "P", 10.8 * 1e5, "Q", 0.45, wf) * 1e-3
c1.set_attr(h=h_c1, p=10.8, m=500, fluid=fld_wf)
p5 = 1.477
c5.set_attr(p=p5)
h_c6 = CPSI("H", "P", p5 * 1e5, "Q", 1, wf) * 1e-3
c6.set_attr(h=h_c6)
c7.set_attr(p=0.4812)

geo.solve(mode='design')
geo.print_results()