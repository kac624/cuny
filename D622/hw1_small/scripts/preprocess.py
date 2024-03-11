import pandas as pd
import numpy as np
from scipy.sparse import save_npz

from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split

from haversine import haversine

from utils import config

import time
start = time.time()


"""CONFIG"""

TRAIN_SPLIT_PROP = config['TRAIN_SPLIT_PROP']
FEATURES_TO_DROP = config['FEATURES_TO_DROP']
FEATURES_TO_SCALE = config['FEATURES_TO_SCALE']
FEATURES_TO_ONEHOT = config['FEATURES_TO_ONEHOT']
SCALE_TARGET = config['SCALE_TARGET']
SCALE_FUNCTION = config['SCALE_FUNCTION']



"""LOAD DATA"""

housing = pd.read_csv('data/raw/NY-House-Dataset.csv')

print(f'Initial shape: {housing.shape}')



"""FEATURE ENGINEERING"""

# Distance
empire_state = (40.748817, -73.985428)
housing['DISTANCE'] = housing.apply(
    lambda x: haversine(empire_state, (x.LATITUDE, x.LONGITUDE)), axis=1
)

# Zipcode
housing['ZIPCODE'] = housing.STATE.apply(lambda x: x[-5:])
zip_counts = housing.ZIPCODE.value_counts()
housing.ZIPCODE = housing.ZIPCODE.apply(lambda x: x if x in zip_counts[zip_counts > 30].index else 'Other')



"""SET UP PIPELINE"""

# Categorical features
onehot_transformer = Pipeline(steps=[
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])

scale_transfomer = Pipeline(steps=[
    ('scaler', SCALE_FUNCTION())
])

# Combine in preprocess pipeline
preprocessor = ColumnTransformer(transformers=[
    ('scale', scale_transfomer, FEATURES_TO_SCALE),
    ('onehot', onehot_transformer, FEATURES_TO_ONEHOT),
])



"""TRAIN TEST SPLIT"""

# Separate features and target
X = housing.drop(FEATURES_TO_DROP + ['PRICE'], axis=1)
y = housing.PRICE

# Train, valid, test split
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=1-TRAIN_SPLIT_PROP, random_state=42)
X_valid, X_test, y_valid, y_test = train_test_split(X_valid, y_valid, test_size=0.5, random_state=42)

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