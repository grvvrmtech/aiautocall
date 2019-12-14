#!/bin/bash
file_path=$1

cd /home/abhimanyu/github/kaldi/egs/mix_noise
bash decode_command_line.sh $file_path 2>&1 | grep -E ^utterance-id1 | cut -d' ' -f2-
