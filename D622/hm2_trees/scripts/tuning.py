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

# time stamps
start = time.time()
log_stamp = datetime.now().strftime("%m.%d_%H.%M")


"""CONFIG"""

RANDOM_SEED = config['RANDOM_SEED']

print(f'\n-- Config -- \n')
for k, v in config.items():
    print(f'{k}: {v}')



"""LOAD DATA"""

X_train = np.load('data/X_train.npy')
X_valid = np.load('data/X_valid.npy')

y_train = np.load('data/y_train.npy')
y_valid = np.load('data/y_valid.npy')



"""HYPERPARAMETERS"""

# Dict of hyperparameter space
hyperparams = {
    'lr': {
        'C': [0.001, 0.01, 0.1, 1, 10, 100],
        'fit_intercept': [True, False],
        'penalty': ['l1', 'l2', 'elasticnet', 'none'],
        'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'],
        'max_iter': [100, 200, 300],
        'multi_class': ['auto', 'ovr', 'multinomial'],
        'random_state': [RANDOM_SEED],
        'n_jobs': [-1]
    },
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
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': [1.0, 'sqrt', 'log2'],
        'random_state': [RANDOM_SEED],
        'n_jobs': [-1]
    },
    'xgb': {
        'n_estimators': [50, 100, 200],
        'max_depth': [3, 6, 10],
        'min_child_weight': [1, 3, 5],
        'colsample_bytree': [0.6, 0.8, 1.0],
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

lr_results = hyperparam_tuner(LogisticRegression, 'lr', hp_combos, X_train, y_train, X_valid, y_valid)
print(f'Logistic Regression tuning complete - {(time.time()-start)/60:.2f} min')

dt_results = hyperparam_tuner(DecisionTreeClassifier, 'dt', hp_combos, X_train, y_train, X_valid, y_valid)
print(f'Decision Tree tuning complete - {(time.time()-start)/60:.2f} min')

rf_results = hyperparam_tuner(RandomForestClassifier, 'rf', hp_combos, X_train, y_train, X_valid, y_valid)
print(f'Random Forest tuning complete - {(time.time()-start)/60:.2f} min')

xgb_results = hyperparam_tuner(XGBClassifier, 'xgb', hp_combos, X_train, y_train, X_valid, y_valid)
print(f'XGBoost tuning complete - {(time.time()-start)/60:.2f} min')



"""SAVE RESULTS"""

with pd.ExcelWriter(f'logs/tuning_results_{log_stamp}.xlsx') as writer:
    lr_results.to_excel(writer, sheet_name='lr')
    dt_results.to_excel(writer, sheet_name='dt')
    rf_results.to_excel(writer, sheet_name='rf')
    xgb_results.to_excel(writer, sheet_name='xgb')

print(f'Tuning complete - {(time.time()-start)/60:.2f} min')