# core
import pandas as pd
import numpy as np
import json
import torch
import time

# sklearn
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

# transformers
import transformers
from transformers import BertTokenizer

# custom
from utils import augment_dataset, random_delete, random_replace, back_translate, get_bert_inputs
from utils import consolidated_categories, performant_classes

# warnings
import warnings
warnings.filterwarnings("ignore", message="TypedStorage is deprecated.*")
warnings.filterwarnings("ignore", message=".*pip install sacremoses.*")
transformers.logging.set_verbosity_error()

start = time.time()



"""CONFIG"""

if torch.cuda.is_available():
    device = torch.device('cuda')
else:
    device = torch.device('cpu')

with open('scripts/config.json', 'r') as file:
    config = json.load(file)

CONSOLIDATE_LABELS = config['CONSOLIDATE_LABELS']
CONSOLIDATE_OTHER = config['CONSOLIDATE_OTHER']
DATA_AUGMENTATION = config['DATA_AUGMENTATION']
TRAIN_SPLIT_PROP = config['TRAIN_SPLIT_PROP']
PRETRAINED_LM = config['PRETRAINED_LM']
MAX_LENGTH = config['MAX_LENGTH']



"""LOAD DATA, CONSOLIDATE AND SPLIT"""

news = pd.read_json('data/raw/News_Category_Dataset_v3.json', orient='records', lines=True)
print(f'Loaded {len(news)} records with {news.category.nunique()} categories')

# Mark performant classes
news['performant'] = news.category.isin(performant_classes)

# Consolidate categories with custom classes
if CONSOLIDATE_LABELS:
    # Invert the dictionary to map each old label to its new, consolidated label
    category_mapping = {
        old_label: new_label for new_label, old_labels in consolidated_categories.items() for old_label in old_labels
    }
    # Apply the mapping to the 'news' DataFrame as before
    news.category = news.category.map(category_mapping)
    # Consolidate non-performant classes under Other
    if CONSOLIDATE_OTHER:
        news.loc[~news.performant, 'category'] = 'OTHER'

    print(f'Consolidated labels to {len(news.category.unique())} classes')

# Collect label names and conversion dict
label_names = news.category.unique()
code_labels_dict = dict(enumerate(news.category.astype('category').cat.categories))

# Integer encode labels and combine two text columns
news['label'] = news.category.astype('category').cat.codes
news['text'] = news.headline + ' ' + news.short_description

# Split
train, valid = train_test_split(news, test_size=1 - TRAIN_SPLIT_PROP, stratify=news.category, random_state=42)
valid, test = train_test_split(valid, test_size=0.5, stratify=valid.category, random_state=42)

print(f'Finished Split - Train: {len(train)}, Test: {len(test)}, Valid: {len(valid)}')



"""DATA AUGMENTATION"""

# Check config for data augmentations
if DATA_AUGMENTATION:
    # Set up variables
    frac = DATA_AUGMENTATION['PERCENTAGE']
    rows_added = 0
    if DATA_AUGMENTATION['BACKTRANSLATION']:
        train, translate_rows_added = augment_dataset(train, back_translate, frac, device=device, MAX_LENGTH=MAX_LENGTH)
        rows_added += translate_rows_added
    if DATA_AUGMENTATION['DELETION']:
        train, translate_rows_added = augment_dataset(train, random_delete, frac)
        rows_added += translate_rows_added
    if DATA_AUGMENTATION['REPLACEMENT']:
        train, translate_rows_added = augment_dataset(train, random_replace, frac)
        rows_added += translate_rows_added
    print(
        f'Augmented {rows_added} samples - Time Elapsed - {(time.time()-start) / 60:.2f} minutes\n'
        f'Split with Augments - Train: {len(train)}, Test: {len(test)}, Valid: {len(valid)}'
    )



"""LABELS"""

y_train = torch.LongTensor(train['label'].values.tolist())
y_valid = torch.LongTensor(valid['label'].values.tolist())
y_test = torch.LongTensor(test['label'].values.tolist())

print(f'Finished Labels - Train: {len(y_train)}, Test: {len(y_test)}, Valid: {len(y_valid)}')



"""TF-IDF"""

tfidf = TfidfVectorizer(min_df=3, stop_words='english', max_features=5000, ngram_range=(1, 3))

tfidf_train = tfidf.fit_transform(train.text)
tfidf_train = torch.from_numpy(tfidf_train.toarray()).to(dtype=torch.float32)

tfidf_valid = tfidf.transform(valid.text)
tfidf_valid = torch.from_numpy(tfidf_valid.toarray()).to(dtype=torch.float32)

tfidf_test = tfidf.transform(test.text)
tfidf_test = torch.from_numpy(tfidf_test.toarray()).to(dtype=torch.float32)

print(f'Finished TF-IDF - Train: {tfidf_train.shape}, Test: {tfidf_test.shape}, Valid: {tfidf_valid.shape}')



"""BERT - TOKENIZE"""

transformers.logging.set_verbosity_error()
tokenizer = BertTokenizer.from_pretrained(PRETRAINED_LM, do_lower_case=True)

train_input_ids, train_att_masks = get_bert_inputs(tokenizer, train['text'].values.tolist(), MAX_LENGTH)
valid_input_ids, valid_att_masks = get_bert_inputs(tokenizer, valid['text'].values.tolist(), MAX_LENGTH)
test_input_ids, test_att_masks = get_bert_inputs(tokenizer, test['text'].values.tolist(), MAX_LENGTH)

print(f'Finished BERT Data - Train: {train_input_ids.shape}, Test: {valid_input_ids.shape}, Valid: {test_input_ids.shape}')



"""SAVE"""

with open('data/processed/code_labels_dict.json', 'w') as f:
    json.dump(code_labels_dict, f)

torch.save(y_train, 'data/processed/y_train.pt')
torch.save(y_valid, 'data/processed/y_valid.pt')
torch.save(y_test, 'data/processed/y_test.pt')

torch.save(tfidf_train, 'data/processed/tfidf_train.pt')
torch.save(tfidf_valid, 'data/processed/tfidf_valid.pt')
torch.save(tfidf_test, 'data/processed/tfidf_test.pt')

torch.save(train_input_ids, 'data/processed/train_input_ids.pt')
torch.save(train_att_masks, 'data/processed/train_att_masks.pt')

torch.save(valid_input_ids, 'data/processed/valid_input_ids.pt')
torch.save(valid_att_masks, 'data/processed/valid_att_masks.pt')

torch.save(test_input_ids, 'data/processed/test_input_ids.pt')
torch.save(test_att_masks, 'data/processed/test_att_masks.pt')


"""END"""

print(f'\nPreprocessing Script Complete - Time Elapsed - {(time.time()-start) / 60:.2f} minutes\n')