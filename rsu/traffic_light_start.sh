#!/bin/bash

echo "1. 启动docker"
gnome-terminal -- bash -c "cd ~/rsu && bash docker_run_develop_into.sh && sudo chmod 777 /dev/ttyUSB0; exec bash"


echo "2. 启动串口驱动" 
gnome-terminal -- bash -c "docker exec -it rsu_docker bash -c '\
source /opt/ros/galactic/setup.bash; \
cd ~/rsu/rsu_handle; \
source install/setup.bash; \
sudo chmod 777 /dev/ttyUSB0; \
ros2 launch serial_driver_py serial_driver.launch.py; \
exec bash'"

echo "3. 启动 rsu_handle 节点"
gnome-terminal -- bash -c "docker exec -it rsu_docker bash -c '\
source /opt/ros/galactic/setup.bash; \
cd ~/rsu/rsu_handle; \
source install/setup.bash; \
ros2 launch rsu_handle start.launch.py; \
exec bash'"
