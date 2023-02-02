from tespy.networks import Network
from tespy.components import (Source, Sink, Valve, HeatExchanger, Compressor, CycleCloser, Pump, Turbine,
                              DropletSeparator, HeatExchangerSimple, Merge)
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
src_co1 = Source('Source Cooling1')
src_co2 = Source('Source Cooling2')
snk_co1 = Sink('Sink Cooling1')
snk_co2 = Sink('Sink Cooling2')
src_gh = Source('geothermy-source')
src_hea = Source('District Heat Source')
snk_hea = Sink('District Heat Sink')
snk_gh = Sink('geothermy-sink')
cp = Compressor('Compressor')
tu = Turbine('Steam Turbine')
tu2 = Turbine('Steam Turbine 2')
ihx = HeatExchanger('Internal Heat Exchanger')
eco1 = HeatExchanger('Economizer1')
eco2 = HeatExchanger('Economizer2   ')
fl = DropletSeparator("Flash Tank")
pu1 = Pump('Pump1')
pu2 = Pump('Pump2')
cd1 = HeatExchanger('Condenser1')
cd2 = HeatExchanger('Condenser2')
mg = Merge('Merge')

c1 = Connection(src_gh, 'out1', fl, 'in1')
c2 = Connection(fl, 'out1', ihx, 'in1')
c3 = Connection(ihx, 'out1', eco2, 'in1')
c4 = Connection(fl, 'out2', tu, 'in1')
c5 = Connection(tu, 'out1', ihx, 'in2')
c6 = Connection(ihx, 'out2', tu2, 'in1')
c7 = Connection(tu2, 'out1', eco1, 'in1')
c8 = Connection(eco1, 'out1', cd1, 'in1')
c9 = Connection(eco2, 'out1', cd2, 'in1')
c10 = Connection(src_hea, 'out1', eco1, 'in2')
c11 = Connection(eco1, 'out2', eco2, 'in2')
c12 = Connection(eco2, 'out2', snk_hea, 'in1')
c13 = Connection(cd1, 'out1', pu1, 'in1')
c14 = Connection(cd2, 'out1', pu2, 'in1')

c15 = Connection(src_co1, 'out1', cd1, 'in2')
c16 = Connection(cd1, 'out2', snk_co1, 'in1')
c17 = Connection(src_co2, 'out1', cd2, 'in2')
c18 = Connection(cd2, 'out2', snk_co2, 'in1')
c19 = Connection(pu1, 'out1', mg, 'in1')
c20 = Connection(pu2, 'out1', mg, 'in2')
c21 = Connection(mg, 'out1', snk_gh, 'in1')
geo.add_conns(c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20, c21)

tu.set_attr(eta_s=0.9)
tu2.set_attr(eta_s=0.9)
pu1.set_attr(eta_s=0.8)
pu2.set_attr(eta_s=0.8)
ihx.set_attr(pr1=1, pr2=1)
eco1.set_attr(pr1=1, pr2=1, ttd_u=5)
eco2.set_attr(pr1=1, pr2=1)
cd1.set_attr(pr1=1, pr2=1, ttd_u=10)
cd2.set_attr(pr1=1, pr2=1, ttd_u=10)

h_c1 = CPSI("H", "P", 10.8 * 1e5, "Q", 0.45, wf) * 1e-3
c1.set_attr(h=h_c1, p=10.8, m=500, fluid=fld_wf)
p5 = 4.632
c5.set_attr(p=p5)
h_c6 = CPSI("H", "P", p5 * 1e5, "Q", 0.986, wf) * 1e-3
c6.set_attr(h=h_c6)
c7.set_attr(p=0.91)
c8.set_attr(x=0)

c10.set_attr(T=50, p=10, fluid=fld_wf)
#c11.set_attr(T=92)
c12.set_attr(T=100)

h_c13 = CPSI("H", "P", 0.91 * 1e5, "T", 273.15 + 55, wf) * 1e-3
c13.set_attr(h=h_c13)

h_c14 = CPSI("H", "P", 10.8 * 1e5, "T", 273.15 + 55, wf) * 1e-3
c14.set_attr(h=h_c14)

h_c15 = CPSI("H", "P", 10 * 1e5, "T", 273.15 + 15, wf) * 1e-3
c15.set_attr(h=h_c15, p=10, fluid=fld_wf)

h_c17 = CPSI("H", "P", 10 * 1e5, "T", 273.15 + 15, wf) * 1e-3
c17.set_attr(h=h_c17, p=10, fluid=fld_wf)

c19.set_attr(p=30)
geo.solve(mode='design')
geo.print_results()


c1.set_attr(h=None, x=0.45)
c5.set_attr(p=None, x=0.95)
c6.set_attr(h=None)
ihx.set_attr(ttd_l=20)
c7.set_attr(p=None, T=97)
c13.set_attr(h=None, T=55)
c14.set_attr(h=None, T=55)
c15.set_attr(h=None, T=15)
c17.set_attr(h=None, T=15)

# busses
power_output = Bus('power output')
power_output.add_comps(
    {'comp': tu},
    {'comp': tu2},
    {'comp': pu1, 'base': 'bus'},
    {'comp': pu2, 'base': 'bus'}
)


heat_product = Bus('heating')
heat_product.add_comps(
    {'comp': src_hea, 'base': 'bus'},
    {'comp': snk_hea})

geo_input = Bus('geothermie heat')
geo_input.add_comps(
    {'comp': src_gh, 'base': 'bus'},
    {'comp': snk_gh})

cooling = Bus('cooling')
cooling.add_comps(
    {'comp': src_co1, 'base': 'bus'},
    {'comp': src_co2, 'base': 'bus'},
    {'comp': snk_co1},
    {'comp': snk_co2})



geo.add_busses(power_output, heat_product, geo_input)

geo.solve(mode='design')
geo.print_results()

# Exergy Analysis

pamb = 1
Tamb = 25

ean = ExergyAnalysis(geo, E_P=[heat_product, power_output], E_F=[geo_input], E_L=[cooling])
ean.analyse(pamb=pamb, Tamb=Tamb)
ean.print_results()
print(ean.network_data.loc['epsilon'])