# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/00_data.core.ipynb.

# %% auto 0
__all__ = ['new_rearrange', 'load_mats', 'create_splits', 'read_data', 'prepare_train_data']

# %% ../../nbs/00_data.core.ipynb 4
import mat73
import scipy
from fastcore.xtras import Path
from fastcore.basics import *
from einops import rearrange
from functools import partial
import pandas as pd
import numpy as np
from tqdm.notebook import tqdm

# %% ../../nbs/00_data.core.ipynb 5
def load_mats(path, max_len=None):
    mats = []
    length = ifnone(max_len, len(path.ls()))
    for mat in tqdm(sorted(path.ls())[:length]):
        try: 
            print(f"Loading: {mat.name}")
            mats.append(mat73.loadmat(mat))
        except:
            print(f"Loading: {mat.name}")
            mats.append(scipy.io.loadmat(mat))
    return mats

# %% ../../nbs/00_data.core.ipynb 6
new_rearrange = partial(rearrange, pattern='d0 d1 d2 -> (d0 d1) d2')

# %% ../../nbs/00_data.core.ipynb 8
def create_splits(mats, valid_pct=0.2):
    train_ix = int((1-valid_pct)*len(mats))
    read_mats = [read_data(mat) for mat in mats]
    rearranged_mats = [new_rearrange(mat) for mat in read_mats]
    n_train_sample = np.concatenate(rearranged_mats[:train_ix]).shape[0]
    return (np.arange(0, n_train_sample), np.arange(n_train_sample, np.concatenate(rearranged_mats).shape[0]))

# %% ../../nbs/00_data.core.ipynb 10
def read_data(mat):
    return np.stack(mat['data_clean']['trial'], axis=0)

# %% ../../nbs/00_data.core.ipynb 12
def prepare_train_data(mats, ix=None):
    train_ix = ifnone(ix, len(mats))
    return np.concatenate([read_data(mats[i]) for i in range(train_ix)])
