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

>BALL6 **-i** expression.tab [**-o** output_dir] [**-m** moutput_file_prefix]  
>    **-i**  A gene expression table file with tab text file contain 2 columns at least.  
>        The first column is ENSEMBL ID, and the last column is genes expression value.  
>    **-o**  Path to output dir, defult './'  
>    **-m**  Prefix for output file, defult 'ball6'  

