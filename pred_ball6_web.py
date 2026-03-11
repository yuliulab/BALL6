import os
import sys
import pandas as pd
import json
import re
import numpy as np
from tensorflow import keras
# from collections import Counter
# from tensorflow.keras import models


''' RUN EXAMPLE
micromamba activate ball6_25
cd ~/projects_scmc/ball6/analysis/training_v2/7.packup
python pred_ball6_web.py AL \
  ./input/input_demo_symbol_TALL.txt \
  demo/tall
python pred_ball6_web.py AL \
  ./input/input_demo_symbol_Ph.txt \
  demo/ph
python pred_ball6_web.py B-ALL \
  ./input/input_demo_symbol_Ph.txt \
  demo/ph

version:2.1 250821
'''


''' debug
imodel='B-ALL'
input_file='./input/input_demo_symbol_Ph.txt'
outmark='demo/ph'
'''

imodel=sys.argv[1]
input_file=sys.argv[2]
outmark=sys.argv[3]




# base_dir = '/app/'
# base_dir = './'
base_dir = os.path.dirname(os.path.abspath(__file__)) 
outdir=os.path.split(outmark)[0]
outfn=os.path.split(outmark)[1]

# out_dir = base_dir + '/output/' + outdir + '/'
# model_dir = base_dir + '/model/'
# out_dir = os.path.abspath('./output/' + outdir)
if outdir == '':
    outdir = outfn
out_dir = os.path.abspath('./' + outdir)
# model_dir = os.path.abspath('./model/')
model_dir = os.path.abspath(base_dir + '/modesave/')
if not os.path.isdir(model_dir):
  model_dir = os.path.abspath('./modesave/')
if not os.path.isdir(model_dir):
    sys.exit(f"Error: Cannot find model_dir at {model_dir}")


if os.path.exists(out_dir) == False:
    os.makedirs(out_dir)


def readfpkm(fpkmfile, onlylast=False):
    fpkm = pd.read_table(fpkmfile)
    # fpkm.index = fpkm['GeneName']
    fpkm.index = fpkm.iloc[:,0]
    fpkm = fpkm.drop(fpkm.columns[0], axis=1) # drop first column
    if onlylast:
        fpkm = pd.DataFrame(fpkm.iloc[:, -1]) # only last column
    return fpkm

def readfpkmEnsembl(fpkmfile, onlylast=False):
    fpkm = pd.read_table(fpkmfile)
    # geneid = fpkm['GeneID']
    geneid = fpkm.iloc[:,0]
    geneid = [re.sub(r'\.\d+$','',x) for x in geneid]
    fpkm.index = geneid
    fpkm = fpkm.drop(fpkm.columns[0], axis=1) # drop first column
    if onlylast:
        fpkm = pd.DataFrame(fpkm.iloc[:, -1]) # only last column
    return fpkm

def readexp(fpkmfile, onlylast=False):
    fpkm = pd.read_table(fpkmfile)
    fpkm.index = fpkm.iloc[:,0]
    fpkm = fpkm.drop(fpkm.columns[0], axis=1) # drop first column
    if onlylast:
        fpkm = pd.DataFrame(fpkm.iloc[:, -1]) # only last column
    return fpkm

def check_header(fpkmfile):
    """
    Check whether fpkmfile contains a header.
    Logic: look at the last column of the file.
    If the first line is a number, it means there is no header, returning None.
    If the first line is a string (non-numeric), returning 0 
    """
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    try:
        with open(fpkmfile, 'r') as f:
            first_line = f.readline().strip()
            if not first_line:
                return None # File is empty
            
            first_last_val = first_line.split('\t')[-1]
            
            # If the last column of the first line is a number, then there is no header
            if is_number(first_last_val):
                return None
            else:
                return 0
    except Exception as e:
        return None


def readExpAuto(fpkmfile, onlylast=True):
    header = check_header(fpkmfile)
    fpkm = pd.read_table(fpkmfile, header=header)
    
    # identify ensembl or symbol
    gene_col = fpkm.iloc[:, 0]
    n_check = min(5, len(gene_col))
    all_ensg = True
    
    for i in range(n_check):
        gene = str(gene_col.iloc[i])
        if not gene.startswith('ENSG'):
            all_ensg = False
            break
    
    geneNameType = 'ensembl' if all_ensg else 'symbol'
    if geneNameType == 'ensembl':
        gene_col = [re.sub(r'\.\d+$','',x) for x in gene_col]
    fpkm.index = gene_col
    fpkm = fpkm.drop(fpkm.columns[0], axis=1)

    # rename column to 'sample' if only one column and no header
    if fpkm.shape[1] ==1 and fpkm.columns[0] == 1 and header is None:
        fpkm.columns = ['sample']

    if onlylast:
        fpkm = pd.DataFrame(fpkm.iloc[:, -1])
    
    return fpkm, geneNameType


