import warnings
warnings.filterwarnings('ignore')

import sys, os
from pathlib import Path
repo_path = Path(os.getcwd())

sys.path.append(str(repo_path))
print(repo_path)

import dense.shearlab as shearlab
import dense.batchgen as bg

print("Stop: Loading Shearlab.jl")
from ptpython.repl import embed
embed(globals(), locals())

# Berkeley dataset training
size = 512
path = './BSR/BSDS500/data/'
dataset = 'train'
nClasses = 180
size_patch = 21

rows = size
cols = size
nScales = 4
shearletSystem = shearlab.getshearletsystem2D(rows,cols,nScales);

