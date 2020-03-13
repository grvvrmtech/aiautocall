#!/sbin/bash

kaldi_home=$1
project=$2
test=$3
tree=$4
kws_upload=$5
kws_raw_list=$6
rm -rf ${kaldi_home}/${project}/data/${test}*
mkdir ${kaldi_home}/${project}/data/${test}
cp kws/data/${kws_raw_list} ${kaldi_home}/${project}/
cp ${kws_upload}/wav.scp ${kws_upload}/utt2spk ${kws_upload}/spk2utt ${kaldi_home}/${project}/data/${test}/
cd ${kaldi_home}/${project}/
bash ivector.sh
bash ${test}_tdnn_aug_1a.sh
bash ${test}_kws_prep.sh
cd -
cp ${kaldi_home}/${project}/${tree}/kws_14/kwslist.xml kws/data/
cp ${kaldi_home}/${project}/data/${test}/kws/keywords.txt kws/data/
