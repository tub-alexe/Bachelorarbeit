from tespy.networks import Network
from tespy.components import (HeatExchanger, Source, Sink)
from tespy.connections import Connection
from CoolProp.CoolProp import PropsSI as CPSI

km = 'R1234ZE(Z)'
se = 'H2O'
fld_km = {km: 1, se: 0}
fld_se = {km: 0, se: 1}

nw = Network(fluids=[km, se], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', Q_unit='kW')

# Komponenten

unt_ein = Source('Enthitzer rein')
ent_aus = Sink('Unterkühler raus')
ent = HeatExchanger('Enthitzer')
ko = HeatExchanger('Kondensator')
unt = HeatExchanger('Unterkühler')
k_ein = Source('Kreislauf rein')
k_aus = Sink('Kreislauf raus')

#Verbindungen heiße Seite

c1 = Connection(k_ein, 'out1', ent, 'in1')
c2 = Connection(ent, 'out1', ko, 'in1')
c3 = Connection(ko, 'out1', unt, 'in1')
c4 = Connection(unt, 'out1', k_aus, 'in1')

#Verbindungen kalte Seite

c5 = Connection(unt_ein, 'out1', unt, 'in2')
c6 = Connection(unt, 'out2', ko, 'in2')
c7 = Connection(ko, 'out2', ent, 'in2')
c8 = Connection(ent, 'out2', ent_aus, 'in1')
nw.add_conns(c1, c2, c3, c4, c5, c6, c7, c8)



# Parameter Komponenten ent: ttd_l=2, unt: ttd_l=5

ent.set_attr(pr1=1, pr2=1)
ko.set_attr(pr1=1, pr2=1)
unt.set_attr(pr1=1, pr2=1)

# Parameter vor Enthitzer

p_kond = CPSI("P", "Q", 1, "T", 273.15 +, km) / 1e5
h_ent = CPSI("H", "P", p_kond, "T", 273.15 +, km) / 1e3
c1.set_attr(h=h_ent, p=p_kond)

# Parameter zwischen Kondensator und Enthitzer
h_kond = CPSI("H", "Q", 1, "T", 273.15 +, km) / 1e3
c2.set_attr(h=h_kond)

# Parameter zwischen Kondensator und Unterkühler
h_unt = CPSI("H", "Q", 0, "T", 273.15 +, km) / 1e3
c3.set_attr(h=h_unt)

#Parameter nach Unterkühler
h_end= CPSI ("H", "P", p_kond, "T", 273.15 + 75, km) / 1e3
c4.set_attr(h=h_end, fluid=fld_km)


#c1.set_attr(fluid=fld_km)
#c2.set_attr(x=1)
#c3.set_attr(x=0)
c5.set_attr(T=70, m=0.2, p=1, fluid=fld_se)
c8.set_attr(T=160)

#Lösen

nw.solve(mode='design')
nw.print_results()

# nur eine Temperatur auf der heißen Seite indirekt gegeben, Temperaturen die auf der heißen Seite herrschen müssten
# sind für R1234ZE(Z) zu hoch