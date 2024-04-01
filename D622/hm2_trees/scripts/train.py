import pandas as pd 
import numpy as np
import joblib

# modeling
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

# evaluation
from sklearn.metrics import classification_report

# utility
from utils import config, hyperparams, evaluate
import time
from datetime import datetime

# time stamps
start = time.time()
log_stamp = datetime.now().strftime("%m.%d_%H.%M")


"""CONFIG"""

# TODO: Add config

print(f'\n-- Config -- \n')
for k, v in config.items():
    print(f'{k}: {v}')



"""LOAD DATA"""

X_train = np.load('data/processed/X_train.npy')
X_valid = np.load('data/processed/X_valid.npy')

y_train = np.load('data/processed/y_train.npy')
y_valid = np.load('data/processed/y_valid.npy')



"""TRAINING AND EVALUATION"""

dt = DecisionTreeClassifier(**hyperparams['dt'])
rf = RandomForestClassifier(**hyperparams['rf'])
xgb = XGBClassifier(**hyperparams['xgb'])

models = [dt, rf, xgb]
summary = pd.DataFrame()

for model in models:
    print(f'\n-- Fitting {model.__class__.__name__} --\n')
    # Train model
    model.fit(X_train, y_train)
    # Get evaluation metrics
    print('Performance on Training Subset')
    train_accuracy, train_precision, train_recall, train_f1 = evaluate(model, X_train, y_train)
    print('Performance on Validation Subset')
    valid_accuracy, valid_precision, valid_recall, valid_f1 = evaluate(model, X_valid, y_valid)
    # Log results
    result = pd.DataFrame({
        'model': model.__class__.__name__,
        'train_accuracy': train_accuracy,
        'train_precision': train_precision,
        'train_recall': train_recall,
        'train_f1': train_f1,
        'valid_accuracy': valid_accuracy,
        'valid_precision': valid_precision,
        'valid_recall': valid_recall,
        'valid_f1': valid_f1
    }, index=[0])
    summary = pd.concat([summary, result], ignore_index=True)
    print(f'Time Elapsed: {(time.time() - start) / 60:.2f} min\n')



"""SAVE MODEL"""

joblib.dump(dt, 'models/dt.joblib')
joblib.dump(rf, 'models/rf.joblib')
joblib.dump(xgb, 'models/xgb.joblib')

summary.to_csv(f'logs/training_results_{log_stamp}.csv', index=False)

print(f'Training Complete - {(time.time() - start) / 60:.2f} min')