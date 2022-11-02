from tespy.networks import Network
from tespy.components import (HeatExchanger, Source, Sink)
from tespy.connections import Connection
from CoolProp.CoolProp import PropsSI as CPSI

km = 'R600'
se = 'H2O'
fld_km = {km: 1, se: 0}
fld_se = {km: 0, se: 1}

nw = Network(fluids=[km, se], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

# Komponenten

gk = HeatExchanger('Gaskühler')
se_ein = Source('Senke ein')
se_aus = Sink('Senke aus')
kr_ein = Source('Kreislauf ein')
kr_aus = Sink('Kreislauf aus')

#Verbindungen heiße Seite

c1 = Connection(kr_ein, 'out1', gk, 'in1')
c2 = Connection(gk, 'out1', kr_aus, 'in1')

#Verbindungen kalte Seite

c3 = Connection(se_ein, 'out1', gk, 'in2')
c4 = Connection(gk, 'out2', se_aus, 'in1')

nw.add_conns(c1, c2, c3, c4)

#Parametrisierung Komponenten

gk.set_attr(pr1=1, pr2=1) #ttd_l = 5 irgendwo im Gaskühler

# Parametrisierung heiße Seite, vor dem Gaskühler
h_gk_vor = CPSI("H", "P", 93*1e5, "T", 273.15+204, km) * 1e-3
c1.set_attr(h=h_gk_vor)


#h_gk_i = h_gk_nach -(i/n)*(h_gk_vor-h_gk_nach), Gaskühler in n=50 Elemente eingeteilt, i muss ich wohl oder übel annehmen, hinzufügen eines zweiten Gaskühlers

# Parametrisierung heiße Seite, nach dem Gaskühler, Druck bleibt konstant im Gaskühler

h_gk_nach = CPSI("H", "P", 93*1e5, "T", 273.15+105, km) * 1e-3
c2.set_attr(h=h_gk_nach, p=93, fluid=fld_km)

#Paramtrisierung Verbindungen heiße Seite

#c1.set_attr(T=204, p=36)
#c2.set_attr(T=105, fluid=fld_km)

#Parametrisierung kalte Seite

c3.set_attr(T=100, m=1, p=2, fluid=fld_se)
c4.set_attr(T=200)

#Lösen

nw.solve(mode='design')
nw.print_results()



