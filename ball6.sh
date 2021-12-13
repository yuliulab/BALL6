#!/bin/sh
## 2021.11.10
export PYTHONDONTWRITEBYTECODE=1

FILE=$1
OUTPUT=$2
LOGFILE=${OUTPUT%/*}/log.${OUTPUT##*/}.txt
# echo file:$FILE
# echo output:$OUTPUT
# echo 'LOADING ENV'
# source activate py39

mkdir -p ${OUTPUT%/*}/

echo 'Running AL Model' > ${LOGFILE} && \
python /root/pred_al.py ${FILE} $OUTPUT \
  1>> ${LOGFILE} \
  2> /dev/null && \
echo 'Running BALL Model' >> ${LOGFILE} && \
python /root/pred_ball.py ${FILE} $OUTPUT \
  1>> ${LOGFILE} \
  2> /dev/null && \
python /root/plotPolar.py ${FILE} $OUTPUT && \
echo 'DONE!' >> ${LOGFILE}

chmod 777 ${LOGFILE}

#echo 'PLOTTING Polar' >> ${LOGFILE} && \

#chmod 777 ${OUTPUT%/*}/pydf_al_${OUTPUT##*/}.tab
#chmod 777 ${OUTPUT%/*}/pydf_ball_${OUTPUT##*/}.tab

# echo 'RUNNING AL model' && \
    # python /root/pred_al.py ${FILE} $OUTPUT && \
    # echo 'RUNNING BALL model' && \
    # python /root/pred_ball.py ${FILE} $OUTPUT && \
    # echo 'DONE!'

