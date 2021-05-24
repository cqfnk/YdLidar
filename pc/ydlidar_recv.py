import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray

def recv_ydlidar(msg):
    yd = msg.data.tolist()
    data = { yd[k]: yd[k+1] for k in range(0,len(yd),2) }
    for th,r in data.items():
        print(th,r)

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
