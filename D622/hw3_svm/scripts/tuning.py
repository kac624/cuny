import pandas as pd
import numpy as np

# modeling
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

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
    'svm': {
        'C': [0.1, 1, 10, 100],  
        'kernel': ['linear', 'poly', 'rbf', 'sigmoid'], 
        'gamma': ['scale', 'auto', 0.01, 0.1, 1, 10],  
        'degree': [2, 3, 4],  
        'coef0': [0, 0.5, 1]
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
rf_results = hyperparam_tuner(RandomForestClassifier, 'rf', hp_combos, X_train, y_train, X_valid, y_valid)
# Write results
with pd.ExcelWriter(f'logs/tuning_results_{log_stamp}.xlsx', mode='a', if_sheet_exists='new') as writer:
    rf_results.to_excel(writer, sheet_name='rf')
print(f'Random Forest tuning complete - {(time.time()-start)/60:.2f} min')

# Run tuning
svm_results = hyperparam_tuner(SVC, 'svm', hp_combos, X_train, y_train, X_valid, y_valid)
# Write results
with pd.ExcelWriter(f'logs/tuning_results_{log_stamp}.xlsx', mode='a', if_sheet_exists='new') as writer:
    svm_results.to_excel(writer, sheet_name='xgb')
print(f'XGBoost tuning complete - {(time.time()-start)/60:.2f} min')



"""END"""

print(f'Tuning complete - {(time.time()-start)/60:.2f} min')