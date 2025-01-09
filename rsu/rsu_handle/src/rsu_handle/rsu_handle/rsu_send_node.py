import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt8MultiArray
import socket

class RsuMapReceiver(Node):
    def __init__(self):
        super().__init__('rsu_map_receiver')
        
        # 声明参数
        self.declare_parameter('target_ip', '192.168.20.199')
        self.declare_parameter('target_port', 30300)
        
        # 获取参数
        self.targetip = self.get_parameter('target_ip').value
        self.targetport = self.get_parameter('target_port').value
        
        # 创建订阅者
        self.subscription = self.create_subscription(
            UInt8MultiArray,
            '/rsu_map',
            self.map_callback,
            10)
        
        # 创建UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.get_logger().info(f'RsuMapReceiver 初始化完成，目标IP: {self.targetip}, 目标端口: {self.targetport}')

    def map_callback(self, msg):
        try:
            # 获取二进制数据
            data = bytes(msg.data)
            
            # 通过UDP发送数据
            self.sock.sendto(data, (self.targetip, self.targetport))
            
            # self.get_logger().info(f'编码数据已发送到 {self.targetip}:{self.targetport}') #减少不必要的日志输出
            
        except Exception as e:
            self.get_logger().error(f'发送数据时出错: {str(e)}')

    def __del__(self):
        self.sock.close()

def main(args=None):
    rclpy.init(args=args)
    receiver = RsuMapReceiver()
    rclpy.spin(receiver)
    receiver.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
