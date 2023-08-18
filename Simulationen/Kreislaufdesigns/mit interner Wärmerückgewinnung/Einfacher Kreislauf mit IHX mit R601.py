from tespy.networks import Network
from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink)
from tespy.connections import Connection, Bus
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
import plotly.graph_objects as go

wf = 'REFPROP::Pentane'
si = 'REFPROP::H2O'

# Definition des Netwerks
nw = Network(fluids=[wf, si], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

# Definition der Komponenten
GK = HeatExchanger('Gaskühler')
VD = HeatExchanger('Verdampfer')
DR = Valve('Drossel')
KP = Compressor('Kompressor')
IWUE = HeatExchanger("Interner Wärmeübertrager")

#Definition der Quelle, Senke und des Kreislaufzusammenschlusses
se_ein = Source('Senke ein')
se_aus = Sink('Senke aus')

qu_ein = Source('Quelle ein')
qu_aus = Sink('Quelle aus')

KR = CycleCloser('Kreislaufzusammenschluss')

# Verbindungen des Kreislaufs
c21 = Connection(KR, 'out1', GK, 'in1', label="21")
c22 = Connection(GK, 'out1', IWUE, 'in1', label="22")
c23 = Connection(IWUE, 'out1', DR, 'in1', label="23")
c24 = Connection(DR, 'out1', VD, 'in2', label="24")
c25 = Connection(VD, 'out2', IWUE, 'in2', label="25")
c26 = Connection(IWUE, 'out2', KP, 'in1', label="26")
c21_cc = Connection(KP, 'out1', KR, 'in1', label="21_cc")

# Verbindungen der Quelle
c11 = Connection(qu_ein, 'out1', VD, 'in1', label="11")
c12 = Connection(VD, 'out1', qu_aus, 'in1', label="12")

# Verbindungen der Senke
c13 = Connection(se_ein, 'out1', GK, 'in2', label="13")
c14 = Connection(GK, 'out2', se_aus, 'in1', label="14")

nw.add_conns(c21, c22, c23, c24, c25, c26, c21_cc, c11, c12, c13, c14)

# Setzen der Startparameter der Komponenten
GK.set_attr(pr1=1, pr2=1, Q=-1e7)
IWUE.set_attr(pr1=1, pr2=1)
VD.set_attr(pr1=1, pr2=1)
KP.set_attr(eta_s=0.76)

# Setzen Startparameter der Verbindungen des Kreislaufs
h_c26 = CPSI("H", "P", 4.706 * 1e5, "T", 273.15+168, wf) * 1e-3
c26.set_attr(h=h_c26, p=4.706, fluid={'Pentane': 1, 'H2O': 0})

h_c22 = CPSI("H", "P", 34 * 1e5, "T", 273.15+178, wf) * 1e-3
c22.set_attr(h=h_c22, p=34)

h_c25 = CPSI("H", "P", 4.706 * 1e5, "T", 273.15+90.1, wf) * 1e-3
c25.set_attr(h=h_c25)

# Setzen Startparameter der Verbindungen der Quelle
c11.set_attr(T=95, p=5, fluid={'Pentane': 0, 'H2O': 1})
c12.set_attr(T=90)

# Setzen Startparameter der Verbindungen der Senke
c13.set_attr(T=160, p=20, fluid={'Pentane': 0, 'H2O': 1})
c14.set_attr(T=190)

# Lösen des Netzwerks
nw.solve(mode='design')
nw.print_results()

# Setzen der Betriebsparameter
c22.set_attr(h=None, p=25)
GK.set_attr(ttd_l=10)
c25.set_attr(h=None, Td_bp=0.1)
c26.set_attr(p=None, h=None)
VD.set_attr(ttd_l=5)
IWUE.set_attr(ttd_u=15)

# Definition der Energieströme
el = Bus('elektrische Leistung')
el.add_comps(
    {'comp': KP, 'char': 1, 'base': 'bus'})

wae_zu = Bus('Wärmequelle')
wae_zu.add_comps(
    {'comp': qu_ein, 'base': 'bus'},
    {'comp': qu_aus})

wae_ab = Bus('Wärmesenke')
wae_ab.add_comps(
    {'comp': se_ein, 'base': 'bus'},
    {'comp': se_aus})

nw.add_busses(el, wae_zu, wae_ab)

#Lösen des Netzwerks
nw.solve(mode='design')
nw.print_results()

#Durchführung der Exergianalyse
p_umg = 1
T_umg = 25

ean = ExergyAnalysis(nw, E_P=[wae_ab], E_F=[el, wae_zu])
ean.analyse(pamb=p_umg, Tamb=T_umg)
ean.print_results()
print(ean.network_data.loc['epsilon'])


# Erstellung des Grassmanndiagramms
links, nodes = ean.generate_plotly_sankey_input()
fig = go.Figure(go.Sankey(
    arrangement="snap",
    node={
        "label": nodes,
        'pad': 11,
        "line": dict(width=0.5),
        'color': 'orange'},
    link=links),
    layout=go.Layout({'width': 1450})
    )
fig.update_layout(
    font_size=20
)
fig.show()

# Erstellung der Datensätze für die p_hoch-ε Kuven bei konstanten Senkentemperaturen oder Linien konstanter oberer Temperaturdifferenz im Gaskühler/Kondensator durch Variierung der Senkenein- oder Senkenaustrittstemperatur
import matplotlib.pyplot as plt
import numpy as np

iterations = 80

param = list(np.linspace(24.63, 40, iterations))
eta = []
p_gk = []


for p in param:
    c22.set_attr(p=p)
    #c13.set_attr(T=p)
    #c14.set_attr(T=p)
    nw.solve('design')
    ean.analyse(pamb=p_umg, Tamb=T_umg)
    eta += [ean.network_data.loc['epsilon'] * 100]
    p_gk += [nw.get_conn("22").get_attr("p").val]

q = np.array(eta).argmax()
print('Hochdruck = ', p_gk[q])
print('exergetischer Wirkungsgrad = ', eta[q])
plt.plot(param, eta, marker='x', color="#1f567d")
plt.xlabel('Gaskühler-/Kondensatordruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
plt.tight_layout()
plt.show()

#Übergabe der Daten
import json

with open('Senkeneintrittstemperatur.txt', 'a') as convert_file:
    convert_file.write(json.dumps(p_gk) + "\n")

with open('Senkeneintrittstemperatur.txt', 'a') as convert_file:
    convert_file.write(json.dumps(eta)+"\n")

#with open('Senkeneintrittstemperatur.txt', 'a') as convert_file:
    #convert_file.write(json.dumps(param)+"\n")


f = open("Senkeneintrittstemperatur.txt", "r")
print(f.read())


