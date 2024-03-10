import pandas as pd
import numpy as np
from scipy.sparse import save_npz

from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split

from haversine import haversine

from config import config

import time
start = time.time()


"""CONFIG"""

SCALE_TARGET = config['SCALE_TARGET']
SCALE_FUNCTION = config['SCALE_FUNCTION']
TRAIN_SPLIT_PROP = config['TRAIN_SPLIT_PROP']


"""LOAD DATA"""

housing = pd.read_csv('data/raw/NY-House-Dataset.csv')

print(f'Initial shape: {housing.shape}')



"""FEATURE ENGINEERING"""

# Distance
empire_state = (40.748817, -73.985428)
housing['DISTANCE'] = housing.apply(
    lambda x: haversine(empire_state, (x.LATITUDE, x.LONGITUDE)), axis=1
)



"""SET UP PIPELINE"""

# Lists to handle columns for dropping, one-hot encoding, scaling
features_to_drop = [
    'ADDRESS', 'FORMATTED_ADDRESS', 'MAIN_ADDRESS',
    'LONG_NAME', 'LATITUDE', 'LONGITUDE', 'BROKERTITLE'
]

# Categorical features
features_to_onehot = [
    'TYPE', 'STATE', 'ADMINISTRATIVE_AREA_LEVEL_2',
    'STREET_NAME', 'LOCALITY', 'SUBLOCALITY', 
]
onehot_transformer = Pipeline(steps=[
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])

# Numerical features
features_to_scale = [
    x for x in housing.columns
    if x not in features_to_drop 
    and x not in features_to_onehot 
    and x != 'PRICE'
]
scale_transfomer = Pipeline(steps=[
    ('scaler', SCALE_FUNCTION())
])

# Combine in preprocess pipeline
preprocessor = ColumnTransformer(transformers=[
    ('scale', scale_transfomer, features_to_scale),
    ('onehot', onehot_transformer, features_to_onehot)
])



"""TRAIN TEST SPLIT"""

# Separate features and target
X = housing.drop(features_to_drop + ['PRICE'], axis=1)
y = housing.PRICE

# Train, valid, test split
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=1-TRAIN_SPLIT_PROP)
X_valid, X_test, y_valid, y_test = train_test_split(X_valid, y_valid, test_size=0.5)

print(
    f'\n-------- Train, Valid, Test Split --------\n'
    f'--- Features ---\n'
    f'Train: {X_train.shape} - Valid: {X_valid.shape} - Test {X_test.shape}\n'
    f'--- Target ---\n'
    f'Train: {y_train.shape} - Valid: {y_valid.shape} - Test {y_test.shape}\n'
)



"""EXECUTE PIPELINE"""

# Fit in training, apply to valid/test
X_train = preprocessor.fit_transform(X_train)
X_valid = preprocessor.transform(X_valid)
X_test = preprocessor.transform(X_test)

# Scale target, conditionally
if SCALE_TARGET:
    target_scaler = SCALE_FUNCTION()
    y_train = target_scaler.fit_transform(y_train.values.reshape(-1, 1))
    y_valid = target_scaler.transform(y_valid.values.reshape(-1, 1))
    y_test = target_scaler.transform(y_test.values.reshape(-1, 1))



"""SAVE FILES"""

save_npz('data/processed/X_train.npz', X_train)
save_npz('data/processed/X_valid.npz', X_valid)
save_npz('data/processed/X_test.npz', X_test)

np.save('data/processed/y_train.npy', y_train)
np.save('data/processed/y_valid.npy', y_valid)
np.save('data/processed/y_test.npy', y_test)

print(
    f'\n-------- Preprocessing Complete --------\n'
    f'--- Features ---\n'
    f'Train: {X_train.shape} - Valid: {X_valid.shape} - Test {X_test.shape}\n'
    f'--- Target ---\n'
    f'Train: {y_train.shape} - Valid: {y_valid.shape} - Test {y_test.shape}\n'

    f'\n-------- Time elapsed {(time.time() - start)/60:.2f} --------'
)