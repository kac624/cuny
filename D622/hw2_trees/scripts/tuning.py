import pandas as pd
import numpy as np

# modeling
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

# hyperparameter grid
from sklearn.model_selection import ParameterGrid

# utility
from utils import config, hyperparam_tuner
import time
from datetime import datetime

# warnings
import warnings
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings("ignore", category=ConvergenceWarning)
warnings.filterwarnings("ignore", message=".*l1_ratio.*")
warnings.filterwarnings("ignore", message=".*'n_jobs' > 1.*")
warnings.filterwarnings("ignore", message=".*number of iterations (max_iter).*")

# time stamps
start = time.time()
log_stamp = datetime.now().strftime("%m.%d_%H.%M")


"""CONFIG"""

RANDOM_SEED = config['RANDOM_SEED']

print(f'\n-- Config -- \n')
for k, v in config.items():
    print(f'{k}: {v}')



"""LOAD DATA"""

X_train = np.load('data/processed/X_train.npy')
X_valid = np.load('data/processed/X_valid.npy')

y_train = np.load('data/processed/y_train.npy')
y_valid = np.load('data/processed/y_valid.npy')



"""HYPERPARAMETERS"""

# Dict of hyperparameter space
hyperparams = {
    'dt': {
        'criterion': ['gini', 'entropy'],
        'splitter': ['best', 'random'],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': [1.0, 'sqrt', 'log2'],
        'random_state': [RANDOM_SEED]
    },
    'rf': {
        'n_estimators': [50, 100, 200],
        'criterion': ['gini', 'entropy'],
        'max_depth': [None, 10, 20, 30],
        'max_features': [1.0, 'sqrt', 'log2'],
        'random_state': [RANDOM_SEED],
        'n_jobs': [-1]
    },
    'xgb': {
        'n_estimators': [50, 100, 200],
        'max_depth': [3, 6, 10],
        'learning_rate': [0.01, 0.1, 0.2],
        'subsample': [0.6, 0.8, 1.0],
        'gamma': [0.1, 0.5, 1],
        'random_state': [RANDOM_SEED],
        'n_jobs': [-1]
    }
}

# Set up dict for full grid
hp_combos = {}
# Iterate through hyperparams and add to dict
for model_name, params in hyperparams.items():
    param_grid = ParameterGrid(params)
    hp_combos[model_name] = param_grid



"""TUNING LOOPS"""

# Run tuning
dt_results = hyperparam_tuner(DecisionTreeClassifier, 'dt', hp_combos, X_train, y_train, X_valid, y_valid)
# Write results
with pd.ExcelWriter(f'logs/tuning_results_{log_stamp}.xlsx') as writer:
    dt_results.to_excel(writer, sheet_name='dt')
print(f'Decision Tree tuning complete - {(time.time()-start)/60:.2f} min')

# Run tuning
rf_results = hyperparam_tuner(RandomForestClassifier, 'rf', hp_combos, X_train, y_train, X_valid, y_valid)
# Write results
with pd.ExcelWriter(f'logs/tuning_results_{log_stamp}.xlsx', mode='a', if_sheet_exists='new') as writer:
    rf_results.to_excel(writer, sheet_name='rf')
print(f'Random Forest tuning complete - {(time.time()-start)/60:.2f} min')

# Run tuning
xgb_results = hyperparam_tuner(XGBClassifier, 'xgb', hp_combos, X_train, y_train, X_valid, y_valid)
# Write results
with pd.ExcelWriter(f'logs/tuning_results_{log_stamp}.xlsx', mode='a', if_sheet_exists='new') as writer:
    xgb_results.to_excel(writer, sheet_name='xgb')
print(f'XGBoost tuning complete - {(time.time()-start)/60:.2f} min')



"""END"""

print(f'Tuning complete - {(time.time()-start)/60:.2f} min')