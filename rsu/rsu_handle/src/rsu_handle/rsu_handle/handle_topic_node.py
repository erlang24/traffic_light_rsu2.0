from std_msgs.msg import String
from asn_msgs.msg import IntersectionState
import asn1tools
import rclpy
from rclpy.node import Node
import os
from std_msgs.msg import UInt8MultiArray
from ament_index_python.packages import get_package_share_directory


class TrafficLightReceiver(Node):

    def __init__(self):
        super().__init__('handle_topic_node')

        # 订阅 /intersection_state_msg 话题
        self.intersection_state_sub = self.create_subscription(
            IntersectionState,
            '/intersection_state_msg',
            self.intersection_state_msg2asn,
            10)
        
        # self.udp_publisher = self.create_publisher(UInt8MultiArray, '/rsu_json', 10)
        self.rsu_map_publisher = self.create_publisher(UInt8MultiArray, '/rsu_map', 10)

        package_share_directory = get_package_share_directory('rsu_handle')
        
        # 获取 asn 文件的路径
        asn_files = [
            os.path.join(package_share_directory, 'asn/BSM.asn'),
            os.path.join(package_share_directory, 'asn/MapSpeedLimit.asn'),
            os.path.join(package_share_directory, 'asn/VehClass.asn'),
            os.path.join(package_share_directory, 'asn/RSM.asn'),
            os.path.join(package_share_directory, 'asn/DefPosition.asn'),
            os.path.join(package_share_directory, 'asn/MapLink.asn'),
            os.path.join(package_share_directory, 'asn/MapPoint.asn'),
            os.path.join(package_share_directory, 'asn/MapNode.asn'),
            os.path.join(package_share_directory, 'asn/DefTime.asn'),
            os.path.join(package_share_directory, 'asn/DefMotion.asn'),
            os.path.join(package_share_directory, 'asn/MapLane.asn'),
            os.path.join(package_share_directory, 'asn/VehSize.asn'),
            os.path.join(package_share_directory, 'asn/MsgFrame.asn'),
            os.path.join(package_share_directory, 'asn/Map.asn'),
            os.path.join(package_share_directory, 'asn/VehSafetyExt.asn'),
            os.path.join(package_share_directory, 'asn/DefPositionOffset.asn'),
            os.path.join(package_share_directory, 'asn/RSI.asn'),
            os.path.join(package_share_directory, 'asn/VehStatus.asn'),
            os.path.join(package_share_directory, 'asn/DefAcceleration.asn'),
            os.path.join(package_share_directory, 'asn/VehEmgExt.asn'),
            os.path.join(package_share_directory, 'asn/VehBrake.asn'),
            os.path.join(package_share_directory, 'asn/SPATIntersectionState.asn'),
            os.path.join(package_share_directory, 'asn/SignalPhaseAndTiming.asn'),
        ]
        self.asn1_spec = asn1tools.compile_files(asn_files, numeric_enums=True)


    def intersection_state_msg2asn(self, msg):
        self.get_logger().info(f"收到的消息: {msg}")
        try:
            spat_message = {
                'msgCnt': 101,
                'intersections': [{
                    'intersectionId': {
                        'region': 500,
                        'id': msg.intersection_id
                    },
                    'status': (b'0000100000000000', 16 *8),
                    'phases': []
                }]
            }

            current_time = 0
            for phase in msg.phases:
                phase_data = {
                    'id': phase.id,
                    'phaseStates': []
                }

                for i, phase_state in enumerate(phase.phase_states):
                    # 如果有上一个灯的结束时间，更新 startTime
                    start_time = current_time if i == 0 else phase_data['phaseStates'][-1]['timing'][1]['likelyEndTime']
                    
                    # 更新 nextDuration 和 likelyEndTime
                    next_duration = calculate_next_duration(phase_state)
                    likely_end_time = start_time + phase_state.current_time_remaining

                    # 创建 phase state 数据
                    state_data = {
                        'light': phase_state.light,
                        'timing': ('counting', {
                            'startTime': start_time,
                            'likelyEndTime': likely_end_time,
                            'nextDuration': next_duration,
                            # 'timeConfidence': 100
                        })
                    }
                    
                    # 更新current_time为最后一个灯的likelyEndTime
                    current_time = likely_end_time
                    phase_data['phaseStates'].append(state_data)

                spat_message['intersections'][0]['phases'].append(phase_data)

            # ASN.1 编码
            # encoded_spat = self.asn.encode('MessageFrame', ('spatFrame', spat_message))
            encoded_spat = self.asn1_spec.encode('MessageFrame', ('spatFrame', spat_message))
            
            # 创建 ROS 消息并发布
            ros_msg = UInt8MultiArray()
            ros_msg.data = list(encoded_spat)
            self.rsu_map_publisher.publish(ros_msg)
            
            self.get_logger().info("SPAT消息编码并发布成功")
            # decoded_spat = self.asn.decode('MessageFrame', encoded_spat)
            decoded_spat = self.asn1_spec.decode('MessageFrame', encoded_spat)

            print("解码后的SPAT消息:", decoded_spat)

        except Exception as e:
            self.get_logger().error(f"SPAT消息处理错误: {e}")


def calculate_next_duration(phase_state):
    # 根据信号灯状态返回持续时长（单位为毫秒）
    if phase_state.light == 3:  # 红灯
        return 80  # 红灯持续时长8s
    elif phase_state.light == 6:  # 绿灯
        return 50  # 绿灯持续时长5s
    elif phase_state.light == 7:  # 黄灯
        return 30  # 黄灯持续时长3s
    return 0  # 默认值



def main(args=None):
    rclpy.init(args=args)
    node = TrafficLightReceiver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

