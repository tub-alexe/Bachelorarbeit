from tespy.networks import Network
from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink)
from tespy.connections import Connection
from CoolProp.CoolProp import PropsSI as CPSI

km = 'R1234ZE(Z)'
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
anfang = Source('Kreislauf rein')
ende = Sink('Kreislauf raus')

#Verbindungen Kreislauf

c1 = Connection(anfang, 'out1', gk, 'in1')
c2 = Connection(gk, 'out1', exp, 'in1')
c3 = Connection(exp, 'out1', vd, 'in2')
c4 = Connection(vd, 'out2', ue, 'in2')
c5 = Connection(ue, 'out2', ende, 'in1')

#Verbindungen kalte Seite Gaskühler

c7 = Connection(se_ein, 'out1', gk, 'in2')
c8 = Connection(gk, 'out2', se_aus, 'in1')


#Verbindungen heiße Seite Verdampfer und Überhitzer
c9 = Connection(ue_in, 'out1', ue, 'in1')
c10 = Connection(ue, 'out1', vd, 'in1')
c11 = Connection(vd, 'out1', vd_aus, 'in1')
nw.add_conns(c1, c2, c3, c4, c5, c7, c8, c9, c10, c11)

#Parametrisierung Komponenten

gk.set_attr(pr1=1, pr2=1)
vd.set_attr(pr1=1, pr2=1)
ue.set_attr(pr1=1, pr2=1)
# Parametrisierung heiße Seite, vor dem Gaskühler

h_gk_vor = CPSI("H", "P", 56 * 1e5, "T", 273.15+208, km) * 1e-3
c1.set_attr(h=h_gk_vor)

# Parametrisierung heiße Seite, nach dem Gaskühler, Druck bleibt konstant im Gaskühler

h_gk_nach = CPSI("H", "P", 56 * 1e5, "T", 273.15+105, km) * 1e-3
c2.set_attr(h=h_gk_nach, p=56)

# Parameter kalte Seite
# Vor dem Verdampfer

#h_verd = CPSI("H", "Q", 0, "T", 273.15+70, km) * 1e-3
c3.set_attr(p=6.7)

# Zwischen Verdampfer und Überhitzer
h_zw = CPSI("H", "Q", 1, "T", 273.15+70, km) * 1e-3
c4.set_attr(h=h_zw)

# Nach dem Überhitzer
h_uebe = CPSI("H", "P", 6.7 * 1e5, "T", 273.15+75, km) * 1e-3
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

#c1.set_attr(h=None, T=208)
c2.set_attr(h=None, T=105)
c4.set_attr(h=None, T=70)
c5.set_attr(h=None, T=75)

nw.solve(mode='design')
nw.print_results()
# Temperaturen in Gaskühler werden automatisch nach oben korrigiert
# erste Enthalpie kann nicht ohne Fehler ersetzt werden