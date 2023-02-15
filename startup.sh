#!/bin/bash

#activate conda environment
source activate selfportrait

#go to directory
#cd /Users/j.rosenbaum/Documents/GitHub/FaceSwap 
cd /Users/sgm_tech/Documents/Self_Portrait_-base 
#export Key
export REPLICATE_API_TOKEN=798257c4fb85e3ea496075c8904fcd44d56012f7

#run server
while true; do
  python server.py
  if [ $? -ne 0 ]; then
    echo "Address is already in use, waiting for 10 seconds."
    sleep 10
  else
    break
  fi
done
