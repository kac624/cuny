import pandas as pd
import numpy as np
from scipy.sparse import load_npz
from joblib import dump

from sklearn.linear_model import LinearRegression, RidgeCV
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, StackingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

import xgboost

from config import config

import time
start = time.time()


"""CONFIG"""

# TODO: Add config options


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
lm = LinearRegression()
lm.fit(X_train, y_train.ravel())
print(f'LM fit complete - {(time.time()-start)/60:.2f} min')

# Random Forest
rf = RandomForestRegressor()
rf.fit(X_train, y_train.ravel())
print(f'RF fit complete - {(time.time()-start)/60:.2f} min')

# XGBoost
xgb = xgboost.XGBRegressor()
xgb.fit(X_train, y_train.ravel())
print(f'XGB fit complete - {(time.time()-start)/60:.2f} min')

# ADA Boost
ada = AdaBoostRegressor()
ada.fit(X_train, y_train.ravel())
print(f'ADA fit complete - {(time.time()-start)/60:.2f} min')

# Stacking
estimators = [
    ('rf', rf), 
    ('xgb', xgb), 
    ('ada', ada)
]
stack = StackingRegressor(
    estimators=estimators, 
    final_estimator=RidgeCV()
)
stack.fit(X_train, y_train.ravel())
print(f'STACK fit complete - {(time.time()-start)/60:.2f} min')



"""EVALUATE"""

print(
    f'\n-------- Model Evaluation --------\n'
    f'--- Linear Regression ---\n'
    f'MSE: {mean_squared_error(y_valid, lm.predict(X_valid))}\n'
    f'MAPE: {mean_absolute_percentage_error(y_valid, lm.predict(X_valid))*100:.2f}%\n'

    f'\n--- Random Forest ---\n'
    f'MSE: {mean_squared_error(y_valid, rf.predict(X_valid))}\n'
    f'MAPE: {mean_absolute_percentage_error(y_valid, rf.predict(X_valid))*100:.2f}%\n'

    f'\n--- XGBoost ---\n'
    f'MSE: {mean_squared_error(y_valid, xgb.predict(X_valid))}\n'
    f'MAPE: {mean_absolute_percentage_error(y_valid, xgb.predict(X_valid))*100:.2f}%\n'

    f'\n--- ADA Boost ---\n'
    f'MSE: {mean_squared_error(y_valid, ada.predict(X_valid))}\n'
    f'MAPE: {mean_absolute_percentage_error(y_valid, ada.predict(X_valid))*100:.2f}%\n'

    f'\n--- Stacking ---\n'
    f'MSE: {mean_squared_error(y_valid, stack.predict(X_valid))}\n'
    f'MAPE: {mean_absolute_percentage_error(y_valid, stack.predict(X_valid))*100:.2f}%\n'

    f'\n-------- Time elapsed {(time.time() - start)/60:.2f} --------'
)


"""SAVE FILES"""

dump(lm, 'models/lm.joblib')
dump(rf, 'models/rf.joblib')
dump(xgb, 'models/xgb.joblib')
dump(ada, 'models/ada.joblib')
dump(stack, 'models/stack.joblib')

