import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray

def recv_ydlidar(msg):
    for d in msg.data.tolist():
        print(int(d/65536),d % 65536)

rclpy.init()

node = rclpy.create_node('ydlidar_receiver')
sub = node.create_subscription(Int32MultiArray, 'ydlidar', recv_ydlidar, 10 )

try:
    rclpy.spin(node)
except Exception as e:
    print(e)
finally:
    node.destroy_node()
    rclpy.shutdown()
