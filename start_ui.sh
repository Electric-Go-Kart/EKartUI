#!/bin/bash

#EKartUI Startup Script

### Comment out CAN or vcan as needed ###
# Set up CAN interface
# sudo ip link set can0 up type can bitrate 500000
# Set up vcan interface
# sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0

# Start up CAN data parser
cd ~/projects/EKartUI
nohup python ./can_parse.py &
sleep 3

# Start up APD
# cd ~/projects/APD_deploy/yolov5
# nohup ./run_it.sh &
# sleep 30

# Start up EKartUI
cd ~/projects/EKartUI
nohup python ./Main.py &

# Delete the nohup.out file
rm nohup.out
