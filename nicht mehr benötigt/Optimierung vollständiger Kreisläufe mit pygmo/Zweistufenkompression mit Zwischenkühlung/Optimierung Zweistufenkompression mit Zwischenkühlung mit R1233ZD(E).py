# %%[sec_1]
import numpy as np
import pygmo as pg

from tespy.components import CycleCloser
from tespy.components import Sink
from tespy.components import Source
from tespy.components import HeatExchanger
from tespy.components import Valve
from tespy.components import Compressor
from tespy.connections import Bus
from tespy.connections import Connection
from tespy.networks import Network
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
from tespy.tools.optimization import OptimizationProblem

class HeatPumpCycle:
    """Class template for TESPy model usage in optimization module."""
    def __init__(self):

        wf = 'R1233ZD(E)'
        si = 'H2O'
        fld_wf = {wf: 1, si: 0}
        fld_si = {wf: 0, si: 1}

        self.nw = Network(fluids=[wf, si], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', iterinfo=False)

        # Components

        gc = HeatExchanger('Gas cooler')
        ev = HeatExchanger('Evaporator')
        sup = HeatExchanger('Superheater')
        cool = HeatExchanger('Cooler')
        va = Valve('Valve')
        cp1 = Compressor('Compressor1')
        cp2 = Compressor('Compressor2')
        ihx = HeatExchanger("Internal Heat Exchanger")

        # Sources, Sinks and CycleCloser

        si_in = Source('Sink in')
        si_out = Sink('Sink out')

        sou_in = Source('Source in')
        sou_out = Sink('Source out')
        sou_cool = Source('Source Cooling')
        si_cool = Sink('Sink Cooling')

        cc = CycleCloser('CycleCloser')

        # Connections Cycle
        c1 = Connection(ihx, 'out2', cp1, 'in1', label="1")
        c1_co = Connection(cp1, 'out1', cool, 'in1', label="1_co")
        c2 = Connection(cool, 'out1', cp2, 'in1', label="2")
        c2cc = Connection(cp2, 'out1', cc, 'in1', label="2_cc")
        c3 = Connection(cc, 'out1', gc, 'in1', label="3")
        c4 = Connection(gc, 'out1', ihx, 'in1', label="4")
        c5 = Connection(ihx, 'out1', va, 'in1', label="5")
        c6 = Connection(va, 'out1', ev, 'in2', label="6")
        c6_ue = Connection(ev, 'out2', sup, 'in2', label="6_ue")
        c7 = Connection(sup, 'out2', ihx, 'in2', label="7")

        # Connections Source
        c8 = Connection(si_in, 'out1', gc, 'in2', label="8")
        c9 = Connection(gc, 'out2', si_out, 'in1', label="9")
        c10 = Connection(sou_in, 'out1', sup, 'in1', label="10")
        c11 = Connection(sup, 'out1', ev, 'in1', label="11")
        c12 = Connection(ev, 'out1', sou_out, 'in1', label="12")
        c13 = Connection(sou_cool, 'out1', cool, 'in2', label="13")
        c14 = Connection(cool, 'out2', si_cool, 'in1', label="14")
        self.nw.add_conns(c1, c1_co, c2, c2cc, c3, c4, c5, c6_ue, c6, c7, c8, c9, c10, c11, c12, c13, c14)

        # Starting Parameters Components
        gc.set_attr(pr1=1, pr2=1)
        ihx.set_attr(pr1=1, pr2=1)
        ev.set_attr(pr1=1, pr2=1)
        sup.set_attr(pr1=1, pr2=1)
        cp1.set_attr(eta_s=0.7)
        cp2.set_attr(eta_s=0.7)
        cool.set_attr(pr1=1, pr2=1)

        # Starting Parameters Connections Cycle
        h_ihx_h_nach = CPSI("H", "P", 5.1 * 1e5, "T", 273.15 + 101, wf) * 1e-3
        c1.set_attr(h=h_ihx_h_nach, p=5.1, fluid={'R1233ZD(E)': 1, 'H2O': 0})

        c1_co.set_attr(p=25)
        h_c2 = CPSI("H", "P", 25 * 1e5, "T", 273.15 + 166, wf) * 1e-3
        c2.set_attr(h=h_c2)

        h_ihx_k_vor = CPSI("H", "P", 44 * 1e5, "T", 273.15 + 106, wf) * 1e-3
        c4.set_attr(h=h_ihx_k_vor, p=44)

        h_zw = CPSI("H", "P", 5.1 * 1e5, "Q", 1, wf) * 1e-3
        c6_ue.set_attr(h=h_zw)

        h_ihx_k_nach = CPSI("H", "P", 5.1 * 1e5, "T", 273.15 + 75, wf) * 1e-3
        c7.set_attr(h=h_ihx_k_nach)

        c8.set_attr(T=100, p=20, fluid={'R1233ZD(E)': 0, 'H2O': 1})
        c9.set_attr(T=200)

        # Starting Parameters Connection Source
        c10.set_attr(T=80, m=5, p=5, fluid={'R1233ZD(E)': 0, 'H2O': 1})
        c12.set_attr(T=75)
        c13.set_attr(T=100, m=10, p=10, fluid={'R1233ZD(E)': 0, 'H2O': 1})

        # busses
        power = Bus('power input')
        power.add_comps(
            {'comp': cp1, 'char': 1, 'base': 'bus'},
            {'comp': cp2, 'char': 1, 'base': 'bus'},
            {'comp': sou_in, 'base': 'bus'},
            {'comp': sou_out})

        heat_product = Bus('heating')
        heat_product.add_comps(
            {'comp': si_in, 'base': 'bus'},
            {'comp': si_out})

        power_COP = Bus('power')
        power_COP.add_comps(
            {'comp': cp1, 'char': 1, 'base': 'bus'},
            {'comp': cp2, 'char': 1, 'base': 'bus'}
        )

        cooling = Bus('cooling')
        cooling.add_comps(
            {'comp': sou_cool, 'base': 'bus'},
            {'comp': si_cool})

        heat_product_COP = Bus('heat_product')
        heat_product_COP.add_comps(
            {"comp": gc, "char": 1})

        self.nw.add_busses(power, heat_product, power_COP, heat_product_COP)
        # Solve Model
        self.nw.solve(mode='design')
        self.nw.print_results()

        c1.set_attr(p=5.1, h=None)
        c1_co.set_attr(p=25)
        ihx.set_attr(ttd_u=5)
        c4.set_attr(h=None, p=44, T=106)
        c6_ue.set_attr(h=None, x=1)
        c7.set_attr(h=None, Td_bp=5)
        c9.set_attr(T=None)
        gc.set_attr(ttd_u=7)
        c13.set_attr(T=None)
        cool.set_attr(ttd_l=5)

        self.nw.solve(mode='design')
        self.nw.print_results()
        self.stable = "_stable"
        self.nw.save(self.stable)
        self.solved = True

        self.pamb = 1
        self.Tamb = 25

        self.ean = ExergyAnalysis(self.nw, E_P=[heat_product], E_F=[power], E_L=[cooling])
        self.ean.analyse(pamb=self.pamb, Tamb=self.Tamb)
        self.ean.print_results()
        print(f'COP = {abs(self.nw.busses["heat_product"].P.val) / abs(self.nw.busses["power"].P.val)}')

 # %%[sec_2]

    def get_param(self, obj, label, parameter):
        """Get the value of a parameter in the network"s unit system.

        Parameters
        ----------
        obj : str
            Object to get parameter for (Components/Connections).

        label : str
            Label of the object in the TESPy model.

        parameter : str
            Name of the parameter of the object.

        Returns
        -------
        value : float
            Value of the parameter.
        """
        if obj == "Components":
            return self.nw.get_comp(label).get_attr(parameter).val
        elif obj == "Connections":
            return self.nw.get_conn(label).get_attr(parameter).val

    def set_params(self, **kwargs):

        if "Connections" in kwargs:
            for c, params in kwargs["Connections"].items():
                self.nw.get_conn(c).set_attr(**params)

        if "Components" in kwargs:
            for c, params in kwargs["Components"].items():
                self.nw.get_comp(c).set_attr(**params)

    def reset_boundary_conditions(self):

        c1, c1_co, c4, c6_ue, c7 = self.nw.get_conn(
            ["1", "1_co", "4", "6_ue", "7"]
        )

        # Connection parameters
        c1.set_attr(p=2.8)
        c1_co.set_attr(p=25)
        c4.set_attr(p=44, T=106)
        c6_ue.set_attr(x=1)
        c7.set_attr(Td_bp=5)

        gc, ihx, ev, sup, cp1, cp2, cool = self.nw.get_comp(
            [
                "Gas cooler", "Internal Heat Exchanger", "Evaporator", "Superheater", "Compressor1", "Compressor2", "Cooler"
            ]
        )
        # Component parameters
        gc.set_attr(pr1=1, pr2=1, ttd_u=7)
        ihx.set_attr(pr1=1, pr2=1, ttd_u=5)
        ev.set_attr(pr1=1, pr2=1)
        sup.set_attr(pr1=1, pr2=1)
        cp1.set_attr(eta_s=0.7)
        cp2.set_attr(eta_s=0.7)
        cool.set_attr(pr1=1, pr2=1, ttd_l=5)

    def solve_model(self, **kwargs):
        """
        Solve the TESPy model given the the input parameters
        """
        self.set_params(**kwargs)

        self.solved = False
        try:
            self.nw.solve("design")
            if self.nw.res[-1] >= 1e-3 or self.nw.lin_dep:
                self.reset_boundary_conditions()
                self.nw.solve("design", init_only=True, init_path=self.stable)
            else:
                # might need more checks here!
                if (
                        any(self.nw.results["HeatExchanger"]["Q"] > 0)
                        or any(self.nw.results["HeatExchanger"]["ttd_l"] < 0)
                        or any(self.nw.results["HeatExchanger"]["ttd_u"] < 0)
                        or any(self.nw.results["Compressor"]["eta_s"] > 1)
                        or any(self.nw.results["Compressor"]["P"] < 0)
                    ):
                    self.reset_boundary_conditions()
                    self.nw.solve("design", init_only=True, init_path=self.stable)
                else:
                    self.solved = True
        except ValueError as e:
            print(e)
            self.nw.lin_dep = True
            self.nw.solve("design", init_only=True, init_path=self.stable)

    def get_objective(self, objective=None):
        """
        Get the current objective function evaluation.

        Parameters
        ----------
        objective : str
            Name of the objective function.

        Returns
        -------
        objective_value : float
            Evaluation of the objective function.
        """
        if self.solved:
            if objective == "eta":
                self.ean.analyse(pamb=self.pamb, Tamb=self.Tamb)
                return 1 / (
                    self.ean.network_data.loc['epsilon']
                )
            else:
                msg = f"Objective {objective} not implemented."
                raise NotImplementedError(msg)
        else:
            return np.nan
HeatPump = HeatPumpCycle()
HeatPump.get_objective("eta")
variables = {
    "Connections": {
        "4": {"p": {"min": 42, "max": 50}, "T": {"min": 100, "max": 108}},
        "1": {"p": {"min": 4.5, "max": 5.82}},
    }
}
constraints = {
    "lower limits": {
        "Connections": {
            "4": {"p": "ref1"}
        },
    },
    "ref1": ["Connections", "1", "p"]
}

optimize = OptimizationProblem(
    HeatPump, variables, constraints, objective="eta"
)
# %%[sec_4]
num_ind = 10
num_gen = 100

# for algorithm selection and parametrization please consider the pygmo
# documentation! The number of generations indicated in the algorithm is
# the number of evolutions we undertake within each generation defined in
# num_gen
algo = pg.algorithm(pg.ihs(gen=3, seed=59))
# create starting population
pop = pg.population(pg.problem(optimize), size=num_ind, seed=59)

optimize.run(algo, pop, num_ind, num_gen)
# %%[sec_5]
# To access the results
print(optimize.individuals)
# check pygmo documentation to see, what you can get from the population
pop

#plot the graphic

import matplotlib.pyplot as plt
import matplotlib as mpl

# make text reasonably sized
plt.rcParams["figure.figsize"] = [10.00, 8.50]
fig = plt.figure()
ax = plt.axes(projection='3d')

filter_valid_constraint = optimize.individuals["valid"].values
filter_valid_result = ~np.isnan(optimize.individuals["eta"].values)
data = optimize.individuals.loc[filter_valid_constraint & filter_valid_result]

colors = ["mediumturquoise", "palegreen", "lawngreen", "greenyellow", "yellow", "gold", "orange", "darkorange", "orangered", "firebrick"]
cmap = mpl.colors.ListedColormap(colors)
cmap.set_under("lavender")
cmap.set_over("darkred")
bounds = [0.68, 0.7, 0.72, 0.73, 0.735, 0.74, 0.7425, 0.745, 0.746, 0.747, 0.748]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)


x = data["Connections-4-p"]
y = data["Connections-1-p"]
z = data["Connections-4-T"]
c = 1 / data["eta"]

im = ax.scatter(x, y, z, c=c, cmap=cmap, norm=norm)

cbar = fig.colorbar(im, extend="both")
ax.set_xlabel("Druck Gaskühlerseite")
ax.set_ylabel("Druck Verdampferseite ")
ax.set_zlabel("Temperatur nach dem Gaskühler")
cbar.set_label("eta")
plt.show()
fig.savefig('pygmo_optimization_Zweistufen_R1233ZD(E).svg')
