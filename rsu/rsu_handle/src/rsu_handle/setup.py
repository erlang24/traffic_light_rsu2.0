from setuptools import setup
import os

package_name = 'rsu_handle'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        # ('share/' + package_name,  + '/launch', ['launch/start.launch.py']),
        (os.path.join('share', package_name, 'launch'), ['launch/start.launch.py']), # 修改后的 launch 文件配置
        (os.path.join('share', package_name, 'config'), ['config/map_center.json.txt']), # 修改后的 launch 文件配置
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/asn', [
            'asn/BSM.asn',
            'asn/MapSpeedLimit.asn',
            'asn/VehClass.asn',
            'asn/RSM.asn',
            'asn/DefPosition.asn',
            'asn/MapLink.asn',
            'asn/MapPoint.asn',
            'asn/MapNode.asn',
            'asn/DefTime.asn',
            'asn/DefMotion.asn',
            'asn/MapLane.asn',
            'asn/VehSize.asn',
            'asn/MsgFrame.asn',
            'asn/Map.asn',
            'asn/VehSafetyExt.asn',
            'asn/DefPositionOffset.asn',
            'asn/RSI.asn',
            'asn/VehStatus.asn',
            'asn/DefAcceleration.asn',
            'asn/VehEmgExt.asn',
            'asn/VehBrake.asn',
            'asn/SPATIntersectionState.asn',
            'asn/SignalPhaseAndTiming.asn',
        ]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='erlang',
    maintainer_email='erlang@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'handle_topic_node = rsu_handle.handle_topic_node:main',
            'rsu_send_node = rsu_handle.rsu_send_node:main',
            'rsu_map_node = rsu_handle.rsu_map_node:main',
        ],
    },
)
