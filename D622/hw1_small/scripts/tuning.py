import pandas as pd
import numpy as np
from scipy.sparse import load_npz

from sklearn.linear_model import Ridge, RidgeCV, LinearRegression
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, StackingRegressor
from sklearn.model_selection import ParameterGrid
from xgboost import XGBRegressor

from utils import hyperparam_tuner

import time
start = time.time()

from datetime import datetime
log_stamp = datetime.now().strftime("%m.%d_%H.%M")


"""SETUP"""

hyperparams_grid = {
    'ridge': {
        'alpha': [0.001, 0.01, 0.1, 1, 10, 100]
    },
    'rf': {
        'n_estimators': [10, 50, 100, 200],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': [1.0, 'sqrt', 'log2'],
        'random_state': [42]
    },
    'xgb': {
        'n_estimators': [50, 100, 200],
        'max_depth': [3, 6, 10],
        'learning_rate': [0.01, 0.1, 0.2],
        'min_child_weight': [1, 3, 5],
        'gamma': [0.1, 0.5, 1],
        'subsample': [0.6, 0.8, 1.0],
        'colsample_bytree': [0.6, 0.8, 1.0],
        'random_state': [42]
    },
    'ada': {
        'n_estimators': [30, 50, 100],
        'learning_rate': [0.01, 0.1, 1],
        'loss': ['linear', 'square', 'exponential'],
        'random_state': [42]
    } # ,
    # 'stack': {
    #     'final_estimator': [Ridge, RidgeCV, LinearRegression]
    # }
}

hp_combos = {}

for model_name, params_grid in hyperparams_grid.items():
    param_grid = ParameterGrid(params_grid)
    hp_combos[model_name] = param_grid



"""LOAD DATA"""

X_train = load_npz('data/processed/X_train.npz')
X_valid = load_npz('data/processed/X_valid.npz')

y_train = np.load('data/processed/y_train.npy')
y_valid = np.load('data/processed/y_valid.npy')



"""TUNING LOOPS"""

ridge_results = hyperparam_tuner(Ridge, 'ridge', hp_combos, X_train, y_train, X_valid, y_valid)
print(f'Ridge tuning complete - {(time.time()-start)/60:.2f} min')

rf_results = hyperparam_tuner(RandomForestRegressor, 'rf', hp_combos, X_train, y_train, X_valid, y_valid)
print(f'RF tuning complete - {(time.time()-start)/60:.2f} min')

xgb_results = hyperparam_tuner(XGBRegressor, 'xgb', hp_combos, X_train, y_train, X_valid, y_valid)
print(f'XGB tuning complete - {(time.time()-start)/60:.2f} min')

ada_results = hyperparam_tuner(AdaBoostRegressor, 'ada', hp_combos, X_train, y_train, X_valid, y_valid)
print(f'ADA tuning complete - {(time.time()-start)/60:.2f} min')



"""SAVE RESULTS"""

with pd.ExcelWriter(f'logs/tuning_results_{log_stamp}.xlsx', mode='w', engine='openpyxl') as writer:
    ridge_results.to_excel(writer, sheet_name='ridge')
    rf_results.to_excel(writer, sheet_name='rf')
    xgb_results.to_excel(writer, sheet_name='xgb')
    ada_results.to_excel(writer, sheet_name='ada')