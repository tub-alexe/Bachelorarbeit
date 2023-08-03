from tespy.networks import Network
from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink, DropletSeparator, Merge)
from tespy.connections import Connection, Bus
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
import plotly.graph_objects as go


wf = 'REFPROP::R1336mzz(Z)'
si = 'REFPROP::H2O'
fld_wf = {wf: 1, si: 0}
fld_si = {wf: 0, si: 1}

# Definition des Netwerks
nw = Network(fluids=[wf, si], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', iterinfo=False)

# Definition der Komponenten
GK = HeatExchanger('Gaskühler')
VD = HeatExchanger('Verdampfer')
DR1 = Valve('Drossel 1')
DR2 = Valve('Drossel 2')
KP1 = Compressor('Kompressor 1')
KP2 = Compressor('Kompressor 2')
IWUE = HeatExchanger("Interner Wärmeübertrager")
PH = DropletSeparator('Phasentrenner')
ZU = Merge('Zusammenführung', num_in=2)

# Definition der Quelle, Senke und des Kreislaufzusammenschlusses
se_ein = Source('Senke ein')
se_aus = Sink('Senke aus')

qu_ein = Source('Quelle ein')
qu_aus = Sink('Quelle aus')

KR = CycleCloser('Kreislaufzusammenschluss')

# Verbindungen des Kreislaufs
c21 = Connection(KR, 'out1', GK, 'in1', label="21")
c22 = Connection(GK, 'out1', IWUE, 'in1', label="22")
c23 = Connection(IWUE, 'out1', DR1, 'in1', label="23")
c24 = Connection(DR1, 'out1', PH, 'in1', label="24")
c25 = Connection(PH, 'out1', DR2, 'in1', label="25")
c26 = Connection(DR2, 'out1', VD, 'in2', label="26")
c27 = Connection(VD, 'out2', IWUE, 'in2', label="27")
c28 = Connection(IWUE, 'out2', KP1, 'in1', label="28")
c29 = Connection(KP1, 'out1', ZU, 'in1', label="29")
c30 = Connection(PH, 'out2', ZU, 'in2', label="30")
c31 = Connection(ZU, 'out1', KP2, 'in1', label="31")
c21_cc = Connection(KP2, 'out1', KR, 'in1', label="21_cc")

# Verbindungen der Quelle
c11 = Connection(qu_ein, 'out1', VD, 'in1', label="11")
c12 = Connection(VD, 'out1', qu_aus, 'in1', label="12")

# Verbindungen der Senke
c13 = Connection(se_ein, 'out1', GK, 'in2', label="13")
c14 = Connection(GK, 'out2', se_aus, 'in1', label="14")

nw.add_conns(c21, c22, c23, c24, c25, c26, c27, c28, c29, c30, c31, c21_cc, c11, c12, c13, c14)

# Setzen der Startparameter für die Komponenten
GK.set_attr(pr1=1, pr2=1, Q=-1e7)
IWUE.set_attr(pr1=1, pr2=1)
VD.set_attr(pr1=1, pr2=1)
KP1.set_attr(eta_s=0.76)
KP2.set_attr(eta_s=0.76)

# Setzen Startparameter der Verbindungen des Kreislaufs
h_c22 = CPSI("H", "P", 29 * 1e5, "T", 273.15+165, wf) * 1e-3
c22.set_attr(h=h_c22, p=29)

h_c27 = CPSI("H", "P", 5.5516 * 1e5, "T", 273.15+90.1, wf) * 1e-3
c27.set_attr(h=h_c27)

h_c28 = CPSI("H", "P", 5.5516 * 1e5, "T", 273.15+155, wf) * 1e-3
c28.set_attr(h=h_c28, p=5.5516, fluid={'R1336mzz(Z)': 1, 'H2O': 0})

c29.set_attr(p=12)

# Setzen Startparameter der Verbindungen der Quelle
c11.set_attr(T=95, p=5, fluid={'R1336mzz(Z)': 0, 'H2O': 1})
c12.set_attr(T=90)

# Setzen Startparameter der Verbindungen der Senke
c13.set_attr(T=160, p=20, fluid={'R1336mzz(Z)': 0, 'H2O': 1})
c14.set_attr(T=190)

#Lösen des Netzwerks
nw.solve(mode='design')
nw.print_results()

#Setzen der Betriebsparameter
c22.set_attr(h=None, p=29)
GK.set_attr(ttd_l=10)
c27.set_attr(h=None, Td_bp=0.1)
c28.set_attr(p=None, h=None)
VD.set_attr(ttd_l=5)
IWUE.set_attr(ttd_u=15)
c29.set_attr(p=11.83)

# Definition der Energieströme
el = Bus('elektrische Leistung')
el.add_comps(
    {'comp': KP1, 'char': 1, 'base': 'bus'},
    {'comp': KP2, 'char': 1, 'base': 'bus'})

wae_zu = Bus('Wärmezufuhr')
wae_zu.add_comps(
    {'comp': qu_ein, 'base': 'bus'},
    {'comp': qu_aus})

wae_ab = Bus('Wärmeabfuhr')
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
        'color': 'orange'},
    link=links),
    layout=go.Layout({'width': 1450})
    )
fig.update_layout(
    font_size=20
)
fig.show()

#Erstellung der Datensätze für das p_hoch-ε Diagramm
import matplotlib.pyplot as plt
import numpy as np

