import pandas as pd
import numpy as np
from scipy.sparse import save_npz

import os
from zipfile import ZipFile
from kaggle.api.kaggle_api_extended import KaggleApi

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
# from imblearn.over_sampling import SMOTE
# from imblearn.under_sampling import RandomUnderSampler

from utils import config

import time
start = time.time()


"""CONFIG"""

RANDOM_SEED = config['RANDOM_SEED']
TRAIN_SIZE = config['TRAIN_SIZE']
SHUFFLE = config['SHUFFLE']
STRATIFY = config['STRATIFY']
FEATURES_TO_REMOVE = config['FEATURES_TO_REMOVE']
FEATURES_TO_SCALE = config['FEATURES_TO_SCALE']
FEATURES_TO_ENCODE = config['FEATURES_TO_ENCODE']
SCALER = config['SCALER']

print(f'\n-- Config -- \n')
for k, v in config.items():
    print(f'{k}: {v}')



"""LOAD DATA"""

# Download data with Kaggle API
api = KaggleApi()
api.authenticate()
api.dataset_download_file(
    dataset='rupakroy/online-payments-fraud-detection-dataset',
    file_name='PS_20174392719_1491204439457_log.csv'
)

# Unzip
zf = ZipFile('PS_20174392719_1491204439457_log.csv.zip')
zf.extractall()
zf.close()

# Read to dataframe
fraud = pd.read_csv('PS_20174392719_1491204439457_log.csv')

# Remove zip and csv files
os.remove('PS_20174392719_1491204439457_log.csv.zip')
os.remove('PS_20174392719_1491204439457_log.csv')

print(f'Initial shape: {fraud.shape}')



"""FEATURE ENGINEERING"""

# TODO: Add more features



"""SPLIT DATA"""

# Separate Features and Labels
X = fraud.drop(['isFraud', 'isFlaggedFraud'], axis=1)
y = fraud['isFraud']
# Split Training and Validation Subsets
X_train, X_valid, y_train, y_valid = train_test_split(
    X, y, train_size=TRAIN_SIZE, random_state=RANDOM_SEED,
    shuffle=SHUFFLE, stratify=y if STRATIFY else None
)
# Split Validation and Testing Subsets
X_valid, X_test, y_valid, y_test = train_test_split(
    X_valid, y_valid, train_size=0.5, random_state=RANDOM_SEED,
    shuffle=SHUFFLE, stratify=y_valid if STRATIFY else None
)

print(
    f'\n-- Train, Valid, Test Split --\n\n'
    f'Features\n'
    f'Train: {X_train.shape} - Valid: {X_valid.shape} - Test {X_test.shape}\n\n'
    f'Labels\n'
    f'Train: {y_train.shape} - Valid: {y_valid.shape} - Test {y_test.shape}\n\n'
    f'Time Elapsed: {(time.time() - start) / 60:.2f} min\n'
)



"""SCALING / ENCODING"""

# Set up Pipeline - Encoding for Categorical Features
one_hot_transformer = Pipeline(steps=[
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])
# Scaling Pipeline for Numerical Features
scale_transformer = Pipeline(steps=[
    ('scaler', SCALER())
])
# Combine into Preprocessor
preprocessor = ColumnTransformer(transformers=[
    ('onehot', one_hot_transformer, FEATURES_TO_ENCODE),
    ('scale', scale_transformer, FEATURES_TO_SCALE),
])
# Execute Preprocessor
X_train = preprocessor.fit_transform(X_train)
X_valid = preprocessor.transform(X_valid)
X_test = preprocessor.transform(X_test)

print(
    f'\n-- Scaling / Encoding --\n\n'
    f'Train: {X_train.shape} - Valid: {X_valid.shape} - Test {X_test.shape}\n\n'
    f'Time Elapsed: {(time.time() - start) / 60:.2f} min\n'
)

"""OVER/UNDER SAMPLING"""

# TODO: Add oversampling



"""SAVE DATA"""

np.save('data/X_train.npy', X_train)
np.save('data/X_valid.npy', X_valid)
np.save('data/X_test.npy', X_test)

np.save('data/y_train.npy', y_train)
np.save('data/y_valid.npy', y_valid)
np.save('data/y_test.npy', y_test)

print(f'Preprocessing Complete. Time Elapsed: {(time.time() - start) / 60:.2f} min')