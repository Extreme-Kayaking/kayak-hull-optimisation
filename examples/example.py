# Example usage of tool
import pickle
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dataclasses import dataclass
from hullopt.hull.constraints import Constraints
from hullopt.gps.strategies.compare import compare_models
from hullopt.gps.strategies.kernels import HydroPhysicsKernel, StandardMaternKernel, ConfigurablePhysicsKernel
from hullopt.gps.strategies.priors import HydrostaticBaselinePrior, ZeroMeanPrior
from hullopt.gps.aggregator import Aggregator
from hullopt.gps.utils import load_simulation_data
from gui import WeightSelector, ResultVisualizer
from sklearn.model_selection import train_test_split
from hullopt.gps.base_functions import create_gp, update_gp
from hullopt.gps.gp import GaussianProcessSurrogate
from hullopt.optimise import optimise
from hullopt.hull import Hull




# Configuration variables here
DATA_PATH = "gp_data.pkl"
MODEL_PATH = "models/boat_gp.pkl"
KERNEL_CONFIG_HYDRO_PROD = {"length": "rbf",
                 "beam": "rbf",
                 "depth": "rbf",
                 "cross_section_exponent": "matern52",
                 "beam_position": "matern52",
                 "rocker_bow": "matern52",
                 "rocker_sterm": "matern52",
                 "rocker_position": "matern52",
                 "rocker_exponent": "matern52",
                 "heel": "periodic_matern" }

KERNEL_CONFIG_HYDRO_SUM = {"length": "rbf",
                 "beam": "rbf",
                 "depth": "rbf",
                 "cross_section_exponent": "matern52",
                 "beam_position": "matern52",
                 "rocker_bow": "matern52",
                 "rocker_sterm": "matern52",
                 "rocker_position": "matern52",
                 "rocker_exponent": "matern52",
                 "heel": "sum_periodic_matern" }

KERNEL_CONFIG_MATERN = {"length": "rbf",
                 "beam": "rbf",
                 "depth": "rbf",
                 "cross_section_exponent": "matern52",
                 "beam_position": "matern52",
                 "rocker_bow": "matern52",
                 "rocker_sterm": "matern52",
                 "rocker_position": "matern52",
                 "rocker_exponent": "matern52",
                 "heel": "matern52" }

KERNEL_CONFIG_RBF = {"length": "rbf",
                 "beam": "rbf",
                 "depth": "rbf",
                 "cross_section_exponent": "rbf",
                 "beam_position": "rbf",
                 "rocker_bow": "rbf",
                 "rocker_sterm": "rbf",
                 "rocker_position": "rbf",
                 "rocker_exponent": "rbf",
                 "heel": "rbf" }


if not os.path.exists(MODEL_PATH):
    # Initial data gathering for GP
    if not os.path.exists(DATA_PATH):
        print(os.getcwd())
        from hullopt.hull.utils import generate_random_hulls
        from hullopt.config.defaults import dummy_hull
        
        from hullopt.simulations.params import Params
        from hullopt.simulations.analytic import run
        hulls = generate_random_hulls(n=100, cockpit_opening=False, seed=42)
        # Second step: We run a simulation for a given heel angle:
        for idx, hull in enumerate(hulls):
            print("Simulating random hull: " + str(idx))
            for k in range(62):
                result = run(hull, Params(heel=0.1*k))

        
    X_full, y_full, column_order = load_simulation_data(DATA_PATH)

    X_train, X_test, y_train, y_test = train_test_split(
            X_full, y_full, test_size=0.2, random_state=42

        )
    gps = [GaussianProcessSurrogate(ConfigurablePhysicsKernel(KERNEL_CONFIG), ZeroMeanPrior()) for KERNEL_CONFIG in (KERNEL_CONFIG_HYDRO_PROD, KERNEL_CONFIG_HYDRO_SUM, KERNEL_CONFIG_MATERN, KERNEL_CONFIG_RBF)]

    rmse = compare_models({"HYDRO_PROD": gps[0],
                           "HYDRO_SUM": gps[1],
                           "MATERN": gps[2],
                           "RBF": gps[3] },
        X_train,
        y_train,
        X_test,
        y_test,
        column_order,
    )
    gps[0].save(MODEL_PATH)
    print(f"Initial GP RMSE: {rmse}")

else:
    with open(MODEL_PATH, 'rb') as f:
        gp: GaussianProcessSurrogate = pickle.load(f)
    _, _, column_order = load_simulation_data(DATA_PATH)


@dataclass
class GP_Result:
    overall_stability: float
    initial_stability: float
    diminishing_stability: float
    tipping_point: float
    righting_energy: float
    overall_buoyancy: float
    initial_buoyancy: float



user_weights = WeightSelector(column_order, GP_Result).run()




aggregator = Aggregator(user_weights, gp, column_order)
f = aggregator.f



best_params, best_dict, best_score = optimise(f, Constraints())

visualizer = ResultVisualizer(best_params, best_dict, best_score, Hull)
