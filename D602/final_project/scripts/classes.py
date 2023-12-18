import torch
import torch
import torch.nn as nn
from torch.utils.data import Dataset

class RnnTextClassifier(nn.Module):
    def __init__(self, input_size, output_size, hidden_size, num_layers, dropout = 0):
        super(RnnTextClassifier, self).__init__()

        # model params
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # layers
        self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first = True, dropout = dropout)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):

        # reshape input
        x = x.unsqueeze(1)

        # initialize hidden state
        hidden = torch.zeros(self.num_layers, x.size(0), self.hidden_size)

        # get RNN output
        out, hidden = self.rnn(x, hidden)
        out = self.dropout(out)
        out = self.fc(out[:, -1, :])
        
        return out

class RnnDataset(Dataset):
    def __init__(self, X_data, y_data):
        self.X_data = X_data
        self.y_data = y_data
        
    def __len__ (self):
        return len(self.X_data)
    
    def __getitem__(self, index):
        return self.X_data[index], self.y_data[index]