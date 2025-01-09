import asn1tools
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt8MultiArray
import ast
from ament_index_python.packages import get_package_share_directory
import os

class RsuMapNode(Node):
    def __init__(self):
        super().__init__('rsu_map_node')
        self.publisher = self.create_publisher(UInt8MultiArray, '/rsu_map', 10)
        self.declare_parameter('map_json_path', '/default/path/to/map.json')
        # 获取包的 share 目录
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

        self.map_data = self.read_map_file()
        self.encoded_data = None

        if self.map_data is not None:
            self.encode_map_data()
        
        self.timer = self.create_timer(1.0, self.timer_callback)

    def read_map_file(self):
        try:
            # 获取参数值
            json_file_path = self.get_parameter('map_json_path').get_parameter_value().string_value
            self.get_logger().info(f"读取地图文件: {json_file_path}")  # 打印日志以帮助调试
            with open(json_file_path, 'r') as f:
                content = f.read()
                return ast.literal_eval(content)
        except Exception as e:
            self.get_logger().error(f'Error reading map file: {str(e)}')
            return None

    def encode_map_data(self):
        try:
            self.get_logger().info('正在编码地图数据...')
            self.encoded_data = self.asn1_spec.encode("MessageFrame", ('mapFrame', self.map_data))
            self.get_logger().info('地图数据编码成功.')
        except Exception as e:
            self.get_logger().error(f"编码地图数据时出错: {str(e)}")

    def timer_callback(self):
        if self.encoded_data is None:
            self.get_logger().error('Encoded data is not available.')
            return 
        try:
            msg = UInt8MultiArray()
            msg.data = self.encoded_data

            self.publisher.publish(msg)
            self.get_logger().info(f"Published map data to /rsu_map")
        except Exception as e:
            self.get_logger().error(f"发布地图数据时出错: {str(e)}")

def main(args=None):
    rclpy.init(args=args)
    rsu_map_node = RsuMapNode()
    rclpy.spin(rsu_map_node)
    rsu_map_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
