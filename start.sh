#!/bin/bash
set -e
#activate env 
.  ~/Environmental_Mesh/env/bin/activate &
#run script
#python Environmental_Mesh/firebase_upload.py &
python3 Environmental_Mesh/enviro_read.py
