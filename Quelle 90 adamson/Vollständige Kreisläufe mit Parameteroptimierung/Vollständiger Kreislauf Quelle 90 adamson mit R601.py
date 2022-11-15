from tespy.networks import Network
from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink)
from tespy.connections import Connection
from CoolProp.CoolProp import PropsSI as CPSI

km = 'R601'
se = 'H2O'
fld_km = {km: 1, se: 0}
fld_se = {km: 0, se: 1}

nw = Network(fluids=[km, se], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

# Komponenten

gk = HeatExchanger('Gaskühler')
se_ein = Source('Senke ein')
se_aus = Sink('Senke aus')

ue_in = Source('Verdampfer rein')
vd_aus = Sink('Überhitzer raus')
vd = HeatExchanger('Verdampfer')
ue = HeatExchanger('Überhitzer')

exp = Valve('Expansionsventil')
kp = Compressor('Kompressor')
cc = CycleCloser('Kreilaufzusammenschluss')

#Verbindungen Kreislauf

c1 = Connection(cc, 'out1', gk, 'in1')
c2 = Connection(gk, 'out1', exp, 'in1')
c3 = Connection(exp, 'out1', vd, 'in2')
c4 = Connection(vd, 'out2', ue, 'in2')
c5 = Connection(ue, 'out2', kp, 'in1')
c6 = Connection(kp, 'out1', cc, 'in1')

#Verbindungen kalte Seite Gaskühler

c7 = Connection(se_ein, 'out1', gk, 'in2')
c8 = Connection(gk, 'out2', se_aus, 'in1')


#Verbindungen heiße Seite Verdampfer und Überhitzer
c9 = Connection(ue_in, 'out1', ue, 'in1')
c10 = Connection(ue, 'out1', vd, 'in1')
c11 = Connection(vd, 'out1', vd_aus, 'in1')
nw.add_conns(c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11)

#Parametrisierung Komponenten

gk.set_attr(pr1=1, pr2=1)
vd.set_attr(pr1=1, pr2=1)
ue.set_attr(pr1=1, pr2=1)
kp.set_attr(eta_s=0.7)
# Parametrisierung heiße Seite, vor dem Gaskühler

h_gk_vor = CPSI("H", "P", 36 * 1e5, "T", 273.15+204, km) * 1e-3
#c1.set_attr(h=h_gk_vor)

# Parametrisierung heiße Seite, nach dem Gaskühler, Druck bleibt konstant im Gaskühler

h_gk_nach = CPSI("H", "P", 36 * 1e5, "T", 273.15+105, km) * 1e-3
c2.set_attr(h=h_gk_nach, p=36)

# Parameter kalte Seite
# Vor dem Verdampfer

#h_verd = CPSI("H", "Q", 0, "T", 273.15+70, km) * 1e-3
c3.set_attr(p=2.8)

# Zwischen Verdampfer und Überhitzer
h_zw = CPSI("H", "P", 2.8 * 1e5, "T", 273.15+70, km) * 1e-3
c4.set_attr(h=h_zw)

# Nach dem Überhitzer
h_uebe = CPSI("H", "P", 2.8 * 1e5, "T", 273.15+75, km) * 1e-3
c5.set_attr(h=h_uebe, fluid=fld_km)

#Parametrisierung kalte Seite Gaskühler

c7.set_attr(T=100, p=20, fluid=fld_se)
c8.set_attr(T=200)

#Parameter heiße Seite Verdampfer
c9.set_attr(T=80, m=5, p=5, fluid=fld_se)
c11.set_attr(T=75)

#Lösen

nw.solve(mode='design')
nw.print_results()
print(f'COP = {abs(gk.Q.val) / kp.P.val}')

#c1.set_attr(h=None, T=204)
c2.set_attr(h=None, T=105)
c4.set_attr(h=None, T=70)
c5.set_attr(h=None, T=75)


nw.solve(mode='design')
nw.print_results()
print(f'COP = {abs(gk.Q.val) / kp.P.val}')


import matplotlib.pyplot as plt
import numpy as np

# make text reasonably sized
plt.rc('font', **{'size': 18})


data = {
    'p_verd': np.linspace(1.1, 2.8, 19),
    'p_kond': np.linspace(36, 55, 20),
    'eta_s': np.linspace(0.7, 0.82, 5) * 100
}
COP = {
    'p_verd': [],
    'p_kond': [],
    'eta_s': []
}
description = {
    'p_verd': 'Verdampferdruck in bar',
    'p_kond': 'Kondensatordruck in bar',
    'eta_s': 'Isentroper Wirkungsgrad in %'
}

for p in data['p_verd']:
    c3.set_attr(p=p)
    nw.solve('design')
    COP['p_verd'] += [abs(gk.Q.val) / kp.P.val]

# reset to base temperature
c3.set_attr(p=2.8)

for p in data['p_kond']:
    c2.set_attr(p=p)
    nw.solve('design')
    COP['p_kond'] += [abs(gk.Q.val) / kp.P.val]

# reset to base temperature
c2.set_attr(p=36)

for eta_s in data['eta_s']:
    kp.set_attr(eta_s=eta_s / 100)
    nw.solve('design')
    COP['eta_s'] += [abs(gk.Q.val) / kp.P.val]

fig, ax = plt.subplots(1, 3, sharey=True, figsize=(16, 8))

[a.grid() for a in ax]

i = 0
for key in data:
    ax[i].scatter(data[key], COP[key], s=100, color="#1f567d")
    ax[i].set_xlabel(description[key])
    i += 1

ax[0].set_ylabel('COP of the heat pump')

plt.tight_layout()

fig.savefig('Optimierung R601.svg')
# h_verd und m von c6 oder c8 entfernen dann funktioniert die Simulation
# sinnvolles setzen der Massenströme wichtig
#bei setzen des oderen Druckes auf 38,625 bar statt 36 wird der erwünschte Wirkungsgrad sowie der erwünschte COP erzielt ohne ihn vorzugeben
#wenn eta_s auf 0.7 gesetzt dann Tempertur vor Gaskühler 207 statt 204

