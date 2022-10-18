from tespy.networks import Network
from tespy.components import (Sink, Source, Pump)
from tespy.connections import Connection, Bus

# %% network

fluids = ['water']

nw = Network(fluids=fluids)
nw.set_attr(p_unit='bar', T_unit='C', h_unit='kJ / kg')

# %% components

# pump
pu = Pump('pump')

# water source and sink
so = Source('water source')
si = Sink('water sink')

# %% connections

# source to pump
w_1 = Connection(so, 'out1', pu, 'in1')
w_2 = Connection(pu, 'out1', si, 'in1')
nw.add_conns(w_1, w_2)

# motor of pump has a constant efficiency
power = Bus('total power')
power.add_comps(
    {'comp': pu, 'base': 'bus'})
nw.add_busses(power)

# %% parametrization of components
pu.set_attr(eta_s=0.8)

# %% parametrization of connections
w_1.set_attr(p=1, T=25, fluid={'water': 1})
w_2.set_attr(p=200)

# total output power as input parameter
power.set_attr(P=1e6)

# %% solving

# solve the network, print the results to prompt and save
nw.solve('design')
nw.print_results()
