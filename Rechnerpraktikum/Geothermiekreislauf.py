from tespy.networks import Network
from tespy.components import (Source, Sink, Valve, HeatExchanger, Compressor, CycleCloser, Pump, Turbine,
                              DropletSeparator, HeatExchangerSimple, Merge, Splitter)
from tespy.connections import Connection, Bus
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
from fluprodia import FluidPropertyDiagram

#fluid definitions
wa = 'water'
lu = 'air'
fld_wa = {wa: 1, lu: 0}
fld_lu = {wa: 0, lu: 1}

#network
geo = Network(fluids=[wa, lu],  T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s')

#components
qu_ko1 = Source('Kühl-Quelle 1')
qu_ko2 = Source('Kühl-Quelle 2')
qu_ko3 = Source('Kühl-Quelle 3')
qu_geo = Source('Geothermie-Quelle')
qu_fw = Source('Fernwärme-Quelle')
snk_ko1 = Sink('Kühl-Senke 1')
snk_ko2 = Sink('Kühl-Senke 2')
snk_ko3 = Sink('Kühl-Senke 3')
snk_geo = Sink('Geothermie-Senke')
snk_fw = Sink('Fernwärme-Senke')

tu1 = Turbine('Dampfurbine 1')
tu2 = Turbine('Dampfurbine 2')
tu3 = Turbine('Dampfurbine 3')
iwü = HeatExchanger('Interner Wärmeübertrager')
wü1 = HeatExchanger('Wärmeübertrager 1')
wü2 = HeatExchanger('Wärmeübertrager 2')
pht = DropletSeparator("Phasentrenner")
pu1 = Pump('Pumpe1')
pu2 = Pump('Pumpe2')
pu3 = Pump('Pumpe3')
kd1 = HeatExchanger('Kondensator1')
kd2 = HeatExchanger('Kondensator2')
kd3 = HeatExchanger('Kondensator3')
zu = Merge('Zusammenführung', num_in=3)
sp = Splitter('Splitter')

D1 = Connection(qu_geo, 'out1', pht, 'in1', label="D1")
D2 = Connection(pht, 'out2', tu1, 'in1', label="D2")
D3 = Connection(tu1, 'out1', iwü, 'in2', label="D3")
D4 = Connection(iwü, 'out2', tu2, 'in1', label="D4")
D5_sep = Connection(tu2, 'out1', sp, 'in1', label="D5_sep")
D5 = Connection(sp, 'out2', tu3, 'in1', label="D5")
D6 = Connection(tu3, 'out1', kd3, 'in1', label="D6")
D7 = Connection(sp, 'out1', wü1, 'in1', label="D7")

W1 = Connection(pht, 'out1', iwü, 'in1', label="W1")
W2 = Connection(iwü, 'out1', wü2, 'in1', label="W2")
W3 = Connection(qu_fw, 'out1', wü1, 'in2', label="W3")
W4 = Connection(wü1, 'out2', wü2, 'in2', label="W4")
W5 = Connection(wü2, 'out2', snk_fw, 'in1', label="W5")
W6 = Connection(wü1, 'out1', kd1, 'in1', label="W6")
W7 = Connection(wü2, 'out1', kd2, 'in1', label="W7")
W8 = Connection(kd1, 'out1', pu1, 'in1', label="W8")
W9 = Connection(kd2, 'out1', pu2, 'in1', label="W9")
W10 = Connection(pu1, 'out1', zu, 'in1', label="W10")
W11 = Connection(pu2, 'out1', zu, 'in2', label="W11")
W12 = Connection(kd3, 'out1', pu3, 'in1', label="W12")
W13 = Connection(pu3, 'out1', zu, 'in3', label="W13")
W14 = Connection(zu, 'out1', snk_geo, 'in1', label="W14")

K1 = Connection(qu_ko1, 'out1', kd1, 'in2', label="K1")
K2 = Connection(kd1, 'out2', snk_ko1, 'in1', label="K2")
K3 = Connection(qu_ko2, 'out1', kd2, 'in2', label="K3")
K4 = Connection(kd2, 'out2', snk_ko2, 'in1', label="K4")
K5 = Connection(qu_ko3, 'out1', kd3, 'in2', label="K5")
K6 = Connection(kd3, 'out2', snk_ko3, 'in1', label="K6")
geo.add_conns(D1, D2, D3, D4, D5_sep, D5, D6, D7, W1, W2, W3, W4, W5, W6, W7, W8, W9, W10, W11, W12, W13, W14, K1, K2, K3,
              K4, K5, K6)

tu1.set_attr(eta_s=0.9)
tu2.set_attr(eta_s=0.9)
tu3.set_attr(eta_s=0.9)
pu1.set_attr(eta_s=0.8)
pu2.set_attr(eta_s=0.8)
pu3.set_attr(eta_s=0.8)
iwü.set_attr(pr1=1, pr2=1)
wü1.set_attr(pr1=1, pr2=1, ttd_u=5)
wü2.set_attr(pr1=1, pr2=1)
kd1.set_attr(pr1=1, pr2=1, ttd_u=10)
kd2.set_attr(pr1=1, pr2=1, ttd_u=25)
kd3.set_attr(pr1=1, pr2=1, ttd_u=5)

h_D1 = CPSI("H", "P", 10.8 * 1e5, "Q", 0.45, wa) * 1e-3
D1.set_attr(h=h_D1, p=10.8, m=500, fluid=fld_wa)
p5 = 4.632
D3.set_attr(p=p5)
h_c6 = CPSI("H", "P", p5 * 1e5, "Q", 0.986, wa) * 1e-3
D4.set_attr(h=h_c6)
h_D7 = CPSI("H", "P", 0.939 * 1e5, "Q", 0.913, wa) * 1e-3
D7.set_attr(h=h_D7)
D5.set_attr(m=50)
D6.set_attr(x=0.9)

h_c7_pu3 = CPSI("H", "P", 30 * 1e5, "T", 273.15 + 55, wa) * 1e-3
W12.set_attr(h=h_c7_pu3)

W6.set_attr(x=0)

W3.set_attr(T=50, p=10, fluid=fld_wa)

W5.set_attr(T=100)

h_W8 = CPSI("H", "P", 0.91 * 1e5, "T", 273.15 + 55, wa) * 1e-3
W8.set_attr(h=h_W8)

h_W9 = CPSI("H", "P", 10.8 * 1e5, "T", 273.15 + 55, wa) * 1e-3
W9.set_attr(h=h_W9)

h_K1 = CPSI("H", "P", 1.013 * 1e5, "T", 273.15 + 15, wa) * 1e-3
K1.set_attr(h=h_K1, p=1.013, fluid=fld_wa)

h_K3 = CPSI("H", "P", 1.013 * 1e5, "T", 273.15 + 15, lu) * 1e-3
K3.set_attr(h=h_K3, p=1.013, fluid=fld_lu)

W10.set_attr(p=30)

h_K5 = CPSI("H", "P", 1.013 * 1e5, "T", 273.15 + 15, lu) * 1e-3
K5.set_attr(h=h_K5, p=1.013, fluid=fld_lu)
geo.solve(mode='design')
geo.print_results()


D1.set_attr(h=None, x=0.45)
D3.set_attr(p=None, x=0.95)
D4.set_attr(h=None)
iwü.set_attr(ttd_l=20)
D7.set_attr(h=None, x=0.913)
W8.set_attr(h=None, T=55)
W9.set_attr(h=None, T=55)
W12.set_attr(h=None, T=55)
K1.set_attr(h=None, T=15)
K3.set_attr(h=None, T=15)
K5.set_attr(h=None, T=15)

# busses
power_output = Bus('power output')
power_output.add_comps(
    {'comp': tu1, 'char': 0.985},
    {'comp': tu2, 'char': 0.985},
    {'comp': tu3, 'char': 0.985},
    {'comp': pu1, 'char': 0.975, 'base': 'bus'},
    {'comp': pu2, 'char': 0.975, 'base': 'bus'},
    {'comp': pu3, 'char': 0.975, 'base': 'bus'})


heat_product = Bus('heating')
heat_product.add_comps(
    {'comp': qu_fw, 'base': 'bus'},
    {'comp': snk_fw})

geo_input = Bus('geothermie heat')
geo_input.add_comps(
    {'comp': qu_geo, 'base': 'bus'},
    {'comp': snk_geo})

cooling = Bus('cooling')
cooling.add_comps(
    {'comp': qu_ko1, 'base': 'bus'},
    {'comp': qu_ko2, 'base': 'bus'},
    {'comp': qu_ko3, 'base': 'bus'},
    {'comp': snk_ko1},
    {'comp': snk_ko2},
    {'comp': snk_ko3})

heat_product_eta = Bus('heating eta')
heat_product_eta.add_comps(
    {'comp': wü1, 'base': 'bus'},
    {'comp': wü2, 'base': 'bus'},
)

geo.add_busses(power_output, heat_product, geo_input, heat_product_eta)

geo.solve(mode='design')
geo.print_results()

# Exergy Analysis

pamb = 1.013
Tamb = 15

ean = ExergyAnalysis(geo, E_P=[heat_product, power_output], E_F=[geo_input], E_L=[cooling])
ean.analyse(pamb=pamb, Tamb=Tamb)
ean.print_results()

print(ean.network_data.loc['epsilon'])
print('elektrische Leistung', abs(power_output.P.val * 1e-6))
print('thermische Leistung', abs(heat_product_eta.P.val * 1e-6))
a = abs(power_output.P.val * 1e-6)
b = abs(heat_product_eta.P.val * 1e-6)
c = (geo.get_conn("D1").get_attr("h").val * geo.get_conn("D1").get_attr("m").val -geo.get_conn("W14").get_attr("h").val * geo.get_conn("W14").get_attr("m").val) * 1e-3

print('Wirkungsgrad', (a+b)/c)
