#!/bin/sh

# echo admin | sudo chmod -R 777 /dev/ttyACM0
echo admin | sudo -S /home/toyoda/anaconda3/envs/Toyoda/bin/python3  /home/toyoda/livis_v2_toyota/republic/backend/camera_service_toyoda/plc_service.py
