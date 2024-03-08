from itertools import product
from datetime import datetime
import pandas as pd
import subprocess
import json
import os
import time

start = time.time()

# Set params
PREPROCESS = True
PREPROCESS_ONLY_ONCE = False

# Create hyperparameter tuning combinations
hp_space = {
    'CONSOLIDATE_LABELS': True, 
    'CONSOLIDATE_NP_OTHER': True, 
    'DATA_AUGMENTATION': {
        'PERCENTAGE': [0.2],
        'BACKTRANSLATION': [True],
        'DELETION': [True],
        'REPLACEMENT': [True]
    }, # False
    'TRAIN_SPLIT_PROP': [0.7], # 0.5
    'PRETRAINED_LM': ['bert-base-uncased'],
    'LOGGING': [False],
    'MAX_LENGTH': [64], # 128
    'BATCH_SIZE': [32], # 64, 128
    'NUM_EPOCHS': [50],
    'LEARNING_RATE': [2e-5], # 1e-4, 2e-6
    'DROPOUT': [0.3], # 0.1, 0.5
    'BALANCE_FACTOR': [0.1], # 0.3, 0.5, 0.7
    'PATIENCE': [3]
}
hp_combos = list(product(*hp_space.values()))

# Set up variables
results = pd.DataFrame()
log_stamp = datetime.now().strftime("%m.%d_%H.%M")

# Loop through each combination, run scripts, and Append results
for counter, values in enumerate(hp_combos):

    # Write hyperparameters to config
    config = dict(zip(hp_space.keys(), values))
    with open('scripts/config.json', 'w') as f:
        json.dump(config, f, indent=4)
    
    print(
        f'\nRUN NUMBER {counter+1} OF {len(hp_combos)} - TIME ELAPSED - {(time.time()-start) / 60:.2f} minutes\n'
        f'\n\n----CONFIG----'
    )
    for key, value in config.items():
        print(f'{key}: {value}')

    # Run preprocessing
    if PREPROCESS:
        print('\n----PREPROCESS----')
        subprocess.run(['python', 'scripts/large_preprocess.py'])
        if PREPROCESS_ONLY_ONCE:
            PREPROCESS = False
    
    # Run training
    print('\n----TRAINING----')
    subprocess.run(['python', 'scripts/large_train_bert.py'])

    # Append results
    result = pd.read_csv('logs/summary_temp.csv', index_col=0)
    results = pd.concat([results, result], axis=1)

    # Save results and delete temp file
    results.to_csv(f'logs/{log_stamp}_tuning_results.csv')
    os.remove('logs/summary_temp.csv')

print(f'\n\nHYPERPARAMETER TUNING SCRIPT COMPLETE - Time Elapsed - {(time.time()-start) / 60:.2f} minutes\n')

best_params = {
    'TRAIN_SPLIT_PROP': [0.7],
    'PRETRAINED_LM': ['bert-base-uncased'],
    'LOGGING': [True],
    'MAX_LENGTH': [64], 
    'BATCH_SIZE': [32], 
    'NUM_EPOCHS': [50],
    'LEARNING_RATE': [2e-5], 
    'DROPOUT': [0.3],
    'BALANCE_FACTOR': [0.1],
    'PATIENCE': [3]
}