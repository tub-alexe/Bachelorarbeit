from tespy.networks import Network
from tespy.components import (HeatExchanger, Valve, Source, Sink)
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
anfang = Source('Umgebung Eintritt')
ende = Sink('Umgebung Austritt')

#Verbindungen Kreislauf

c1 = Connection(anfang, 'out1', gk, 'in1')
c2 = Connection(gk, 'out1', exp, 'in1')
c3 = Connection(exp, 'out1', vd, 'in2')
c4 = Connection(vd, 'out2', ue, 'in2')
c5 = Connection(ue, 'out2', ende, 'in1')

#Verbindungen kalte Seite Gaskühler

c6 = Connection(se_ein, 'out1', gk, 'in2')
c7 = Connection(gk, 'out2', se_aus, 'in1')


#Verbindungen heiße Seite Verdampfer und Überhitzer
c8 = Connection(ue_in, 'out1', ue, 'in1')
c9 = Connection(ue, 'out1', vd, 'in1')
c10 = Connection(vd, 'out1', vd_aus, 'in1')
nw.add_conns(c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

#Parametrisierung Komponenten

gk.set_attr(pr1=1, pr2=1)
vd.set_attr(pr1=1, pr2=1)
ue.set_attr(pr1=1, pr2=1)

# Parametrisierung heiße Seite, vor dem Gaskühler

h_gk_vor = CPSI("H", "P", 36 * 1e5, "T", 273.15+204, km) * 1e-3
c1.set_attr(h=h_gk_vor)

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

c6.set_attr(T=100, p=20, fluid=fld_se)
c7.set_attr(T=200)

#Parameter heiße Seite Verdampfer
c8.set_attr(T=80, m=5, p=5, fluid=fld_se)
c10.set_attr(T=75)

#Lösen

nw.solve(mode='design')
nw.print_results()

c1.set_attr(h=None, T=204)
c2.set_attr(h=None, p=None, T=105)
c3.set_attr(p=None, x=0)
c4.set_attr(h=None, T=70, x=1)
c5.set_attr(h=None, T=75)


nw.solve(mode='design')
nw.print_results()

# h_verd und m von c6 oder c8 entfernen dann funktioniert die Simulation
# sinnvolles setzen der Massenströme wichtig