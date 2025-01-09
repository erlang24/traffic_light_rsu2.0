## RSU可进行 MAP SPAT 消息的发布

此文件夹需放在 `/home/promote/` 下 执行。  
进入 rsu/rsu_handle/ 文件夹，执行 `bash traffic_light_start.sh` 开始运行，在第二个终端输入密码 `123456` 即可启动串口驱动。

## 参数
RSU默认的ip和端口号为 `192.168.20.199:30300`，如需修改可在 `rsu_handle/install/rsu_handle/share/rsu_handle/launch/start.launch.py` 中修改。  
 
广播的 MAP 消息 路径为 `rsu_handle/install/rsu_handle/share/rsu_handle/config/map_center.json.txt` 如果需要更改，将txt文件里面的内容替换即可。