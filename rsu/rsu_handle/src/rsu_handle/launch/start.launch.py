from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_share_dir = get_package_share_directory('rsu_handle')
    default_json_path = os.path.join(pkg_share_dir, 'config', 'map_center.json.txt') 

    map_json_path_arg = DeclareLaunchArgument(
        'map_json_path',
        default_value=default_json_path,
        description='Path to the JSON map file'
    )

    rsu_map_node = Node(
        package='rsu_handle',
        executable='rsu_map_node',
        output='screen',
        emulate_tty=True,
        parameters=[
            {'map_json_path': LaunchConfiguration('map_json_path')}
        ]
    )

    handle_topic_node = Node(
        package='rsu_handle',
        executable='handle_topic_node',
        output='screen',
        emulate_tty=True,
    )

    rsu_send_node = Node(
        package='rsu_handle',
        executable='rsu_send_node',
        output='screen',
        emulate_tty=True,
        parameters=[
            {'target_ip': '192.168.20.199'},  # 默认IP
            {'target_port': 30300}  # 默认端口
        ]
    )

    ld = LaunchDescription()

    ld.add_action(map_json_path_arg)
    ld.add_action(rsu_map_node)
    ld.add_action(handle_topic_node)
    ld.add_action(rsu_send_node)

    return ld
