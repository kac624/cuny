import pandas as pd
import numpy as np
import time

from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

config = {
    'RANDOM_SEED': 42,
    'TRAIN_SIZE': 0.8,
    'SHUFFLE': True,
    'STRATIFY': True,
    'FEATURES_TO_REMOVE': ['nameOrig', 'nameDest', 'isFlaggedFraud'],
    'FEATURES_TO_SCALE': ['amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest'], # 'step'
    'FEATURES_TO_ENCODE': ['type'],
    'SCALER': StandardScaler,
}

hyperparams = {
    'rf': {
        'n_estimators': 100,
        'criterion': 'entropy',
        'max_depth': None,
        'max_features': 1.0,
        'random_state': config['RANDOM_SEED'],
        'n_jobs': -1
    },
    'svm': {
        # 'C': [0.1, 1, 10, 100],
        # 'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],  
        # 'gamma': ['scale', 'auto', 0.01, 0.1, 1, 10],  # Kernel coefficient for 'rbf', 'poly' and 'sigmoid'.
        # 'degree': [2, 3, 4],  # Only signiifiicant for 'poly'.
        # 'coef0': [0, 0.5, 1],  # Only significant in 'poly' and 'sigmoid'.
        'random_state': config['RANDOM_SEED'],
    }
}

def evaluate(model, X, y, print_results=True):
    # Get predictions
    y_pred = model.predict(X)
    # Get evaluation metrics
    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred, zero_division=0)
    recall = recall_score(y, y_pred, zero_division=0)
    f1 = f1_score(y, y_pred, zero_division=0)
    # Print metrics
    if print_results:
        print(
            f'Accuracy: {accuracy:.2f}\n'
            f'Precision: {precision:.2f}\n'
            f'Recall: {recall:.2f}\n'
            f'F1: {f1:.2f}\n'
        )

    return accuracy, precision, recall, f1


def hyperparam_tuner(model_class, model_name, hp_combos, X_train, y_train, X_valid, y_valid):
    start = time.time()
    counter = 0
    total = len(hp_combos[model_name])
    print(f'\n--Total number of hyperparameter combinations for {model_name}: {total}')
    # Set up df to store results
    results = pd.DataFrame()
    # Loop through hyperparameter combos
    for hp_combo in hp_combos[model_name]:
        # Instantiate model
        model = model_class(**hp_combo)
        # Fit model
        model.fit(X_train, y_train)
        # Get evaluation metrics for training and validation subsets
        train_accuracy, train_precision, train_recall, train_f1 = evaluate(model, X_train, y_train, print_results=False)
        valid_accuracy, valid_precision, valid_recall, valid_f1 = evaluate(model, X_valid, y_valid, print_results=False)
        # Log evaluation results
        result = pd.DataFrame({
            'model': model_name,
            'train_accuracy': train_accuracy,
            'train_precision': train_precision,
            'train_recall': train_recall,
            'train_f1': train_f1,
            'valid_accuracy': valid_accuracy,
            'valid_precision': valid_precision,
            'valid_recall': valid_recall,
            'valid_f1': valid_f1
        }, index=[0])
        # Log hyperparameters
        for key, value in hp_combo.items():
            result[key] = value
        # Add to results df
        results = pd.concat([results, result], ignore_index=True)

        counter += 1
        if counter % np.ceil(total / 10) == 0:
            print(
                f'Completed {counter} of {total} hyperparameter combinations '
                f'Time in Loop: {(time.time() - start) / 60:.2f} min'
            )
    
    return results