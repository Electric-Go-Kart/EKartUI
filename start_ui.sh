#!/bin/bash
# Start the CAN interface and the UI for the EKart project
sudo ip link set can0 up type can bitrate 500000
python3 /home/gokart/projects/EKartUI/Main.py
