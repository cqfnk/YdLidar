import PyLidar3
port = '/dev/ttyUSB0'
chunk_size = 12000
obj = PyLidar3.YdLidarX4(port,chunk_size=chunk_size) 

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
        data = Int32MultiArray(data=sum(ydata.items(),()))
        pub.publish(data)
        
except Exception as e:
    print(e)

finally:
    obj.StopScanning()
    obj.Disconnect()
