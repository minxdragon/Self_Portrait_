#!/bin/bash
#set export PATH
export PATH="/Applications/Processing.app/Contents/MacOS:$PATH"

#open processing windows
#cd ~/Documents/GitHub/FaceSwap

#open Syphoncam
cd  /Users/sgm_tech/Documents/Self_Portrait_-base/syphoncam 
#cd ~/Documents/GitHub/FaceSwap/syphoncam
nohup processing-java --sketch=$PWD --run &
echo "Syphoncam is running"

sleep 2

cd /Users/sgm_tech/Documents/Self_Portrait_-base/interactive/data/galleryPlayer
#cd ~/Documents/GitHub/FaceSwap/interactive/data/galleryPlayer
nohup processing-java --sketch=$PWD --run &
echo "galleryPlayer is running"

sleep 2

cd /Users/sgm_tech/Documents/Self_Portrait_-base/interactive/galleryPlayer2
#cd ~/Documents/GitHub/FaceSwap/interactive/data/galleryPlayer2
nohup processing-java --sketch=$PWD --run &
echo "galleryPlayer2 is running"
#open interactive/macos-x86_64/interactive.app

echo "to check these processes, type bg or check the nohup.out file"