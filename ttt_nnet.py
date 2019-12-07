import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.utils.data import sampler

import numpy as np

def flatten(x):
    N = x.shape[0] # read in N, C, H, W
    return x.view(N, -1)  # "flatten" the C * H * W values into a single vector per board tensor


class TicTacToeNet(nn.Module):
    def __init__(self, channel_1, channel_2, channel_3, hidden_1, hidden_2):
        super().__init__()
        self.conv1 = nn.Conv2d(3, channel_1, 2, stride=1, padding=0, bias=True)
        self.relu1 = nn.ReLU()
        self.conv2 = nn.Conv2d(channel_1, channel_2, 2, stride=1, padding=0, bias=True)
        self.relu2 = nn.ReLU()
        self.conv3 = nn.Conv2d(channel_2, channel_3, 2, stride=1, padding=0, bias=True)
        self.relu3 = nn.ReLU()
        self.fc = nn.Linear(channel_3 * 3 * 3, hidden_1)
        self.relu4 = nn.ReLU

        # policy head
        self.fc_pi = nn.Linear(hidden_1, 9)
        self.logsoftmax = nn.LogSoftmax(dim=1)

        # value head
        self.fc_v1 = nn.Linear(hidden_1, hidden_2)
        self.relu_v1 = nn.ReLU
        self.fc_v2 = nn.Linear(hidden_2, 1)

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.conv2(x)
        x = self.relu2(x)
        x = self.conv3(x)
        x = self.relu3(x)
        x = self.fc(x)
        x = self.relu4(x)

        pi = self.fc_pi(x)
        pi = self.logsoftmax(pi)

        v = self.fc_v1(x)
        v = self.relu_v1(v)
        v = fc_v2(v)
        v = torch.tanh(v)
        return pi, v




