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

        # network
        wf = 'R600'
        si = 'H2O'
        fld_wf = {wf: 1, si: 0}
        fld_si = {wf: 0, si: 1}
        self.nw = Network(fluids=[wf, si])
        self.nw.set_attr(
            p_unit="bar", T_unit="C", h_unit="kJ / kg", iterinfo=False
        )

        # components

        gc = HeatExchanger('Gas cooler')
        ev = HeatExchanger('Evaporator')
        sup = HeatExchanger('Superheater')
        va = Valve('Valve')
        cp = Compressor('Compressor')

        # Sources, Sinks and CycleCloser

        si_in = Source('Sink in')
        si_out = Sink('Sink out')

        sou_in = Source('Source in')
        sou_out = Sink('Source out')

        cc = CycleCloser('CycleCloser')

        # Connections Cycle

        c1 = Connection(cc, 'out1', gc, 'in1', label="1")
        c2 = Connection(gc, 'out1', va, 'in1', label="2")
        c3 = Connection(va, 'out1', ev, 'in2', label="3")
        c4 = Connection(ev, 'out2', sup, 'in2', label="4")
        c5 = Connection(sup, 'out2', cp, 'in1', label="5")
        c6 = Connection(cp, 'out1', cc, 'in1', label="6")

        # Connections Sink

        c7 = Connection(si_in, 'out1', gc, 'in2', label="7")
        c8 = Connection(gc, 'out2', si_out, 'in1', label="8")

        # Connections Source

        c9 = Connection(sou_in, 'out1', sup, 'in1', label="9")
        c10 = Connection(sup, 'out1', ev, 'in1', label="10")
        c11 = Connection(ev, 'out1', sou_out, 'in1', label="11")
        self.nw.add_conns(c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11)


        # Starting Parameters Components

        gc.set_attr(pr1=1, pr2=1)
        ev.set_attr(pr1=1, pr2=1)
        sup.set_attr(pr1=1, pr2=1)
        cp.set_attr(eta_s=0.7)

        # Starting Parameters Connections Cycle
        #h_gk_vor = CPSI("H", "P", 93 * 1e5, "T", 273.15 + 205, km) * 1e-3
        # c1.set_attr(h=h_gk_vor)

        h_gk_nach = CPSI("H", "P", 93 * 1e5, "T", 273.15 + 105, wf) * 1e-3
        c2.set_attr(h=h_gk_nach, p=93)

        # h_verd = CPSI("H", "Q", 0, "T", 273.15+70, km) * 1e-3
        c3.set_attr(p=8.1)

        h_zw = CPSI("H", "Q", 1, "T", 273.15 + 70.05, wf) * 1e-3
        c4.set_attr(h=h_zw)

        h_uebe = CPSI("H", "P", 8.1 * 1e5, "T", 273.15 + 75, wf) * 1e-3
        c5.set_attr(h=h_uebe, fluid=fld_wf)

        # Starting Parameters Connections Sink

        c7.set_attr(T=100, p=20, fluid=fld_si)
        c8.set_attr(T=200)

        # Starting Parameters Connections Source
        c9.set_attr(T=80, m=5, p=5, fluid=fld_si)
        c11.set_attr(T=75)

        # busses

        self.power = Bus('power input')
        self.power.add_comps(
            {'comp': cp, 'char': 1, 'base': 'bus'},
            {'comp': sou_in, 'base': 'bus'},
            {'comp': sou_out})

        self.heat_product = Bus('heating')
        self.heat_product.add_comps(
            {'comp': si_in, 'base': 'bus'},
            {'comp': si_out})

        self.power_COP = Bus('power')
        self.power_COP.add_comps(
            {'comp': cp, 'char': 1, 'base': 'bus'}
        )

        self.heat_product_COP = Bus('heat_product')
        self.heat_product_COP.add_comps(
            {"comp": gc, "char": 1})

        self.nw.add_busses(self.heat_product_COP, self.power_COP, self.heat_product, self.power)


        #Solve Model

        self.nw.solve(mode='design')
        self.nw.print_results()
        print(f'COP = {abs(gc.Q.val) / cp.P.val}')

        # New Parameters
        # c1.set_attr(h=None, T=204)
        c2.set_attr(h=None, T=105)
        c4.set_attr(h=None, x=1)
        c5.set_attr(h=None, Td_bp=5)
        c8.set_attr(T=None)
        gc.set_attr(ttd_u=5)

        # Solve Model
        self.nw.solve(mode='design')
        self.nw.print_results()
        print(f'COP = {abs(gc.Q.val) / cp.P.val}')

        self.stable = "_stable"
        self.nw.save(self.stable)
        self.solved = True

        # Exergy Analysis
        self.pamb = 1
        self.Tamb = 25

        self.ean = ExergyAnalysis(self.nw, E_P=[self.heat_product], E_F=[self.power])
        self.ean.analyse(pamb=self.pamb, Tamb=self.Tamb)
        self.ean.print_results()

 # %%[sec_2] Optimization

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

        c2, c3, c4, c5 = self.nw.get_conn(
            ["2", "3", "4", "5"]
        )

        # Connection parameters
        c2.set_attr(h=None, T=105, p=93)
        c3.set_attr(p=8.1)
        c4.set_attr(h=None, x=1)
        c5.set_attr(h=None, Td_bp=5)

        gc, ev, sup, cp = self.nw.get_comp(
            [
                "Gas cooler", "Evaporator", "Superheater", "Compressor"
            ]
        )
        # Component parameters
        gc.set_attr(pr1=1, pr2=1, ttd_u=5)
        ev.set_attr(pr1=1, pr2=1)
        sup.set_attr(pr1=1, pr2=1)
        cp.set_attr(eta_s=0.7)

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
        "2": {"p": {"min": 50, "max": 100}, "T": {"min": 100, "max": 110}},
        "3": {"p": {"min": 2, "max": 10}}
    }
}
constraints = {
    "lower limits": {
        "Connections": {
            "2": {"p": "ref1"}
        },
    },
    "ref1": ["Connections", "3", "p"]
}

optimize = OptimizationProblem(
    HeatPump, variables, constraints, objective="eta"
)
# %%[sec_4]
num_ind = 10
num_gen = 200

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
bounds = [0.67, 0.68, 0.69, 0.7, 0.705, 0.71, 0.715, 0.72, 0.725, 0.73, 0.735]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)


x = data["Connections-2-p"]
y = data["Connections-3-p"]
z = data["Connections-2-T"]
c = 1 / data["eta"]

im = ax.scatter(x, y, z, c=c, cmap=cmap, norm=norm)

cbar = fig.colorbar(im, extend="both")
ax.set_xlabel("Druck Gaskühlerseite")
ax.set_ylabel("Druck Verdampferseite ")
ax.set_zlabel("Temperatur nach dem Gaskühler")
cbar.set_label("eta")
plt.show()
fig.savefig('pygmo_optimization_R600.svg')