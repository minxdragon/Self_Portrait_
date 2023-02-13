#!/bin/bash

#activate conda environment
source activate selfportrait

#go to directory
cd /Users/j.rosenbaum/Documents/GitHub/FaceSwap 

#export Key
export REPLICATE_API_TOKEN=798257c4fb85e3ea496075c8904fcd44d56012f7

#run server
python3 server.py