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

        wf1 = 'REFPROP::R1233ZD(E)'
        wf2 = 'REFPROP::Pentane'
        si = 'H2O'

        self.nw = Network(fluids=[wf1, wf2, si], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', iterinfo=False)

        # Components
        ca = HeatExchanger('Cascade HeatExchanger')
        cp1 = Compressor('Compressor1')
        cp2 = Compressor('Compressor2')
        gc1 = HeatExchanger('GasCooler1')
        gc2 = HeatExchanger('GasCooler2')
        va1 = Valve('Valve1')
        va2 = Valve('Valve2')
        ev1 = HeatExchanger('Evaporator1')
        sup1 = HeatExchanger('Superheater1')
        ev2 = HeatExchanger('Evaporator2')
        sup2 = HeatExchanger('Superheater2')

        # Sources, Sinks and CycleCloser

        si_in = Source('Sink in')
        si_out = Sink('Sink out')
        sou_in1 = Source('Source in1')
        sou_out1 = Sink('Source out1')
        sou_in2 = Source('Source in2')
        sou_out2 = Sink('Source out2')

        cc1 = CycleCloser('CycleCloser1')
        cc2 = CycleCloser('CycleCloser2')

        # Connections Cycle Top
        c1 = Connection(gc2, 'out1', ca, 'in1', label="1")
        c2 = Connection(ca, 'out1', va2, 'in1', label="2")
        c3 = Connection(va2, 'out1', ev2, 'in2', label="3")
        c3_sup = Connection(ev2, 'out2', sup2, 'in2', label="3_sup")
        c4 = Connection(sup2, 'out2', cp2, 'in1', label="4")
        c4_cc = Connection(cp2, 'out1', cc1, 'in1', label="4_cc")
        c5 = Connection(cc1, 'out1', gc2, 'in1', label="5")
        # Connections Cycle Bottom
        c6 = Connection(cc2, 'out1', ca, 'in2', label="6")
        c7 = Connection(ca, 'out2', cp1, 'in1', label="7")
        c8 = Connection(cp1, 'out1', gc1, 'in1', label="8")
        c9 = Connection(gc1, 'out1', va1, 'in1', label="9")
        c10 = Connection(va1, 'out1', ev1, 'in2', label="10")
        c10_sup = Connection(ev1, 'out2', sup1, 'in2', label="10_sup")
        c11_cc = Connection(sup1, 'out2', cc2, 'in1', label="11_cc")

        c11 = Connection(si_in, 'out1', gc1, 'in2', label="11")
        c12 = Connection(gc1, 'out2', gc2, 'in2', label="12")
        c13 = Connection(gc2, 'out2', si_out, 'in1', label="13")

        c14 = Connection(sou_in2, 'out1', sup2, 'in1', label="14")
        c15 = Connection(sup2, 'out1', ev2, 'in1', label="15")
        c16 = Connection(ev2, 'out1', sou_out2, 'in1', label="16")
        c17 = Connection(sou_in1, 'out1', sup1, 'in1', label="17")
        c18 = Connection(sup1, 'out1', ev1, 'in1', label="18")
        c19 = Connection(ev1, 'out1', sou_out1, 'in1', label="19")

        self.nw.add_conns(c1, c2, c3, c3_sup, c4, c4_cc, c5, c6, c7, c8, c9, c10, c10_sup, c11_cc, c11, c12, c13, c14,
                          c15, c16, c17, c18, c19)

        # Starting Parameters Components
        ca.set_attr(pr1=1, pr2=1)
        cp1.set_attr(eta_s=0.7)
        cp2.set_attr(eta_s=0.7)
        gc1.set_attr(pr1=1, pr2=1)
        gc2.set_attr(pr1=1, pr2=1)
        ev1.set_attr(pr1=1, pr2=1)
        sup1.set_attr(pr1=1, pr2=1)
        ev2.set_attr(pr1=1, pr2=1)
        sup2.set_attr(pr1=1, pr2=1)

        h_c1 = CPSI("H", "P", 57.5 * 1e5, "T", 273.15 + 140, wf1) * 1e-3
        c1.set_attr(h=h_c1, p=57.5, fluid={'R1233ZD(E)': 1, 'Pentane': 0, 'H2O': 0})

        # h_c2 = CPSI("H", "P", 36 * 1e5, "T", 273.15+127, wf1) * 1e-3
        # c2.set_attr(h=h_c2)

        c3.set_attr(p=5.1)

        h_c3_sup = CPSI("H", "Q", 1, "T", 273.15 + 70, wf1) * 1e-3
        c3_sup.set_attr(h=h_c3_sup)

        h_c4 = CPSI("H", "P", 5.1 * 1e5, "T", 273.15 + 75, wf1) * 1e-3
        c4.set_attr(h=h_c4)

        h_c6 = CPSI("H", "P", 2.8 * 1e5, "T", 273.15 + 75, wf2) * 1e-3
        c6.set_attr(p=2.8, fluid={'R1233ZD(E)': 0, 'Pentane': 1, 'H2O': 0})

        h_c7 = CPSI("H", "P", 2.8 * 1e5, "T", 273.15 + 95, wf2) * 1e-3
        c7.set_attr(h=h_c7)

        c8.set_attr(p=11.652)
        h_c9 = CPSI("H", "P", 11.652 * 1e5, "T", 273.15 + 105, wf2) * 1e-3
        c9.set_attr(h=h_c9)

        h_c10_sup = CPSI("H", "Q", 1, "T", 273.15 + 70, wf2) * 1e-3
        c10_sup.set_attr(h=h_c10_sup)

        h_c11_cc = CPSI("H", "P", 2.8 * 1e5, "T", 273.15 + 75, wf2) * 1e-3
        c11_cc.set_attr(h=h_c11_cc)

        c11.set_attr(T=100, p=20, fluid={'R1233ZD(E)': 0, 'Pentane': 0, 'H2O': 1})
        c12.set_attr(T=135)
        c13.set_attr(T=200)

        c14.set_attr(T=80, m=5, p=5, fluid={'R1233ZD(E)': 0, 'Pentane': 0, 'H2O': 1})
        c16.set_attr(T=75)
        c17.set_attr(T=80, p=5, fluid={'R1233ZD(E)': 0, 'Pentane': 0, 'H2O': 1})
        c19.set_attr(T=75)

        # busses
        self.power = Bus('power input')
        self.power.add_comps(
            {'comp': cp1, 'char': 1, 'base': 'bus'},
            {'comp': cp2, 'char': 1, 'base': 'bus'},
            {'comp': sou_in1, 'base': 'bus'},
            {'comp': sou_in2, 'base': 'bus'},
            {'comp': sou_out1},
            {'comp': sou_out2})

        self.heat_product = Bus('heating')
        self.heat_product.add_comps(
            {'comp': si_in, 'base': 'bus'},
            {'comp': si_out})

        self.power_COP = Bus('power')
        self.power_COP.add_comps(
            {'comp': cp1, 'char': -1, 'base': 'bus'},
            {'comp': cp2, 'char': -1, 'base': 'bus'}
        )

        self.heat_product_COP = Bus('heat_product')
        self.heat_product_COP.add_comps(
            {"comp": gc1, "char": 1},
            {"comp": gc2, "char": 1})

        self.nw.add_busses(self.heat_product_COP, self.power_COP, self.heat_product, self.power)

        # Solve Model
        self.nw.solve(mode='design')
        self.nw.print_results()
        print(f'COP = {abs(self.nw.busses["heat_product"].P.val) / abs(self.nw.busses["power"].P.val)}')

        # New Parameters
        c1.set_attr(h=None, T=140, p=56)
        c3.set_attr(p=5.1)
        c3_sup.set_attr(h=None, x=1)
        c4.set_attr(h=None, Td_bp=5)
        c6.set_attr(p=2.8)
        c7.set_attr(h=None, T=95)
        c8.set_attr(p=11.652)
        c9.set_attr(h=None, T=105)
        c10_sup.set_attr(h=None, x=1)
        c11_cc.set_attr(h=None, Td_bp=5)
        c12.set_attr(T=None)
        gc1.set_attr(ttd_u=10)
        c13.set_attr(T=None)
        gc2.set_attr(ttd_u=5)

        self.nw.solve(mode='design')
        self.nw.print_results()

        self.stable = "_stable"
        self.nw.save(self.stable)
        self.solved = True

        self.pamb = 1
        self.Tamb = 25

        self.ean = ExergyAnalysis(self.nw, E_P=[self.heat_product], E_F=[self.power])
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

        c1, c3, c3_sup, c4, c6, c7, c8, c9, c10_sup, c11_cc, c12, c13 = self.nw.get_conn(
            ["1", "3", "3_sup", "4", "6", "7", "8", "9", "10_sup", "11_cc", "12", "13"]
        )

        # Connection parameters
        c1.set_attr(T=140, p=56)
        c3.set_attr(p=5.1)
        c3_sup.set_attr(x=1)
        c4.set_attr(Td_bp=5)
        c6.set_attr(p=2.8)
        c7.set_attr(T=95)
        c8.set_attr(p=11.652)
        c9.set_attr(T=105)
        c10_sup.set_attr(x=1)
        c11_cc.set_attr(Td_bp=5)


        gc1, gc2, ca, cp1, cp2, ev1, sup1, ev2, sup2 = self.nw.get_comp(
            [
                "GasCooler1", "GasCooler2", "Cascade HeatExchanger", "Compressor1", "Compressor2", "Evaporator1",
                "Superheater1", "Evaporator2", "Superheater2"
            ]
        )
        # Component parameters
        gc1.set_attr(pr1=1, pr2=1, ttd_u=10)
        gc2.set_attr(ttd_u=5)
        ca.set_attr(pr1=1, pr2=1)
        cp1.set_attr(eta_s=0.7)
        cp2.set_attr(eta_s=0.7)
        ev1.set_attr(pr1=1, pr2=1)
        sup1.set_attr(pr1=1, pr2=1)
        ev2.set_attr(pr1=1, pr2=1)
        sup2.set_attr(pr1=1, pr2=1)

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
        "1": {"T": {"min": 135, "max": 141}, "p": {"min": 54, "max": 62}},
        "3": {"p": {"min": 4.9, "max": 5.9}},
        "6": {"p": {"min": 2.7, "max": 3.5}},
        "7": {"T": {"min": 94, "max": 96.2}},
        "8": {"p": {"min": 11, "max": 13}},
        "9": {"T": {"min": 100, "max": 107}}
    },
    "Components": {
        "GasCooler1": {"ttd_u": {"min": 8, "max": 11}},
    }
}
constraints = {
    "lower limits": {
        "Connections": {
            "1": {"p": "ref1"}
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