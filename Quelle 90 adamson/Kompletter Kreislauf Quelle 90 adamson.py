from tespy.networks import Network
from tespy.components import (HeatExchanger, Source, Sink, CycleCloser, Valve, Compressor)
from tespy.connections import Connection
from CoolProp.CoolProp import PropsSI as CPSI

km = 'R601'
wa = 'H2O'
fld_km = {km: 1, wa: 0}
fld_wa = {km: 0, wa: 1}

nw = Network(fluids=[km, wa], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

# Komponenten

gk = HeatExchanger('Gaskühler')
se_ein = Source('Senke ein')
se_aus = Sink('Senke aus')
vd_in = Source('Verdampfer rein')
ue_aus = Sink ('Überhitzer raus')
vd = HeatExchanger('Verdampfer')
ue = HeatExchanger('Überhitzer')
kp = Compressor('Verdichter')
CC = CycleCloser('Kreislauf')
va = Valve('Drossel')

#Verbindungen Kreislauf

c1 = Connection(CC, 'out1', vd, 'in2')
c2 = Connection(vd, 'out2', ue, 'in2')
c3 = Connection(ue, 'out2', kp, 'in1')
c4 = Connection(kp, 'out1', gk, 'in1')
c5 = Connection(gk, 'out1', va, 'in1')
c6 = Connection(va, 'out1', CC, 'in1')

#Verbindungen Senke und Quelle des Verdampfers und Überhitzers

c7 = Connection(vd_in, 'out1', vd, 'in1')
c8 = Connection(vd, 'out1', ue, 'in1')
c9 = Connection(ue, 'out1', ue_aus, 'in1')

#Verbindungen Senke und Quelle des Gaskühlers

c10 = Connection(se_ein, 'out1', gk, 'in2')
c11 = Connection(gk, 'out2', se_aus, 'in1')

nw.add_conns(c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11)

#Parameter Komponenten

vd.set_attr(pr1=1, pr2=1)
ue.set_attr(pr2=1)
gk.set_attr(pr1=1)
kp.set_attr(eta_s=0.75)

# Parameter Verbindungen Verdampfer und Überhitzer

#Parametrisierung vor dem Verdampfer, Druck im Verdampfer ist auch bekannt sowie wie stark das Fluid überhitzt wird

#bekannter Druck im Verdampfer

h_verd = CPSI("H", "Q", 0, "T", 273.15+70, km) * 1e-3
c1.set_attr(h=h_verd)

# Zwischen Verdampfer und Überhitzer
h_zw = CPSI("H", "Q", 1, "T", 273.15+70, km) * 1e-3
c2.set_attr(h=h_zw, p=2.8)

# Nach dem Überhitzer
h_uebe = CPSI("H", "P", 2.8 * 1e5, "T", 273.15+75, km) * 1e-3
c3.set_attr(h=h_uebe, fluid=fld_km)

#Parameter heiße Seite
c7.set_attr(T=80, m=1, p=1, fluid=fld_wa)
c9.set_attr(T=75)


# Parametrisierung heiße Seite, vor dem Gaskühler
h_gk_vor = CPSI("H", "P", 36 * 1e5, "T", 273.15+204, km) * 1e-3
c4.set_attr(h=h_gk_vor)

# Parametrisierung heiße Seite, nach dem Gaskühler, Druck bleibt konstant im Gaskühler

h_gk_nach = CPSI("H", "P", 36 * 1e5, "T", 273.15+105, km) * 1e-3
c5.set_attr(h=h_gk_nach, p=36)

#Parametrisierung kalte Seite

c10.set_attr(T=100, m=1, fluid=fld_wa)
c11.set_attr(T=200)

nw.solve(mode='design')
nw.print_results()


