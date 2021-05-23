import PyLidar3
port = '/dev/ttyUSB0'
obj = PyLidar3.YdLidarX4(port) 

import rclpy
from std_msgs.msg import Int32MultiArray
from time import sleep

rclpy.init()
node = rclpy.create_node('ydlidar_sender')
pub = node.create_publisher(Int32MultiArray,'ydlidar',10)

obj.Connect()
gen=obj.StartScanning()

try:
    while True:
        ydata = next(gen)
        data = Int32MultiArray(data=[ y[0] * 65536 + y[1] for y in ydata.items() ])
        pub.publish(data)
        
except Exception as e:
    print(e)

finally:
    obj.StopScanning()
    obj.Disconnect()
