import pandas as pd
import json
import time

import torch
from torch.utils.data import TensorDataset, DataLoader

import transformers
from transformers import BertModel, BertTokenizer

from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

from utils import get_bert_inputs, performant_classes

transformers.logging.set_verbosity_error()
start = time.time()


"""CONFIG"""

if torch.cuda.is_available():
    device = torch.device('cuda')
else:
    device = torch.device('cpu')

with open('scripts/config.json', 'r') as file:
    config = json.load(file)

# PRETRAINED_LM = config['PRETRAINED_LM']



"""LOAD DATA"""

news = pd.read_json('data/raw/News_Category_Dataset_v3.json', orient='records', lines=True)
news['text'] = news['headline'] + ' ' + news['short_description']



"""REMOVE PERFORMANT CLASSES"""

news = news[~news.category.isin(performant_classes)]



"""GET EMBEDDINGS"""

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

input_ids, att_masks = get_bert_inputs(tokenizer, news.text.values.tolist())
labels = torch.tensor(news.category.astype('category').cat.codes.values, dtype=torch.long)
dataset = TensorDataset(input_ids, att_masks, labels)
dataloader = DataLoader(dataset, batch_size=32, shuffle=False)

model.to(device)
model.eval()

embeddings = []

with torch.no_grad():
    for batch in dataloader:
        input_ids, att_masks, _ = batch
        input_ids = input_ids.to(device)
        att_masks = att_masks.to(device)

        output = model(input_ids, att_masks)
        batch_embeddings = output.last_hidden_state[:, 0, :]

        embeddings.extend(batch_embeddings.cpu().numpy())

print(f'Embeddings Complete - Time Elapsed - {(time.time()-start) / 60:.2f} minutes')



"""CLUSTERING"""

kmeans = KMeans(n_clusters=10, n_init='auto')
kmeans.fit(embeddings)

print(f'Clustering Complete - Time Elapsed - {(time.time()-start) / 60:.2f} minutes')



"""APPLY TO DF AND SAVE"""

news['cluster'] = kmeans.labels_

news.to_csv('data/processed/news_clustered_classes.csv', index=True)