# BALL6

![image-20211214132216676](https://github.com/yuliulab/BALL6/blob/main/docs/web-banner.png?raw=true)

BALL6 (B-cell Acute Leukemia Subtype Identification based on rank of eXpression): A deep learning tool for predicting AL and BALL subtypes based on the expression rank values of 476 selected genes.


Visit our online tool

http://cccg.ronglian.com/#/analysis



# INSTALL

We recommend installing BALL6 with conda. *If you don't have conda, see help installing conda [here](https://conda.io/en/latest/miniconda.html).*

###  Install Dependence
```shell
conda create --name ball6 python=3.9.1 libgcc-ng -c conda-forge
source activate ball6

conda install numpy=1.19.5 -c conda-forge
conda install pandas=1.3.0
conda install tensorflow=2.6.0 -c conda-forge
conda install grpcio=1.39.0 -c conda-forge
pip install pyecharts==1.9.0
```
### Install BALL6
```shell
git clone https://github.com/yuliulab/BALL6.git
cd BALL6
chmod +x ball6
```
The model files `modesave/*.keras` are also available for download at [sjtu pan](https://pan.sjtu.edu.cn/web/share/9e3ba555f5500fa1ae117dc9471b1a56).

### Run Test

We provide an example gene expression input file `/test/sample_sub_fpkm.txt`, and its results are also provided in `test/output/`. Users can reproduce the results with the following command:

```shell
cd test
alias ball6="PATH_TO_BALL6/ball6"
ball6 -i sample_sub_fpkm.txt -o ./output -m sample
```

# USAGE

### Command  Format

```
BALL6 -i expression.tab [-o output_dir] [-m moutput_file_prefix]

-i  A gene expression table file with tab text file contain 2 columns at least.
    The first column is ENSEMBL ID, and the last column is genes expression value.  
-o  Path to output dir, default './'  
-m  Prefix for output file, default 'ball6'  
```

### Input Requirement
In brief, the only input BALL6 required is the 476 genes expression table with **tab-separated**. The first column in the table should be the Ensembl gene ID, and the last column should be gene expression values or rank values.

The BALL6 only requires 229 genes for the AL model and 292 genes for the BALL model, the program will ignore other genes in the user’s input, and if there are some genes not in the input, the program will set its values to 0.

If the input file has the Ensembl version suffix in the first column, the program will strip off the suffix automatically. BALL6 will convert the input gene expression to rank values, which will help the model to avoid batch effect among data sources. So, it’s don’t matter if the gene expression of your input is original values or not, but it’s important on the difference in values size between the genes. 

An example input is provided in [here](https://github.com/yuliulab/BALL6/blob/main/test/sample_sub_fpkm.txt) `/test/sample_sub_fpkm.txt`, note that only the first and last columns are valid input.

### Results Explanation
There are two parts of the prediction results, representing the AL model and the BALL model, respectively. The prediction subtype and its probability are present in the table. The best prediction subtype is in the first row. All of the probabilities are rounded to four significant digits.

The polar interactive plots are followed, indicating a visualization of the probability size in each subtype. If the subtype probability is bigger than 0.9, its polar bar will be shown in red, and the other bar colors will be dark grey.

[Here](https://github.com/yuliulab/BALL6/blob/main/test/output/pydf_ball_sample.tab) is an example output `/test/output/`. Subtype predict probability was saved in the table and visualized as polar plots:

<img src='https://github.com/yuliulab/BALL6/blob/main/docs/polar-example_v2.0.png' align="right" width='400px'>

| PredSubtype      | ETV6::RUNX1 (0.9999) |
| ---------------- | -------------------- |
| DUX4             | 0                    |
| ETV6::RUNX1      | 0.9999               |
| ETV6::RUNX1-like | 0                    |
| HLF              | 0                    |
| HYPER            | 0                    |
| HYPO             | 0                    |
| IAMP21           | 0                    |
| IKZF1 N159Y      | 0                    |
| KMT2A            | 0                    |
| MEF2D            | 0                    |
| MYC              | 0                    |
| NUTM1            | 0                    |
| PAX5 P80R        | 0                    |
| PAX5alt          | 0                    |
| Ph               | 0                    |
| Phlike           | 0                    |
| TCF3::PBX1       | 0                    |
| ZEB2/CEBP        | 0                    |
| ZNF384           | 0                    |
| ZNF384-like      | 0                    |





# CONTACT US
If there are any questions in BALL6, feel free to contact us or [create an issue](https://github.com/yuliulab/BALL6/issues).

> **[Liu Lab](https://yuliulab.github.io/)**  
> Shanghai Children’s Medical Center, Shanghai Jiao Tong University, China  
> Bowen Cui: xcxiongmao@126.com  
> Yu Liu: yu.liu@sjtu.edu.cn

