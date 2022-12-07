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

        km = 'R601'
        se = 'H2O'
        fld_km = {km: 1, se: 0}
        fld_se = {km: 0, se: 1}
        self.nw = Network(fluids=[km, se])
        self.nw.set_attr(
            p_unit="bar", T_unit="C", h_unit="kJ / kg", iterinfo=False
        )
        # components
        # main cycle
        gk = HeatExchanger('Gaskühler')
        se_ein = Source('Senke ein')
        se_aus = Sink('Senke aus')

        ue_ein = Source('Verdampfer rein')
        vd_aus = Sink('Überhitzer raus')
        vd = HeatExchanger('Verdampfer')
        ue = HeatExchanger('Überhitzer')

        exp = Valve('Expansionsventil')
        kp = Compressor('Kompressor')
        cc = CycleCloser('Kreilaufzusammenschluss')

        # Verbindungen Kreislauf

        c1 = Connection(cc, 'out1', gk, 'in1', label="1")
        c2 = Connection(gk, 'out1', exp, 'in1', label="2")
        c3 = Connection(exp, 'out1', vd, 'in2', label="3")
        c4 = Connection(vd, 'out2', ue, 'in2', label="4")
        c5 = Connection(ue, 'out2', kp, 'in1', label="5")
        c6 = Connection(kp, 'out1', cc, 'in1', label="6")

        # Verbindungen kalte Seite Gaskühler

        c7 = Connection(se_ein, 'out1', gk, 'in2', label="7")
        c8 = Connection(gk, 'out2', se_aus, 'in1', label="8")

        # Verbindungen heiße Seite Verdampfer und Überhitzer
        c9 = Connection(ue_ein, 'out1', ue, 'in1', label="9")
        c10 = Connection(ue, 'out1', vd, 'in1', label="10")
        c11 = Connection(vd, 'out1', vd_aus, 'in1', label="11")
        self.nw.add_conns(
            c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11
        )

        #busses

        # Parametrisierung Komponenten

        gk.set_attr(pr1=1, pr2=1)
        vd.set_attr(pr1=1, pr2=1)
        ue.set_attr(pr1=1, pr2=1)
        kp.set_attr(eta_s=0.7)
        # Parametrisierung heiße Seite, vor dem Gaskühler

        h_gk_vor = CPSI("H", "P", 36 * 1e5, "T", 273.15 + 204, km) * 1e-3
        # c1.set_attr(h=h_gk_vor)

        # Parametrisierung heiße Seite, nach dem Gaskühler, Druck bleibt konstant im Gaskühler

        h_gk_nach = CPSI("H", "P", 36 * 1e5, "T", 273.15 + 105, km) * 1e-3
        c2.set_attr(h=h_gk_nach, p=36)

        # Parameter kalte Seite
        # Vor dem Verdampfer

        # h_verd = CPSI("H", "Q", 0, "T", 273.15+70, km) * 1e-3
        c3.set_attr(p=2.8)

        # Zwischen Verdampfer und Überhitzer
        h_zw = CPSI("H", "P", 2.8 * 1e5, "T", 273.15 + 70, km) * 1e-3
        c4.set_attr(h=h_zw)

        # Nach dem Überhitzer
        h_uebe = CPSI("H", "P", 2.8 * 1e5, "T", 273.15 + 75, km) * 1e-3
        c5.set_attr(h=h_uebe, fluid=fld_km)

        # Parametrisierung kalte Seite Gaskühler

        c7.set_attr(T=100, p=20, fluid=fld_se)
        c8.set_attr(T=200)

        # Parameter heiße Seite Verdampfer
        c9.set_attr(T=80, m=5, p=5, fluid=fld_se)
        c11.set_attr(T=75)

        # busses

        self.power = Bus('power input')
        self.power.add_comps(
            {'comp': kp, 'char': 1, 'base': 'bus'},
            {'comp': ue_ein, 'base': 'bus'},
            {'comp': vd_aus})

        self.heat_product = Bus('heating')
        self.heat_product.add_comps(
            {'comp': se_ein, 'base': 'bus'},
            {'comp': se_aus})

        self.power_COP = Bus('power')
        self.power_COP.add_comps(
            {'comp': kp, 'char': -1, 'base': 'bus'}
        )

        self.heat_product_COP = Bus('heat_product')
        self.heat_product_COP.add_comps(
            {"comp": gk, "char": 1})

        self.nw.add_busses(self.heat_product_COP, self.power_COP, self.heat_product, self.power)

        # Lösen

        self.nw.solve(mode='design')
        self.nw.print_results()
        print(f'COP = {abs(self.nw.busses["heat_product"].P.val) / abs(self.nw.busses["power"].P.val)}')

        # c1.set_attr(h=None, T=204)
        c2.set_attr(h=None, T=105)
        c4.set_attr(h=None, x=1)
        c5.set_attr(h=None, Td_bp=5)
        c8.set_attr(T=None)
        gk.set_attr(ttd_u=4)

        self.nw.solve(mode='design')
        self.nw.print_results()

        self.stable = "_stable"
        self.nw.save(self.stable)
        self.solved = True

        pamb = 1
        Tamb = 25

        ean = ExergyAnalysis(self.nw, E_P=[self.heat_product], E_F=[self.power])
        ean.analyse(pamb=pamb, Tamb=Tamb)
        ean.print_results()
        print(f'COP = {abs(gk.Q.val) / kp.P.val}')
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

    def solve_model(self, **kwargs):
        """
        Solve the TESPy model given the the input parameters
        """
        self.set_params(**kwargs)

        self.solved = False
        try:
            self.nw.solve("design")
            if self.nw.res[-1] >= 1e-3 or self.nw.lin_dep:
                self.nw.solve("design", init_only=True, init_path=self.stable)
            else:
                # might need more checks here!
                if (
                        any(self.nw.results["HeatExchanger"]["Q"] > 0)
                        or any(self.nw.results["Compressor"]["P"] < 0)
                    ):
                    self.solved = False
                else:
                    self.solved = True
        except ValueError as e:
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
            if objective == "COP":
                return 1 / (
                        self.nw.busses["heat_product"].P.val / self.nw.busses["power"].P.val
                )
            else:
                msg = f"Objective {objective} not implemented."
                raise NotImplementedError(msg)
        else:
            return np.nan

HeatPump = HeatPumpCycle()
HeatPump.get_objective("COP")
variables = {
    "Connections": {
        "2": {"p": {"min": 35.6, "max": 52.8}},
        "3": {"p": {"min": 1.2, "max": 3.1}}
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
    HeatPump, variables, constraints, objective="COP"
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

import matplotlib.pyplot as plt


# make text reasonably sized
plt.rc("font", **{"size": 18})

fig, ax = plt.subplots(1, figsize=(16, 8))

filter_valid_constraint = optimize.individuals["valid"].values
filter_valid_result = ~np.isnan(optimize.individuals["COP"].values)
data = optimize.individuals.loc[filter_valid_constraint & filter_valid_result]

sc = ax.scatter(
    data["Connections-2-p"],
    data["Connections-3-p"],
    c=1 / data["COP"],
    s=100
)
cbar = plt.colorbar(sc)
cbar.set_label("COP")

ax.set_axisbelow(True)
ax.set_xlabel("Druck Gaskühler in bar")
ax.set_ylabel("Druck Verdampfer in bar")
plt.tight_layout()

fig.savefig("pygmo_optimization_R601.svg")
print(data.loc[data["COP"].values == data["COP"].min()])
# %%[sec_6]