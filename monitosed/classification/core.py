# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/01_regression.core.ipynb.

# %% auto 0
__all__ = ['get_users_labels', 'stack_trials', 'prepare_labels', 'CustomLoss']

# %% ../../nbs/01_regression.core.ipynb 3
from ..data.core import *
import numpy as np
import pandas as pd
from fastcore.basics import store_attr
from einops import rearrange, repeat
import torch.nn as nn
import torch.nn.functional as F
import torch

# %% ../../nbs/01_regression.core.ipynb 4
def get_users_labels(path, label_col='R_Pain_Int', drop_ixs=None):
    data = pd.read_excel(path)
    labels = data['R_Pain_Int'].dropna()
    users = data['ID'].dropna()
    users.drop(drop_ixs, inplace=True)
    labels.drop(drop_ixs, inplace=True)
    return users, labels

# %% ../../nbs/01_regression.core.ipynb 6
def stack_trials(mats, signal_len=None):
    data = prepare_train_data(mats)
    if signal_len: data = data[..., :signal_len]
    x = torch.from_numpy(np.concatenate(data, axis=0)).unsqueeze(1)
    return torch.tensor(x, dtype=torch.float32)

# %% ../../nbs/01_regression.core.ipynb 7
def prepare_labels(mats, labels):
    read_mats = [read_data(mat) for mat in mats]
    rearranged_mats = [new_rearrange(mat) for mat in read_mats]
    y = np.concatenate([np.repeat(labels[i], rearranged_mats[i].shape[0]) for i in range(len(mats))])
    return torch.tensor(y, dtype=torch.float32)

# %% ../../nbs/01_regression.core.ipynb 8
class CustomLoss(nn.Module):
    def __init__(self, size_average=None, reduce=None, alpha=0.5, reduction: str = 'mean') -> None:
        super(CustomLoss, self).__init__()
        store_attr()

    def forward(self, input: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        l1 = F.l1_loss(input, target, reduction=self.reduction)
        mse = F.mse_loss(input, target, reduction=self.reduction)
        return self.alpha*l1 + (1-self.alpha)*mse
