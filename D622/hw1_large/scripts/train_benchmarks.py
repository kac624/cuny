# core
import json
import torch
import time
import joblib

# modeling
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

# evaluation
from sklearn.metrics import accuracy_score, f1_score

# timing
start = time.time()


"""CONFIG"""

print('--Config--')
if torch.cuda.is_available():
    device = torch.device('cuda')
    print(f'device: {torch.cuda.get_device_name(0)}')
else:
    device = torch.device('cpu')
    print('device: CPU')

with open('scripts/config.json', 'r') as file:
    config = json.load(file)

for key, value in config.items():
    print(f'{key}: {value}')


"""LOAD DATA"""

tfidf_train = torch.load('data/processed/tfidf_train.pt').numpy()
tfidf_valid = torch.load('data/processed/tfidf_valid.pt').numpy()
tfidf_test = torch.load('data/processed/tfidf_test.pt').numpy()
y_train = torch.load('data/processed/y_train.pt').numpy()
y_valid = torch.load('data/processed/y_valid.pt').numpy()
y_test = torch.load('data/processed/y_test.pt').numpy()


"""LOGISTIC REGRESSION"""

lr_model = LogisticRegression(multi_class='multinomial', max_iter=1000)
lr_model.fit(tfidf_train, y_train)

y_pred_train = lr_model.predict(tfidf_train)
y_pred_valid = lr_model.predict(tfidf_valid)
y_pred_test = lr_model.predict(tfidf_test)

print(
    f'--Logistic Regression Results--'

    f'\nTrain Accuracy: {100 * accuracy_score(y_train, y_pred_train):.2f}%'
    f'\nTrain F-1 Score: {100 * f1_score(y_train, y_pred_train, average="weighted"):.2f}%'

    f'\nValidation Accuracy: {100 * accuracy_score(y_valid, y_pred_valid):.2f}%'
    f'\nValidation F-1 Score: {100 * f1_score(y_valid, y_pred_valid, average="weighted"):.2f}%'

    f'\nTest Accuracy: {100 * accuracy_score(y_test, y_pred_test):.2f}%'
    f'\nTest F-1 Score: {100 * f1_score(y_test, y_pred_test, average="weighted"):.2f}%'

    f'\nTime Elapsed: {(time.time() - start)/60:.2f} minutes'
)


"""XGBOOST"""

xgb_model = XGBClassifier()
xgb_model.fit(tfidf_train, y_train)

y_pred_train = xgb_model.predict(tfidf_train)
y_pred_valid = xgb_model.predict(tfidf_valid)
y_pred_test = xgb_model.predict(tfidf_test)

print(
    f'--XGBoost Results--'
    f'\nTrain Accuracy: {100 * accuracy_score(y_train, y_pred_train):.2f}%'
    f'\nTrain F-1 Score: {100 * f1_score(y_train, y_pred_train, average="weighted"):.2f}%'

    f'\nValidation Accuracy: {100 * accuracy_score(y_valid, y_pred_valid):.2f}%'
    f'\nValidation F-1 Score: {100 * f1_score(y_valid, y_pred_valid, average="weighted"):.2f}%'

    f'\nTest Accuracy: {100 * accuracy_score(y_test, y_pred_test):.2f}%'
    f'\nTest F-1 Score: {100 * f1_score(y_test, y_pred_test, average="weighted"):.2f}%'

    f'\nTime Elapsed: {(time.time() - start)/60:.2f} minutes'
)


"""SAVE MODEL"""

joblib.dump(lr_model, 'models/lr_model.pkl')
xgb_model.save_model('models/xgb_model.json')


"""END"""

print(f'Total Time: {(time.time() - start)/60:.2f} minutes')