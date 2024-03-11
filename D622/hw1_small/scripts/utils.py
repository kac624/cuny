import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import Ridge, RidgeCV, LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

config = {
    'TRAIN_SPLIT_PROP': 0.6,
    
    'FEATURES_TO_DROP': [
        'ADDRESS', 'FORMATTED_ADDRESS', 'MAIN_ADDRESS',
        'LONG_NAME', 'LATITUDE', 'LONGITUDE', 'BROKERTITLE',
        'ADMINISTRATIVE_AREA_LEVEL_2', 'LOCALITY', 'SUBLOCALITY', 
        'STATE', 'STREET_NAME'],
    
    'FEATURES_TO_ONEHOT': ['TYPE', 'ZIPCODE'],
    
    'FEATURES_TO_SCALE': ['DISTANCE', 'BEDS', 'BATH', 'PROPERTYSQFT'],
    
    'SCALE_TARGET': False,
    
    'SCALE_FUNCTION': MinMaxScaler,

    'EVALUATE_TEST': True
}

hyperparams = {
    'ridge': {
        # 'alpha': 10
    },
    'rf': {
        # 'n_estimators': 10,
        # 'max_depth': 20,
        # 'min_samples_split': 2,
        # 'min_samples_leaf': 1,
        # 'max_features': 1.0,
        'random_state': 42
    },
    'xgb': {
        # 'n_estimators': 100,
        # 'max_depth': 20,
        # 'learning_rate': 0.1,
        # 'min_child_weight': 1,
        # 'gamma': 0.1,
        # 'subsample': 1,
        # 'colsample_bytree': 1,
        'random_state': 42
    },
    'ada': {
        # 'n_estimators': 30,
        # 'learning_rate': 0.01,
        # 'loss': 'exponential',
        'random_state': 42
    },
    'stack': {
        'final_estimator': LinearRegression
    }
}



def evaluate(model, X_train, y_train, X_valid, y_valid, print_results=True):
    rmse_t = mean_squared_error(y_train, model.predict(X_train), squared=False)
    mape_t = mean_absolute_percentage_error(y_train, model.predict(X_train))*100
    rmse_v = mean_squared_error(y_valid, model.predict(X_valid), squared=False)
    mape_v = mean_absolute_percentage_error(y_valid, model.predict(X_valid))*100

    if print_results:
        print(
            f'--- {model.__class__.__name__} ---\n'
            f'Train RMSE: {rmse_t:.2f}\n'
            f'Train MAPE: {mape_t:.2f}%\n'
            f'Valid RMSE: {rmse_v:.2f}\n'
            f'Valid MAPE: {mape_v:.2f}%\n'
        )

    return rmse_t, mape_t, rmse_v, mape_v



def hyperparam_tuner(model_class, model_name, hp_combos, X_train, y_train, X_valid, y_valid):
    results = pd.DataFrame()
    for hp_combo in hp_combos[model_name]:
        model = model_class(**hp_combo)
        model.fit(X_train, y_train.ravel())
        rmse_t, mape_t, rmse_v, mape_v = evaluate(model, X_train, y_train, X_valid, y_valid, print_results=False)
        result = pd.DataFrame({
            'model': model_name,
            'train_rmse': rmse_t,
            'train_mape': mape_t,
            'valid_rmse': rmse_v,
            'valid_mape': mape_v
        }, index=[0])
        for key, value in hp_combo.items():
            result[key] = value
        results = pd.concat([results, result], ignore_index=True)
    
    return results

