from tespy.networks import Network
from tespy.components import (HeatExchanger, Drum, Source, Sink)
from tespy.connections import Connection
from CoolProp.CoolProp import PropsSI as CPSI

# fluid names
wf = 'R1234ZE(Z)'
wh = 'air'
fld_wh = {wf: 0, wh: 1}
fld_wf = {wf: 1, wh: 0}

# network
nw = Network(fluids=[wf, wh], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s')

# components

src_wh = Source('waste-heat-source')
snk_wh = Sink('waste-heat-sink')
src_wf = Source('working-fluid-source')
snk_wf = Sink('working-fluid-sink')
cmp_dr = Drum('drum')
cmp_ev = HeatExchanger('evaporator')
cmp_sh = HeatExchanger('superheater')

# connections

# cold
c11 = Connection(src_wf, 'out1', cmp_dr, 'in1', label='11')
c12 = Connection(cmp_dr, 'out1', cmp_ev, 'in2', label='12')
c13 = Connection(cmp_ev, 'out2', cmp_dr, 'in2', label='13')
c14 = Connection(cmp_dr, 'out2', cmp_sh, 'in2', label='14')
c15 = Connection(cmp_sh, 'out2', snk_wf, 'in1', label='15')

# hot
c21 = Connection(src_wh, 'out1', cmp_sh, 'in1', label='21')
c22 = Connection(cmp_sh, 'out1', cmp_ev, 'in1', label='22')
c23 = Connection(cmp_ev, 'out1', snk_wh, 'in1', label='23')

nw.add_conns(c11, c12, c13, c14, c15, c21, c22, c23)

# parameters

# components
cmp_ev.set_attr(pr1=1)
cmp_sh.set_attr(pr1=1, pr2=1)

# connections

# working fluid saturation state
h_sat = CPSI("H", "Q", 0, "T", 273.15 + 68, wf) / 1e3
c11.set_attr(h=h_sat)

# evaporation pressure drum
p_evap = CPSI("P", "Q", 1, "T", 273.15 + 68, wf) / 1e5
# enthalpy drum
h_drum = CPSI("H", "Q", 0.5, "T", 273.15 + 68, wf) / 1e3
c13.set_attr(h=h_drum, p=p_evap)

# working fluid superheated
h_sh = CPSI("H", "P", p_evap, "T", 273.15 + 75, wf) / 1e3
c15.set_attr(h=h_sh, fluid=fld_wf)

# waste heat water
c21.set_attr(m=1, p=1, T=80, fluid=fld_wh)
c23.set_attr(T=70)

# solve

nw.solve(mode='design')
nw.print_results()
