import pandas as pd
import numpy as np
from scipy.sparse import load_npz
from joblib import dump

from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, StackingRegressor

import xgboost

from utils import config, hyperparams, evaluate

import time
start = time.time()

from datetime import datetime
log_stamp = datetime.now().strftime("%m.%d_%H.%M")


"""CONFIG"""

EVALUATE_TEST = config['EVALUATE_TEST']

RIDGE_PARAMS = hyperparams['ridge']
RF_PARAMS = hyperparams['rf']
XGB_PARAMS = hyperparams['xgb']
ADA_PARAMS = hyperparams['ada']
STACK_PARAMS = hyperparams['stack']



"""LOAD DATA"""

X_train = load_npz('data/processed/X_train.npz')
X_valid = load_npz('data/processed/X_valid.npz')
X_test = load_npz('data/processed/X_test.npz')

y_train = np.load('data/processed/y_train.npy')
y_valid = np.load('data/processed/y_valid.npy')
y_test = np.load('data/processed/y_test.npy')

print(
    f'\n-------- Data Loaded --------\n'
    f'--- Features ---\n'
    f'Train: {X_train.shape} - Valid: {X_valid.shape} - Test {X_test.shape}\n'
    f'--- Target ---\n'
    f'Train: {y_train.shape} - Valid: {y_valid.shape} - Test {y_test.shape}\n'
)



"""TRAIN MODELS"""

# Linear Regression
ridge = Ridge(**RIDGE_PARAMS)
ridge.fit(X_train, y_train.ravel())
print(f'Ridge fit complete - {(time.time()-start)/60:.2f} min')

# Random Forest
rf = RandomForestRegressor(**RF_PARAMS)
rf.fit(X_train, y_train.ravel())
print(f'RF fit complete - {(time.time()-start)/60:.2f} min')

# XGBoost
xgb = xgboost.XGBRegressor(**XGB_PARAMS)
xgb.fit(X_train, y_train.ravel())
print(f'XGB fit complete - {(time.time()-start)/60:.2f} min')

# ADA Boost
ada = AdaBoostRegressor(**ADA_PARAMS)
ada.fit(X_train, y_train.ravel())
print(f'ADA fit complete - {(time.time()-start)/60:.2f} min')

# Stacking
estimators = [
    ('ridge', ridge),
    ('rf', rf), 
    ('xgb', xgb), 
    ('ada', ada)
]
stack = StackingRegressor(
    estimators=estimators, 
    final_estimator=STACK_PARAMS['final_estimator'](),
)
stack.fit(X_train, y_train.ravel())
print(f'STACK fit complete - {(time.time()-start)/60:.2f} min')



"""EVALUATE"""

print(f'\n-------- Model Evaluation --------\n')

ridge_rmse_t, ridge_mape_t, ridge_rmse_v, ridge_mape_v = evaluate(ridge, X_train, y_train, X_valid, y_valid)
rf_rmse_t, rf_mape_t, rf_rmse_v, rf_mape_v = evaluate(rf, X_train, y_train, X_valid, y_valid)
xgb_rmse_t, xgb_mape_t, xgb_rmse_v, xgb_mape_v = evaluate(xgb, X_train, y_train, X_valid, y_valid)
ada_rmse_t, ada_mape_t, ada_rmse_v, ada_mape_v = evaluate(ada, X_train, y_train, X_valid, y_valid)
stack_rmse_t, stack_mape_t, stack_rmse_v, stack_mape_v = evaluate(stack, X_train, y_train, X_valid, y_valid)

summary = pd.DataFrame({
    'model': ['ridge', 'rf', 'xgb', 'ada', 'stack'],
    'train_rmse': [ridge_rmse_t, rf_rmse_t, xgb_rmse_t, ada_rmse_t, stack_rmse_t],
    'train_mape': [ridge_mape_t, rf_mape_t, xgb_mape_t, ada_mape_t, stack_mape_t],
    'valid_rmse': [ridge_rmse_v, rf_rmse_v, xgb_rmse_v, ada_rmse_v, stack_rmse_v],
    'valid_mape': [ridge_mape_v, rf_mape_v, xgb_mape_v, ada_mape_v, stack_mape_v],
})

if EVALUATE_TEST:
    _, _, ridge_rmse_test, ridge_mape_test = evaluate(ridge, X_train, y_train, X_test, y_test)
    _, _, rf_rmse_test, rf_mape_test = evaluate(rf, X_train, y_train, X_test, y_test)  
    _, _, xgb_rmse_test, xgb_mape_test = evaluate(xgb, X_train, y_train, X_test, y_test)
    _, _, ada_rmse_test, ada_mape_test = evaluate(ada, X_train, y_train, X_test, y_test)
    _, _, stack_rmse_test, stack_mape_test = evaluate(stack, X_train, y_train, X_test, y_test)

    summary['test_rmse'] = [ridge_rmse_test, rf_rmse_test, xgb_rmse_test, ada_rmse_test, stack_rmse_test]
    summary['test_mape'] = [ridge_mape_test, rf_mape_test, xgb_mape_test, ada_mape_test, stack_mape_test]



"""SAVE FILES"""

dump(ridge, 'models/ridge.joblib')
dump(rf, 'models/rf.joblib')
dump(xgb, 'models/xgb.joblib')
dump(ada, 'models/ada.joblib')
dump(stack, 'models/stack.joblib')

summary.to_csv(f'logs/training_results_{log_stamp}.csv', index=False)