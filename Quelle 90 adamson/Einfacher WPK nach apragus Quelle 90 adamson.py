from tespy.networks import Network
from tespy.components import (HeatExchanger, Source, Sink)
from tespy.connections import Connection
from CoolProp.CoolProp import PropsSI as CPSI

#R601
km = 'R601'
wa = 'H2O'
fld_wa = {km: 0, wa: 1}
fld_km = {km: 1, wa: 0}
nw = Network(fluids=[km, wa], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

vd_in = Source('Verdampfer rein')
ue_aus = Sink ('Überhitzer raus')
vd = HeatExchanger('Verdampfer')
ue = HeatExchanger('Überhitzer')
anfang = Source('Umgebung Eintritt')
ende = Sink('Umgebung Austritt')

#Verbindungen heiße Seite

c1 = Connection(vd_in, 'out1', vd, 'in1')
c2 = Connection(vd, 'out1', ue, 'in1')
c3 = Connection(ue, 'out1', ue_aus, 'in1')

#Verbindungen kalte Seite

c4 = Connection(anfang, 'out1', vd, 'in2')
c5 = Connection(vd, 'out2', ue, 'in2')
c6 = Connection(ue, 'out2', ende, 'in1')
nw.add_conns(c1, c2, c3, c4, c5, c6)

#Parameter

#Komponenten

vd.set_attr(pr1=1, pr2=1) #ttd_l=5
ue.set_attr(pr1=1, pr2=1) #ttd_u=5

#Parametrisierung vor dem Verdampfer, Druck im Verdampfer ist auch bekannt sowie wie stark das Fluid überhitzt wird

#bekannter Druck im Verdampfer

h_verd = CPSI("H", "Q", 0, "T", 273.15+70, km) * 1e-3
c4.set_attr(h=h_verd)

# Zwischen Verdampfer und Überhitzer
h_zw = CPSI("H", "Q", 1, "T", 273.15+70, km) * 1e-3
c5.set_attr(h=h_zw, p=2.8)

# Nach dem Überhitzer
h_uebe = CPSI("H", "P", 2.8 * 1e5, "T", 273.15+75, km) * 1e-3
c6.set_attr(h=h_uebe, fluid=fld_km)

#Parameter heiße Seite
c1.set_attr(T=80, m=1, p=1, fluid=fld_wa)
c3.set_attr(T=75)


#Parametrisierung Komponenten



#Parametrisierung heiße Seite





nw.solve(mode='design')
nw.print_results()

#Parametrisierung

#c4.set_attr(p=2.8, x=0, fluid=fld_km)
#c5.set_attr(x=1)

#vd.set_attr(ttd_l=5)
#ue.set_attr(ttd_u=5)
#c4.set_attr(h=None, x=0)
#c5.set_attr(h=None, p=None, x=1)
#c6.set_attr(h=None)

#nw.solve(mode='design')
#nw.print_results()


