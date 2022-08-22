# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_pickle.ipynb.

# %% auto 0
__all__ = ['label', 'cos_sim', 'successive_similarities', 'create_dict_whole_book', 'create_label_whole_book', 'create_label',
           'get_embed_method_and_name']

# %% ../nbs/01_pickle.ipynb 2
import os
import numpy as np
import pickle
import string
from numpy import dot
from numpy.linalg import norm
from fastcore.xtras import *
from fastcore.script import *

# %% ../nbs/01_pickle.ipynb 4
def label(
    method:str # name of the method
    ):
    """
    Returns the full name of the model based on the abbreviation
    """
    switcher = {
        'dcltr_base': "DeCLUTR Base",
        'dcltr_sm': "DeCLUTR Small",
        'distil': "DistilBERT",
        'if_FT': "InferSent FastText",
        'if_glove': "InferSent GloVe",
        'roberta': "RoBERTa",
        'use': "USE",
        'new_lex': 'Lexical Vectors',
        'old_lex': 'Lexical Weights',
        'lexical_wt': 'Lexical Weights',
        'lexical_wt_ssm': 'Lexical Weights',
        'lex_vect': 'Lexical Vectors',
        'lex_vect_corr_ts': 'Lexical Vectors (Corr)',
        'mpnet': 'MPNet',
        'minilm': 'MiniLM',
        'xlm': 'XLM'
    }
    return switcher.get(method)

# %% ../nbs/01_pickle.ipynb 5
def cos_sim(
    a: np.ndarray, # vector 1 
    b: np.ndarray, # vector 2
    ):
    """
    Returns the cosine similarity between 2 vectors. 
    """
    return dot(a, b)/(norm(a)*norm(b))

# %% ../nbs/01_pickle.ipynb 6
from pathlib import Path

# %% ../nbs/01_pickle.ipynb 7
def successive_similarities(embeddings, k):
    successive = []
    for i in range(len(embeddings) - k):
        successive.append(cos_sim(embeddings[i], embeddings[i+k]))
    return successive

# %% ../nbs/01_pickle.ipynb 8
@call_parse
def create_dict_whole_book(
    embedding_path:str = '.', # path to the embeddings
    k:int=1, # consecutive index
    ):
    
    p = Path(embedding_path).absolute()
    book_name = p.stem.replace('_', ' ').title()
    
    mdict = {}
    parent_dir = os.path.basename(os.path.dirname(embedding_path))
    sub_dict = {}
    
    files = globtastic(p, recursive=False, file_glob='*.npy').map(Path)
    flen = files.__len__()
    if flen < 1:
        print(f'Found {flen} embeddings')
        print(f'Check `embedding path` and try again')
        return
        
    print(f'Book Name: {book_name}')
    print(f'Found {flen} methods')
    print('-'*45)
    
    for f in files:
        name = f.stem

        if name.endswith('_vect'):
            embed = np.load(f)
            book_name, method = get_embed_method_and_name(name)
            # ts = successive_similarities(embed, k)
            sub_dict[name] = embed


        elif name.endswith('_wt'):
            embed = np.load(f)
            book_name, method = get_embed_method_and_name(name)
            # ts = successive_similarities(embed, k)
            sub_dict[name] = embed

        elif name.endswith('_corr_ts'):
            embed = np.load(f)
            book_name, method = get_embed_method_and_name(name)
            # ts = successive_similarities(embed, k)
            print('Found Lex Corr', name)
            sub_dict[name] = embed
        
        else:
            embed = np.load(f)
            book_name, method = get_embed_method_and_name(name)
            
            ts = successive_similarities(embed, k)
            name = create_label_whole_book(method, parent_dir)
            print(f'Found {name}')
            sub_dict[name] = ts

    mdict[0] = sub_dict
    
    new_path = p/'pkl'
    new_path.mkdir(exist_ok = True)
    pickle.dump(mdict, open(new_path/f'{book_name}_whole.pkl', 'wb'))
    print('-'*45)
    print(f'Saved pkl at {new_path}')

# %% ../nbs/01_pickle.ipynb 9
def create_label_whole_book(method, parent_dir):
    # returns only the method name
    return label(method)

    # Format of Book name + Method
    # return parent_dir.title() + ' ' + label(method)


# %% ../nbs/01_pickle.ipynb 10
def create_label(index, method, parent_dir):
    met = label(method)
    return 'Book ' +str(index + 1) + " " + parent_dir.title() + " " + met


# %% ../nbs/01_pickle.ipynb 11
def get_embed_method_and_name(
    fname, # name of the file
    )->(str, str): # name of file, embeddding method
    """
    Returns the name of the file and the method by 
    splitting on the word '_cleaned_'
    """
    t = fname.split('_cleaned_')
    return  t[0].split()[-1], t[-1]