iterations = 40
iterations2 = 70
param = list(np.linspace(31, 31.2, iterations))
param2 = list(np.linspace(11.5, 12, iterations2))
eta = []
p_gk = []
Hochdruck = []
Mitteldruck = []
Wirkungsgrad = []
Tsink = []
#y = 0
#x = 0
#z = 0
#j = 0
#erster Parameter wird variiert
for p1 in param:
    c22.set_attr(p=p1)
    y = 0
    x = 0
    z = 0
    j = 0
    nw.solve(mode='design')
    ean.analyse(pamb=p_umg, Tamb=T_umg)

    #zweiter Parameter wird variiert
    for p2 in param2:

        VD.set_attr(pr1=1, pr2=1, ttd_l=None)
        GK.set_attr(pr1=1, pr2=1, Q=-1e7, ttd_l=None, ttd_u=None)
        IWUE.set_attr(pr1=1, pr2=1, ttd_u=None)
        KP1.set_attr(eta_s=0.76)
        KP2.set_attr(eta_s=0.76)

        # Setzen Startparameter der Verbindungen des Kreislaufs
        h_c22 = CPSI("H", "P", 29 * 1e5, "T", 273.15 + 165, wf) * 1e-3
        c22.set_attr(h=h_c22, p=29)

        h_c27 = CPSI("H", "P", 5.5516 * 1e5, "T", 273.15 + 90.1, wf) * 1e-3
        c27.set_attr(h=h_c27, Td_bp=None)

        h_c28 = CPSI("H", "P", 5.5516 * 1e5, "T", 273.15 + 155, wf) * 1e-3
        c28.set_attr(h=h_c28, p=5.5516, fluid={'R1336mzz(Z)': 1, 'H2O': 0})

        c29.set_attr(p=12)

        # Setzen Startparameter der Verbindungen der Quelle
        c11.set_attr(T=95, p=5, fluid={'R1336mzz(Z)': 0, 'H2O': 1})
        c12.set_attr(T=90)

        # Setzen Startparameter der Verbindungen der Senke
        c13.set_attr(T=160, p=20, fluid={'R1336mzz(Z)': 0, 'H2O': 1})
        c14.set_attr(T=190)

        # Lösen des Netzwerks
        nw.solve(mode='design')

        #Neues Setzen der zu untersuchenden Parameter
        c22.set_attr(h=None, p=p1)
        GK.set_attr(ttd_l=10)
        c27.set_attr(h=None, Td_bp=0.1)
        c28.set_attr(p=None, h=None)
        VD.set_attr(ttd_l=5)
        IWUE.set_attr(ttd_u=15)
        c29.set_attr(p=p2)

        # Lösen des Netzwerks und Durchführung einer Exergieanalyse
        nw.solve('design')
        ean.analyse(pamb=p_umg, Tamb=T_umg)

        if ean.network_data.loc['epsilon'] < y:

            # Abbruch der inneren Schleife falls mit diesem Zwischendruckniveau der Zustand des Fluids außerhalb des Zweiphasengebiets liegt
            if nw.get_conn('21').get_attr('p').val == 29.0:
                Hochdruck += [x]
                Mitteldruck += [z]
                Wirkungsgrad += [y * 100]
                Tsink += [j]
                break
            # Abbruch der inneren Schleife, falls der optimale Zwischendruck erreicht wurde
            elif nw.get_comp("Gaskühler").get_attr("ttd_u").val > 0:
                Hochdruck += [x]
                Mitteldruck += [z]
                Wirkungsgrad += [y * 100]
                Tsink += [j]
                print('Ausfahrt Nummer 1')
                break
            else:
                print('Ausfahrt Nummer 2')
                break

        elif ean.network_data.loc['epsilon'] > y:
            # Abbruch der inneren Schleife falls mit diesem Zwischendruckniveau der Zustand des Fluids außerhalb des Zweiphasengebiets liegt
            if nw.get_conn('21').get_attr('p').val == 29.0:
                Hochdruck += [x]
                Mitteldruck += [z]
                Wirkungsgrad += [y * 100]
                Tsink += [j]
                break

            # Neuspeicherung der Variablen, falls der optimale Zwischendruck noch nicht erreicht wurde
            else:
                y = ean.network_data.loc['epsilon']
                x = nw.get_conn("22").get_attr("p").val
                z = nw.get_conn("29").get_attr("p").val
                j = nw.get_conn("13").get_attr("T").val

q = np.array(Wirkungsgrad).argmax()
print('Mitteldruck = ', Mitteldruck[q])
print('Hochdruck = ', Hochdruck[q])
print('exergetischer Wirkungsgrad = ', Wirkungsgrad[q])

c29.set_attr(p=Mitteldruck[q])
param = list(np.linspace(29, 34.6, 60))

# Datensatz für die Exergieanalyse mit dem optimalen Zwischendruck
for p3 in param:
    c22.set_attr(p=p3)
    nw.solve('design')
    ean.analyse(pamb=p_umg, Tamb=T_umg)
    eta += [ean.network_data.loc['epsilon'] * 100]
    p_gk += [nw.get_conn("22").get_attr("p").val]

plt.plot(param, eta, marker='x', color="#1f567d")
plt.xlabel('Gaskühler-/Kondensatordruck [bar]')
plt.ylabel('exergetischer Wirkungsgrad [%]')
plt.tight_layout()
plt.show()

import json

with open('Zweistufenkompression.txt', 'a') as convert_file:
    convert_file.write(json.dumps(p_gk) + "\n")

with open('Zweistufenkompression.txt', 'a') as convert_file:
    convert_file.write(json.dumps(eta) + "\n")

f = open("Zweistufenkompression.txt", "r")
print(f.read())