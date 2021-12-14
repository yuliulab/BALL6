# -*- coding: utf-8 -*-
# @Time : 21/11/10 9:15
# @Author : Bowen Cui
# @Email : xcxiongmao@126.com
# @File : pred_ball.py
# @Project : predRNN

import os
import stat
import sys
import pandas as pd
import json
import glob
import re
import numpy as np
from collections import Counter
from tensorflow.keras import models

# ids='sample1_fpkm.txt'
# outdir="./"
ids=str(sys.argv[1])
outprefix=str(sys.argv[2])

scriptdir=os.path.abspath(__file__)
scriptdir=os.path.split(scriptdir)[0]

outdir=os.path.split(outprefix)[0]
outmark=os.path.split(outprefix)[1]
if outdir == '':
    outdir = './'
outdir=os.path.abspath(outdir)
os.makedirs(outdir, exist_ok=True)
if outmark == '':
    outmark = os.path.split(ids)[1]
    outmark = os.path.splitext(outmark)[0]
    # outmark = 'res'
# print("input file: " + ids)
# print("output dir: " + outdir + '/')

modelmark = 'mode210917_ballrank_01'




## LOAD DATASET
## gene sel
with open(scriptdir + '/modesave/dict_idx2gene_'+ modelmark+'.json', 'r') as json_file:
    idx2gene = json.load(json_file)

with open(scriptdir + '/modesave/dict_gene2idx_'+ modelmark+'.json', 'r') as json_file:
    gene2idx = json.load(json_file)

with open(scriptdir + '/modesave/dict_idx2subtype_'+ modelmark+'.json', 'r') as json_file:
    idx2subtype = json.load(json_file)

with open(scriptdir + '/modesave/dict_subtype2idx_'+ modelmark+'.json', 'r') as json_file:
    subtype2idx = json.load(json_file)

## model load
model = models.load_model(scriptdir + '/modesave/'+ modelmark + '.h5')

def readfpkm(fpkmfile):
    fpkm = pd.read_table(fpkmfile)
    fpkm.index = fpkm['GeneName']
    fpkm = pd.DataFrame(fpkm.iloc[:, -1])
    return fpkm

def readfpkmEnsembl(fpkmfile):
    fpkm = pd.read_table(fpkmfile)
    # geneid = fpkm['GeneID']
    geneid = fpkm.iloc[:,0]
    geneid = [re.sub(r'\.\d+$','',x) for x in geneid]
    fpkm.index = geneid
    fpkm = pd.DataFrame(fpkm.iloc[:, -1])
    return fpkm

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
        fpkm = fpkm.append(fpkm_notin)

    dx = []
    for idx, row in fpkm.iloc[:, :].iteritems():
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

# def dx2res(dx, model, id):
#     py = model.predict(dx)
#
#     pydf = pd.DataFrame(py, index=[id])
#     pydf.columns = [idx2subtype[str(x)] for x in pydf.columns]
#     pydf['PredSubtype'] = prob2type(py)
#     return pydf

def dx2res(dx, model, ids):
    ## 211206 update:
    # 1.one sample per row -> one sample per column
    # 2.wide table to long table
    # 3.PredSubtype move to first row
    # 4.add prob to PredSubtype

    py = model.predict(dx)
    besttype = prob2type(py)
    if(len(besttype) > 1 ):
        besttype = 'mutil-match'
    else:
        besttype = besttype[0]
        bestp = format(py[0, subtype2idx[besttype]], '.4f')
        besttype = besttype + ' (' + bestp + ')'


    py = [format(x, '.4f') for x in py[0]]
    py = np.array(py).astype('float')
    pydf = pd.DataFrame(py, columns=[ids])
    pydf.index = [idx2subtype[str(x)] for x in pydf.index]
    pydf = pd.DataFrame(pd.Series({'PredSubtype': besttype}), columns=[ids]).append(pydf)
    return pydf


# ids = glob.glob(fpkmdir+"*_all_fpkm.txt")
# ids = [x.replace(fpkmdir, '') for x in ids]
# ids = [x.replace('_all_fpkm.txt', '') for x in ids]
pydf_m = pd.DataFrame()
# fpkmfile = fpkmdir + i + '_all_fpkm.txt'
fpkm = readfpkmEnsembl(ids)
dx = fpkm2dx(fpkm)
pydf = dx2res(dx, model, ids)
pydf_m = pydf_m.append(pydf)
# pydf_m = np.transpose(pydf_m)
# k = pydf_m.shape[0]
# pydf_m = pydf_m.iloc[(k-1):k, :].append(pydf_m.iloc[0:(k-1), :])
# format(pydf_m.iloc[1:k, 0], '.3f')

out = outdir+'/pydf_ball_'+outmark+'.tab'
pydf_m.to_csv(out, sep='\t', header=0)
#os.chmod(out,stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
#pydf_m.to_excel('pydf_merge_20210817.xls')

