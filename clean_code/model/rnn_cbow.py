import torch
from torch import nn
import torch.nn.functional as F

class RNNCBOW(torch.nn.Module):
    def __init__(self, vocab_size, img_feat_size):
        super(RNNCBOW, self).__init__()
        self.losses = []
        self.losses_pos = []
        self.top1s, self.top3s, self.top5s = [], [], []
        self.losses_test = []

        self.embeddings = torch.nn.Embedding(vocab_size, img_feat_size, padding_idx=0)
        self.proj = nn.Linear(img_feat_size, img_feat_size)
        self.encoder = nn.RNN(input_size=img_feat_size, hidden_size=img_feat_size)

    def forward(self, input_text):
        input_text = input_text.view(input_text.size(0), -1)
        x = self.embeddings(input_text)
        x = torch.sum(x, 1)
        x = self.proj(F.selu(x))
        return x