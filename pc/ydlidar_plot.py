import matplotlib.pyplot as plt
from math import cos,sin,radians

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
    data = { yd[k] : yd[k+1] for k in range(0,len(yd),2) }
    
    x = [ r * cos(radians(90-deg)) for deg,r in data.items() ]
    y = [ r * sin(radians(90-deg)) for deg,r in data.items() ]

    ax.lines[0].set_data(x,y)
    ax.set_xlim(-700,700)
    ax.set_ylim(-700,700)
    ax.set_aspect('equal')
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
