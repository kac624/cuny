import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from scripts.classes import RnnTextClassifier, RnnDataset

def get_sentence_vector(statement, model):
    words = [word for word in statement if word in model.wv.key_to_index]
    if len(words) >= 1:
        return np.mean(model.wv[words], axis=0)
    else:
        return np.zeros(model.vector_size)

def get_embeddings_bert(statement, tokenizer, model):
    input = tokenizer(
        statement, return_tensors = 'pt', 
        padding = True, truncation = True, max_length = 512
    )
    
    with torch.no_grad():
        output = model(**input)
    embeddings_vector = output.last_hidden_state.mean(dim = 1).squeeze()
    
    return embeddings_vector


def get_embeddings_gpt(statement, tokenizer, model):
    input = tokenizer(
        statement, return_tensors = 'pt', # padding = True, 
        truncation = True, max_length = 512
    )
    
    with torch.no_grad():
        output = model(**input)
    embeddings_vector = output.last_hidden_state.mean(dim = 1).squeeze()
    
    return embeddings_vector


def train_rnn(model, data_loader, criterion, optimizer, n_epochs):
    
    model.train()
    
    for _ in n_epochs:

        for X_batch, y_batch in data_loader:

            y_pred = model(X_batch)
            loss = criterion(y_pred, y_batch)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
    return model

def rnn_bce_logits_predict(model, data, threshold = 0.5):
    model.eval()
    with torch.no_grad():
        logits = model(data)
        probs = torch.sigmoid(logits)
        predictions = probs > threshold
    return predictions

def tune_rnn(hyperparameters, X_train, X_test, y_train, y_test, metric):

    # Initialize the model with the given hyperparameters
    rnn = RnnTextClassifier(
        input_size = X_train.shape[1], output_size = 1, 
        hidden_size = hyperparameters[0], 
        num_layers = hyperparameters[1],
        dropout = hyperparameters[2]
    )
    dataset = RnnDataset(X_train, y_train)
    data_loader = DataLoader(dataset, batch_size = hyperparameters[3], shuffle = True)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = hyperparameters[4](rnn.parameters(), lr = hyperparameters[5])
    n_epochs = range(20)
    
    # Training loop
    trained_rnn = train_rnn(rnn, data_loader, criterion, optimizer, n_epochs)

    # # Evaluate the model
    trained_rnn.eval()
    with torch.no_grad():
        y_pred = rnn_bce_logits_predict(trained_rnn, X_test)
        score = metric(y_test, y_pred)
    return score