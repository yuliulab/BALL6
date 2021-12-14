![image-20211214132216676](https://github.com/yuliulab/BALL6/blob/main/pic/web-banner.png?raw=true)

BALL6 (B-cell Acute Leukemia Subtype Identification based on rank of eXpression): A deep learning tool for predicting AL and BALL subtypes based on the expression rank values of 455 selected genes.


Visit our online tool

http://cccg.ronglian.com/#/analysis



### INSTALL
#####  Install dependence
```shell
conda install python=3.9.1 libgcc-ng -c conda-forge
conda install numpy=1.19.5 -c conda-forge
conda install pandas=1.3.0 -c conda-forge
conda install tensorflow=2.6.0 -c conda-forge
conda install grpcio=1.39.0 -c conda-forge
pip install pyecharts==1.9.0
```
##### Install BALL6
```shell
git clone https://github.com/yuliulab/BALL6.git
chmod +x ball6
```
##### Run test
```shell
cd test
../ball6 -i sample_sub_fpkm.txt -o ./output -m sample
```

### USEAGE

```shell
BALL6 -i expression.tab [**-o** output_dir] [**-m** moutput_file_prefix]

-i  A gene expression table file with tab text file contain 2 columns at least.
    The first column is ENSEMBL ID, and the last column is genes expression value.  
-o  Path to output dir, defult './'  
-m  Prefix for output file, defult 'ball6'  
```

##### Input Requirement
In brief, the only input BALL6 required is the 455 genes expression table with **tab-separated**. The first column in the table should be the Ensembl gene ID, and the last column should be gene expression values or rank values.

The BALL6 only requires 229 genes for the AL model and 271 genes for the BALL model, the program will ignore other genes in the user’s input, and <u>if there are some genes not in the input, the program will set its values to 0.</u>

If the input file has the Ensembl version suffix in the first column, the program will strip off the suffix automatically. BALL6 will convert the input gene expression to rank values, which will help the model to avoid batch effect among data sources. So, it’s don’t matter if the gene expression of your input is original values or not, but it’s important on the difference in values size between the genes.

##### Results Explanation
There are two parts of the prediction results, representing the AL model and the BALL model, respectively. The prediction subtype and its probability are present in the table. The best prediction subtype is in the first row. All of the probabilities are rounded to four significant digits.

The polar interactive plots are followed, indicating a visualization of the probability size in each subtype. If the subtype probability is bigger than 0.9, its polar bar will be shown in red, and the other bar colors will be dark grey.



>BALL6 **-i** expression.tab [**-o** output_dir] [**-m** moutput_file_prefix]  
>    **-i**  A gene expression table file with tab text file contain 2 columns at least.  
>         The first column is ENSEMBL ID, and the last column is genes expression value.  
>    **-o**  Path to output dir, defult './'  
>    **-m**  Prefix for output file, defult 'ball6'  