def fpkm2dx(fpkm):
    genes_sel = []
    genes_notin = []
    for x in gene2idx.keys():
        if x in fpkm.index:
            genes_sel.append(x)
        else:
            genes_notin.append(x)

    fpkm = fpkm.loc[genes_sel, :]

    if (len(genes_notin) > 0):
        print('There are ' + str(len(genes_notin)) + ' gene(s) missed in your input.')
        fpkm_notin = pd.DataFrame(np.zeros((len(genes_notin), fpkm.shape[1])),
                                  index=genes_notin, columns=fpkm.columns)
        # fpkm = fpkm.append(fpkm_notin)
        fpkm = pd.concat([fpkm, fpkm_notin], axis=0)

    dx = []
    # for idx, row in fpkm.iloc[:, :].iteritems():
    for idx, row in fpkm.iloc[:, :].items():
        row = row.sort_values(ascending=False)
        genes = row.index.to_list()
        geneskey = [gene2idx[x] for x in genes]
        dx = np.concatenate([dx, geneskey], axis=0)

    dx = dx.reshape((fpkm.shape[1], fpkm.shape[0]))
    dx = dx.astype(int)
    # print(dx.shape)
    return dx

def prob2type(py):
    ## usage:
    ## pytype = prob2type(py)
    py = pd.DataFrame(py)
    pytype = []
    for idx, row in py.iterrows():
        # k = np.argwhere(row.max() == row)
        k = row.idxmax()
        pytype.append(idx2subtype[str(k)])
    return pytype


def dx2res(dx, model, ids):
    ## 260311 updata: 
    # Multi-sample input compatible
    ## 211206 update:
    # 1.one sample per row -> one sample per column
    # one sample per row 241126
    # 2.wide table to long table
    # 3.PredSubtype move to first row
    # 4.add prob to PredSubtype

    py = model.predict(dx)
    besttype = prob2type(py)
    # if(dx.shape[0] == 1):
    #     if(len(besttype) > 1 ):
    #         besttype = 'mutil-match'
    #     else:
    #         besttype = besttype[0]
    #         bestp = format(py[0, subtype2idx[besttype]], '.4f')
    #         besttype = besttype + ' (' + bestp + ')'

    besttype = [bt + ' (' + format(py[i, subtype2idx[bt]], '.4f') + ')' for i,bt in enumerate(besttype)]

    # py = [format(x, '.4f') for x in py[0]]
    # py = np.array(py).astype('float')
    py = np.around(py, 4)
    pydf = pd.DataFrame(py, index=[ids], columns=idx2subtype.values())
    # pydf.index = [idx2subtype[str(x)] for x in pydf.index]
    # pydf = pd.DataFrame(pd.Series({'PredSubtype': besttype}), columns=[ids]).append(pydf)
    pydf = pd.concat([pd.DataFrame({'PredSubtype': besttype}, index=[ids]), pydf], axis=1)
    pydf = pydf.transpose()

    return pydf


fpkm, geneNameType = readExpAuto(input_file, onlylast=False)


if imodel in ["B-ALL", "BALL"]:
    modelmark = 'mode241224_ballrank_01-48-1.00.keras'
    modelmark = 'mode241224_ballrank_01'
    out_file = out_dir + '/pydf_' + 'ball_' + outfn + '.tab'
elif imodel == "AL":
    modelmark = 'mode250123_alrank_01-20-0.99.keras'
    modelmark = 'mode250123_alrank_01'
    out_file = out_dir + '/pydf_' + 'al_' + outfn + '.tab'
else:
    print('WRONG MODEL TYPE')
    exit()

model_file = model_dir + '/' + modelmark + '.keras'
model = keras.models.load_model(model_file)

## gene sel
if geneNameType == 'ensembl':
    with open(model_dir + '/dict_idx2geneID_'+ modelmark+'.json', 'r') as json_file:
        idx2gene = json.load(json_file)
    with open(model_dir + '/dict_geneID2idx_'+ modelmark+'.json', 'r') as json_file:
        gene2idx = json.load(json_file)
if geneNameType == 'symbol':
    with open(model_dir + '/dict_idx2gene_'+ modelmark+'.json', 'r') as json_file:
        idx2gene = json.load(json_file)
    with open(model_dir + '/dict_gene2idx_'+ modelmark+'.json', 'r') as json_file:
        gene2idx = json.load(json_file)

## subtype
with open(model_dir + '/dict_idx2subtype_'+ modelmark+'.json', 'r') as json_file:
    idx2subtype = json.load(json_file)
with open(model_dir + '/dict_subtype2idx_'+ modelmark+'.json', 'r') as json_file:
    subtype2idx = json.load(json_file)


dx = fpkm2dx(fpkm)
pydf = dx2res(dx, model, fpkm.columns)
# pydf = dx2res(dx, model, 'sample')


if "MEIS1::FOXO1" in pydf.index:
    # row_data = pydf.loc["MEIS1::FOXO1"].copy()
    row_data = pydf.loc[["MEIS1::FOXO1"]].copy()
    row_data.index = ["Bother"]
    pydf = pydf.drop("MEIS1::FOXO1", axis=0)
    pydf = pd.concat([pydf, row_data], axis=0)


# pydf.to_csv(out_file, sep='\t', header=0)
pydf.to_csv(out_file, sep='\t', header=1)

