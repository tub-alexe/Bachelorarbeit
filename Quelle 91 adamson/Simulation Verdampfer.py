from tespy.networks import Network
from tespy.components import (HeatExchanger, Source, Sink,)
from tespy.connections import Connection


vd_in = Source('Verdampfer rein')
vd_aus = Sink ('Überhitzer raus')
vd = HeatExchanger('Verdampfer')

c1 = Connection(vd_in, 'out1', vd_in,)