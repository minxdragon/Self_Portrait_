#!/bin/bash
pgrep -f "script.py" | xargs kill
nohup python server.py &