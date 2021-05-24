import matplotlib.pyplot as plt

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray

plt.ion()
fig = plt.figure()
ax = plt.subplot(1,1,1)
th,r = [],[]
ax.plot(th,r,'ko',markersize = 1)
fig.show()

def recv_ydlidar(msg):
    yd = msg.data.tolist()
    th = [ yd[k] for k in range(0,len(yd),2) ]
    r  = [ yd[k] for k in range(1,len(yd),2) ]    

    ax.lines[0].set_data(th,r)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.flush_events()

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
