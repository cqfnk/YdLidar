import matplotlib.pyplot as plt

d_threshold = 40
plot_dist_max = 2500

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
    data = msg.data.tolist()
    th = [ int(d/65536) for d in data ]
    r =  [ d % 65536 for d in data]
    
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
