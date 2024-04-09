#!/bin/bash

#EKartUI Startup Script
# Function to handle cleanup actions
cleanup() {
    # Add your cleanup actions here
    echo "Performing cleanup actions..."
    # For example:
    # Terminate processes, close files, release resources, etc.
}

# Register the cleanup function to be called on exit or termination signals
trap cleanup EXIT SIGTERM SIGINT

### Comment out CAN or vcan as needed ###
# Set up CAN interface
sudo ip link set can0 up type can bitrate 500000
# Set up vcan interface
# sudo modprobe vcan
# sudo ip link add dev vcan0 type vcan
# sudo ip link set up vcan0

# Start up CAN data parser
cd ~/projects/EKartUI
python ./lib/controllers/can_parse.py &
sleep 3

# Start up CAN data parser
cd ~/projects/EKartUI
python3 ~/projects/EKartUI/Main.py
sleep 3

# Start up APD
# cd ~/projects/APD_deploy/yolov5
# nohup ./run_it.sh &
# sleep 30

# Start up EKartUI
# cd ~/projects/EKartUI
# nohup python3 ./Main.py
