# %%[sec_1]
import numpy as np
import pygmo as pg

from tespy.components import (HeatExchanger, Compressor, CycleCloser, Valve, Source, Sink, DropletSeparator, Merge)
from tespy.connections import Bus
from tespy.connections import Connection
from tespy.networks import Network
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis
from tespy.tools.optimization import OptimizationProblem


class HeatPumpCycle:
    """Class template for TESPy model usage in optimization module."""
    def __init__(self):

        wf = 'REFPROP::R1233ZD(E)'
        si = 'H2O'
        fld_wf = {wf: 1, si: 0}
        fld_si = {wf: 0, si: 1}

        self.nw = Network(fluids=[wf, si], T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s', iterinfo=False)

        # Components
        fl = DropletSeparator('Flash Tank')
        cp_1 = Compressor('Compressor 1')
        cp_2 = Compressor('Compressor 2')
        va_1 = Valve('Valve 1')
        va_2 = Valve('Valve 2')
        ev = HeatExchanger('Evaporator')
        sup = HeatExchanger('Superheater')
        gc = HeatExchanger('Gas Cooler')
        ihx_1 = HeatExchanger('Internal Heat Exchanger 1')
        ihx_2 = HeatExchanger('Internal Heat Exchanger 2')

        sou_in = Source('Source in')
        sou_out = Sink('Source out')
        si_in = Source('Sink in')
        si_out = Sink('Sink out')
        mg = Merge('merge', num_in=2)

        cc = CycleCloser('CycleCloser')

        # Connections
        # Main Cycle
        gc_ihx_2 = Connection(gc, 'out1', ihx_2, 'in1', label="1")
        ihx_2_va_2 = Connection(ihx_2, 'out1', va_2, 'in1', label="2")
        va_2_fl = Connection(va_2, 'out1', fl, 'in1', label="3")
        fl_ihx_1 = Connection(fl, 'out1', ihx_1, 'in1', label="4")
        ihx_1_va_1 = Connection(ihx_1, 'out1', va_1, 'in1', label="5")
        va_1_ev = Connection(va_1, 'out1', ev, 'in2', label="6")
        ev_sup = Connection(ev, 'out2', sup, 'in2', label="7")
        sup_ihx_1 = Connection(sup, 'out2', ihx_1, 'in2', label="8")
        ihx_1_cp_1 = Connection(ihx_1, 'out2', cp_1, 'in1', label="9")
        cp_1_mg = Connection(cp_1, 'out1', mg, 'in1', label="10")
        fl_ihx_2 = Connection(fl, 'out2', ihx_2, 'in2', label="11")
        ihx_2_cp_2 = Connection(ihx_2, 'out2', cp_2, 'in1', label="12")
        cp_2_mg = Connection(cp_2, 'out1', mg, 'in2', label="13")
        mg_cc = Connection(mg, 'out1', cc, 'in1', label="14")
        cc_gc = Connection(cc, 'out1', gc, 'in1', label="15")

        # Source
        sou_in_sup = Connection(sou_in, 'out1', sup, 'in1', label="16")
        ev_sup_sou = Connection(sup, 'out1', ev, 'in1', label="17")
        ev_sou_out = Connection(ev, 'out1', sou_out, 'in1', label="18")

        # Sink
        si_in_gc = Connection(si_in, 'out1', gc, 'in2', label="19")
        gc_si_out = Connection(gc, 'out2', si_out, 'in1', label="20")

        self.nw.add_conns(gc_ihx_2, ihx_2_va_2, va_2_fl, fl_ihx_1, ihx_1_va_1, va_1_ev, ev_sup, sup_ihx_1, ihx_1_cp_1,
                          cp_1_mg, fl_ihx_2, ihx_2_cp_2, cp_2_mg, mg_cc, cc_gc, sou_in_sup, ev_sup_sou, ev_sou_out,
                          si_in_gc, gc_si_out)

        # Starting Parameters Components
        ev.set_attr(pr1=1, pr2=1)
        sup.set_attr(pr1=1, pr2=1)
        gc.set_attr(pr1=1, pr2=1)
        ihx_1.set_attr(pr1=1, pr2=1)
        ihx_2.set_attr(pr1=1, pr2=1)
        cp_1.set_attr(eta_s=0.7)
        cp_2.set_attr(eta_s=0.7)

        # Paramters Connections
        # Main Cycle
        h_gc_ihx_2 = CPSI("H", "P", 41 * 1e5, "T", 273.15 + 119, wf) * 1e-3
        gc_ihx_2.set_attr(h=h_gc_ihx_2, p=41)

        # h_va_2_fl = CPSI("H", "P", 7.3 * 1e5, "Q", 0.4, wf) * 1e-3
        va_2_fl.set_attr(p=13.9, fluid={'R1233ZD(E)': 1, 'H2O': 0})

        h_ihx_2_cp_2 = CPSI("H", "P", 13.9 * 1e5, "T", 273.15 + 114, wf) * 1e-3
        ihx_2_cp_2.set_attr(h=h_ihx_2_cp_2)

        h_ev_sup = CPSI("H", "Q", 1, "T", 273.15 + 70, wf) * 1e-3
        ev_sup.set_attr(h=h_ev_sup, p=5.1)

        h_sup_ihx_1 = CPSI("H", "P", 5.1 * 1e5, "T", 273.15 + 75, wf) * 1e-3
        sup_ihx_1.set_attr(h=h_sup_ihx_1)

        h_ihx_1_cp_1 = CPSI("H", "P", 5.1 * 1e5, "T", 273.15 + 108.7, wf) * 1e-3
        ihx_1_cp_1.set_attr(h=h_ihx_1_cp_1)

        # Source
        sou_in_sup.set_attr(T=80, m=5, p=5, fluid={'R1233ZD(E)': 0, 'H2O': 1})
        ev_sou_out.set_attr(T=75)

        # Sink
        si_in_gc.set_attr(T=100, p=20, fluid={'R1233ZD(E)': 0, 'H2O': 1})
        gc_si_out.set_attr(T=200)

        # Solve Model
        self.nw.solve(mode='design')
        self.nw.print_results()

        gc_ihx_2.set_attr(h=None, T=119, p=41)
        va_2_fl.set_attr(p=13.9)
        ihx_2_cp_2.set_attr(h=None)
        ihx_2.set_attr(ttd_u=5)
        ev_sup.set_attr(h=None, x=1, p=5.1)
        sup_ihx_1.set_attr(h=None, Td_bp=5)
        ihx_1_cp_1.set_attr(h=None)
        ihx_1.set_attr(ttd_u=5)
        gc_si_out.set_attr(T=None)
        gc.set_attr(ttd_u=5)

        # busses
        self.power = Bus('power input')
        self.power.add_comps(
            {'comp': cp_1, 'char': 1, 'base': 'bus'},
            {'comp': cp_2, 'char': 1, 'base': 'bus'},
            {'comp': sou_in, 'base': 'bus'},
            {'comp': sou_out})

        self.heat_product = Bus('heating')
        self.heat_product.add_comps(
            {'comp': si_in, 'base': 'bus'},
            {'comp': si_out})

        self.power_COP = Bus('power')
        self.power_COP.add_comps(
            {'comp': cp_1, 'char': -1, 'base': 'bus'},
            {'comp': cp_2, 'char': -1, 'base': 'bus'}
        )

        self.heat_product_COP = Bus('heat_product')
        self.heat_product_COP.add_comps(
            {"comp": gc, "char": 1})

        self.nw.add_busses(self.power, self.heat_product, self.power_COP, self.heat_product_COP)

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
        print(self.ean.network_data.loc['epsilon'])
        print(f'COP = {abs(gc.Q.val) / (cp_1.P.val + cp_2.P.val)}')
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

        gc_ihx_2, va_2_fl, ev_sup, sup_ihx_1 = self.nw.get_conn(
            ["1", "3", "7", "8"]
        )

        # Connection parameters
        gc_ihx_2.set_attr(T=119, p=41)
        va_2_fl.set_attr(p=13.9)
        ev_sup.set_attr(x=1, p=5.1)
        sup_ihx_1.set_attr(Td_bp=5)

        gc, ihx_1, ihx_2, ev, sup, cp_1, cp_2 = self.nw.get_comp(
            [
                "Gas Cooler", "Internal Heat Exchanger 1", "Internal Heat Exchanger 2", "Evaporator", "Superheater",
                "Compressor 1", "Compressor 2"
            ]
        )
        # Component parameters
        gc.set_attr(pr1=1, pr2=1, ttd_u=5)
        ihx_1.set_attr(pr1=1, pr2=1, ttd_u=5)
        ihx_2.set_attr(pr1=1, pr2=1, ttd_u=5)
        ev.set_attr(pr1=1, pr2=1)
        sup.set_attr(pr1=1, pr2=1)
        cp_1.set_attr(eta_s=0.7)
        cp_2.set_attr(eta_s=0.7)

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
        "1": {"p": {"min": 39, "max": 46}, "T": {"min": 119, "max": 125}},
        "7": {"p": {"min": 4, "max": 5.3}}
    }
}
constraints = {
    "lower limits": {
        "Connections": {
            "1": {"p": "ref1"}
        },
    },
    "ref1": ["Connections", "7", "p"]
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