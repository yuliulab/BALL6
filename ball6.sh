#!/bin/sh
## 2021.11.10
export PYTHONDONTWRITEBYTECODE=1

while getopts "i:o:m:" opt
do
  case $opt in
    i)
    FILE=$OPTARG
    ;;
    o)
    OUTDIR=$OPTARG
    ;;
    m)
    PREFIX=$OPTARG
    ;;
    ?)
    echo -e "usage: \e[1;34mBALL6 \e[1;33m-i \e[1;0mexpression.tab [\e[1;33m-o \e[1;0moutput_dir] [\e[1;33m-m \e[1;0mmoutput_file_prefix]"

    echo -e "  \e[1;33m-i \e[1;0m A gene expression table file with tab text file contain 2 columns at least.\n      The first column is ENSEMBL ID, and the last column is genes expression value."
    echo -e "  \e[1;33m-o \e[1;0m Path to output dir, defult './'"
    echo -e "  \e[1;33m-m \e[1;0m Prefix for output file, defult 'ball6'"

    exit 1;;
  esac
done


if [[ $FILE -eq '' ]]
then
  echo -e "ERROR: Parameter -i is necessary (see 'ball6 -h')"
  exit 1
fi


if [[ $OUTDIR != /* ]];
then
 OUTDIR=./$OUTDIR
fi

if [[ $PREFIX -eq '' ]]
then
  PREFIX='ball6'
fi

# FILE=$1
OUTPUT=$OUTDIR/$PREFIX
LOGFILE=${OUTPUT%/*}/log.${OUTPUT##*/}.txt
# echo $OUTPUT
# echo $FILE
# echo $LOGFILE


WORKDIR=$(cd "$(dirname "$0")"; pwd)


echo 'Wellcome to BALL6!'
echo 'Visit our online tool http://cccg.ronglian.com/#/analysis'

mkdir -p ${OUTPUT%/*}/

echo 'Running AL Model' > ${LOGFILE} && \
python ${WORKDIR}/pred_al.py ${FILE} $OUTPUT \
  1>> ${LOGFILE} \
  2> /dev/null && \
echo 'Running BALL Model' >> ${LOGFILE} && \
python ${WORKDIR}/pred_ball.py ${FILE} $OUTPUT \
  1>> ${LOGFILE} \
  2> /dev/null && \
python ${WORKDIR}/plotPolar.py ${FILE} $OUTPUT && \
echo 'DONE!' >> ${LOGFILE}

#chmod 777 ${LOGFILE}


