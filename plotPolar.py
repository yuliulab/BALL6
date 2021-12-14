# -*- coding: utf-8 -*-
# @Time : 21/11/11 14:51
# @Author : Bowen Cui
# @Email : xcxiongmao@126.com
# @File : plotPolar.py
# @Project : predRNN

import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Polar
import sys
import os
import stat

# os.getcwd()
axis_min = -0.06
axis_max = 1
cutoff = 0.9

ids = str(sys.argv[1])
# wddir = str(sys.argv[2])
outprefix=str(sys.argv[2])

outdir=os.path.split(outprefix)[0]
outmark=os.path.split(outprefix)[1]
if outdir == '':
    outdir = './'
outdir=os.path.abspath(outdir)
if outmark == '':
    outmark = os.path.split(ids)[1]
    outmark = os.path.splitext(outmark)[0]

# print("polar plot input: " + ids)

# data = pd.read_table("./pyecharts/example_out/pydf_ball_sample1.tab", index_col=0)
data = pd.read_table(outdir + "/pydf_ball_" + outmark + ".tab", index_col=0)
data = pd.read_table(outdir + "/pydf_ball_" + outmark + ".tab")
# subtype = data.columns.values.tolist()
# value = data.iloc[0, :].tolist()
subtype = data.iloc[:, 0].tolist()
value = data.iloc[:, 1].tolist()

value_bg = [i if i < cutoff else axis_min for i in value]
value_fg = [i if i >= cutoff else axis_min for i in value]

c = (
    Polar()
    # .add_schema(angleaxis_opts=opts.AngleAxisOpts(data=subtype, type_="category"))
    .add_schema(
        angleaxis_opts=opts.AngleAxisOpts(data=subtype, type_="category"),
        radiusaxis_opts=opts.RadiusAxisOpts(type_="value", min_=axis_min, max_=axis_max))
    # .add("", value, type_="bar", label_opts=opts.LabelOpts(is_show=False))
    .add("", value_fg, type_="bar", label_opts=opts.LabelOpts(is_show=False), stack="a")
    .add("", value_bg, type_="bar", label_opts=opts.LabelOpts(is_show=False), stack="a")
    # .set_global_opts(title_opts=opts.TitleOpts(title=outmark))
    .render(outdir + "/polar_ball_" + outmark + ".html")
)
os.chmod(outdir + "/polar_ball_" + outmark + ".html",
    stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)


data = pd.read_table(outdir + "/pydf_al_" + outmark + ".tab")
subtype = data.iloc[:, 0].tolist()
for i in range(len(subtype)):
    subtype.insert(2*i, '')
value = data.iloc[:, 1].tolist()
for i in range(len(value)):
    value.insert(2*i, axis_min)

value_bg = [i if i < cutoff else axis_min for i in value]
value_fg = [i if i >= cutoff else axis_min for i in value]

c = (
    Polar()
    .add_schema(
        angleaxis_opts=opts.AngleAxisOpts(data=subtype, type_="category"), #boundary_gap=True
        radiusaxis_opts=opts.RadiusAxisOpts(type_="value", min_=axis_min, max_=axis_max))
    .add("", value_fg, type_="bar", label_opts=opts.LabelOpts(is_show=False), stack="a")
    .add("", value_bg, type_="bar", label_opts=opts.LabelOpts(is_show=False), stack="a")
    # .set_global_opts(title_opts=opts.TitleOpts(title=outmark))
    .render(outdir + "/polar_al_" + outmark + ".html")
)
# os.chmod(outdir + "/polar_al_" + outmark + ".html",
#     stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
