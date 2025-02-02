# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/04_plot.utils.ipynb.

# %% auto 0
__all__ = ['Plot']

# %% ../../nbs/04_plot.utils.ipynb 3
from fastcore.basics import store_attr, patch_to, patch
from fastcore.xtras import globtastic
from fastcore.meta import delegates
from fastcore.foundation import coll_repr
from pathlib import Path
import os 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from ..pickle import label
from ..utils import normalize
import seaborn as sns
import matplotlib.pyplot as plt
import gc

# %% ../../nbs/04_plot.utils.ipynb 4
sns.set_style(style='white')

# %% ../../nbs/04_plot.utils.ipynb 5
import inspect

# %% ../../nbs/04_plot.utils.ipynb 6
class Plot:
    "Plotting module"
    def __init__(self, 
                 path: str, # path to embeddings
                ):
        self.path = Path(path)
        self.norm = {}
        self.book_name = self.path.stem.split('_cleaned')[0].replace('_', ' ').title()
        self.std_ssms = {}
        
    @delegates(globtastic)
    def view_all_files(self, **kwargs):
        return globtastic(self.path, **kwargs)
    
    def create_ssms(self):
        new_path = self.path/'full_plots'
        new_path.mkdir(exist_ok=True)
        
        for method, norm_ssm in self.norm.items():
            title = f'{self.book_name} {method}'
            sns.heatmap(norm_ssm, cmap='hot', 
                        vmin=0, vmax=1, square=True, 
                        xticklabels=False)
            length = norm_ssm.shape[0]
            ticks = np.linspace(1, length, 5, dtype=int)
            plt.yticks(ticks, ticks, rotation = 0)
            plt.ylabel('sentence number')
            plt.savefig(new_path/f'{title}.png', dpi = 300, bbox_inches='tight')
            print(f'Done plotting {title}.png')
            plt.clf()
            del norm_ssm
        
    
    def get_corr_plots(self):
        pass
    
    def get_sectional_ssms(self, 
                           start, # start of the cross section 
                           end, # end of the cross section
                           std, # flag to standardize
                          )->None:
        if std:
            length = self.std_ssms['XLM'].shape[0]
        else:
            length = self.norm['XLM'].shape[0]
        if start == 0 and end == -1:
            end = length
        else: assert start < end, 'Incorrect bounds'
        new_path = self.path/f'sections_{start} {end}'
        new_path.mkdir(exist_ok=True)
        
        if start == 0:
            labels = np.linspace(start + 1, end, 5, dtype=int)
        else:
            labels = np.linspace(start, end, 5, dtype=int)
        
        ticks = np.linspace(0, end - start, 5, dtype=int)
        
        x = self.std_ssms if std else self.norm
        
        plt.figure()
        for method, norm_ssm in x.items():
            if np.min(norm_ssm) < 0:
                vmin = int(np.min(norm_ssm)) - 1
            vmax = int(np.max(norm_ssm)) + 1
            title = f'{self.book_name} {method}'
            sns.heatmap(norm_ssm[start:end, start:end], cmap='hot', 
                        vmin=vmin, vmax=vmax, square=True, 
                        xticklabels=False)
            
            
            
            
            plt.yticks(ticks, labels, rotation = 0)
            plt.ylabel('sentence number')
            plt.savefig(new_path/f'{title}.png', dpi = 300, bbox_inches='tight')
            print(f'Done plotting {title}.png')
            plt.clf()
            del norm_ssm
            _ = gc.collect()
    
    def __repr__(self):
        # remember __str__ calls the __repr_ internally
#         dir_path = os.path.dirname(os.path.realpath(self.path))
        return f'This object contains the path to `{self.path.absolute()}`'

# %% ../../nbs/04_plot.utils.ipynb 7
@patch
def get_normalized(self:Plot):
    "Returns the normalized ssms"
    files = self.view_all_files(file_glob='*.npy')
    
    for f in files:
        f = Path(f)
        fname = f.stem.split('_cleaned_')
        book, method = fname[0], label(fname[1])
        
        title = f'{book.title()} {method}'

        em = np.load(f)

        if fname[1] == 'lexical_wt_ssm':
            sim = em
            print(em.shape)
            n = normalize(sim)
            # modifies the input array inplace
            np.fill_diagonal(n, 1)
        else:
            sim = cosine_similarity(em, em)
            n = normalize(sim)
            
#         yield method, n
        self.norm[method] = n
        del em, sim, n
    return self.norm

# %% ../../nbs/04_plot.utils.ipynb 8
@patch
def get_standardized(self:Plot):
    "Returns the standardized ssms"
    files = self.view_all_files(file_glob='*.npy')
    
    for f in files:
        f = Path(f)
        fname = f.stem.split('_cleaned_')
        book, method = fname[0], label(fname[1])
        
        title = f'{book.title()} {method}'

        em = np.load(f)

        if fname[1] == 'lexical_wt_ssm':
            sim = em
            print(em.shape)
            n = normalize(sim)
            # modifies the input array inplace
            np.fill_diagonal(n, 1)
        else:
            sim = cosine_similarity(em, em)
            n = normalize(sim)
            
        
        numerator = n - np.mean(n)
        denominator = np.sqrt(np.sum(numerator**2) / (numerator.size - 1) )
        
        ab1 = numerator / denominator
        
        self.std_ssms[method] = ab1
        del em, sim, n, numerator, denominator
    return self.std_ssms
