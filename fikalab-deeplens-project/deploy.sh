#!/usr/bin/env bash
set +x
source .env
ssh aws_cam@$DEEP_LENS_HOST "mkdir -p ~/fikalab-deeplens-project"
scp -r cpdl main.py TrackingPeople.py aws_cam@$DEEP_LENS_HOST:~/fikalab-deeplens-project/
ssh -t aws_cam@$DEEP_LENS_HOST "cd ~/fikalab-deeplens-project && sudo python main.py"
