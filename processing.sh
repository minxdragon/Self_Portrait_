#!/bin/bash

#set export PATH
export PATH="/Applications/Processing.app/Contents/MacOS:$PATH"

# Initialize the variable to track success
all_success=true

#open Syphoncam
cd /Users/sgm_tech/Documents/Self_Portrait_-base/syphoncam 
if nohup processing-java --sketch=$PWD --run; then
    echo "Syphoncam is running"
else
    echo "Error: Syphoncam failed to run"
    all_success=false
fi

sleep 2

#open galleryPlayer
cd /Users/sgm_tech/Documents/Self_Portrait_-base/interactive/data/galleryPlayer
if nohup processing-java --sketch=$PWD --run; then
    echo "galleryPlayer is running"
else
    echo "Error: galleryPlayer failed to run"
    all_success=false
fi

sleep 2

#open galleryPlayer2
cd /Users/sgm_tech/Documents/Self_Portrait_-base/interactive/galleryPlayer2
if nohup processing-java --sketch=$PWD --run; then
    echo "galleryPlayer2 is running"
else
    echo "Error: galleryPlayer2 failed to run"
    all_success=false
fi

# Check if all commands ran successfully
if $all_success; then
    echo "All processes started successfully"
else
    echo "Some processes failed to start"
fi
