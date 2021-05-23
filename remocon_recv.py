# FS90R
import pigpio

FS90R = {
    'bcm_pin': { 'R': 18, 'L': 19 },
    'freq': 50,
    'halt': 7.5, 'drive': 0.4,
    'duration':0.1,
}

# 送信用のduty cycle パラメータに変換
def to_dc(dcr,factor=10000.0):
    return int(dcr * factor)

freq  = FS90R['freq']
halt = to_dc(FS90R['halt'])

pi = pigpio.pi()

def set_dc(bcm,freq,dc):
    pi.hardware_PWM(bcm,freq,halt+dc)

def init_FS90R():
    for wheel in ('R','L'):
        bcm = FS90R['bcm_pin'][wheel]
        pi.set_mode(bcm,pigpio.OUTPUT)
        set_dc(bcm,freq,0)
                    
init_FS90R()

#######  ROS2 subscriber
import sys
import rclpy
from std_msgs.msg import Int8MultiArray

# Don't care about win32 for simplicity (msvcrt)
import termios
import tty

def recv_cmd(msg):
    print(msg.data)
    L,R = msg.data.tolist()
    set_dc(FS90R['bcm_pin']['L'], freq, L * to_dc(FS90R['drive']))
    set_dc(FS90R['bcm_pin']['R'], freq, R * to_dc(FS90R['drive']))

rclpy.init()
node = rclpy.create_node('remocon_receiver')
sub = node.create_subscription(Int8MultiArray, 'rcmd', recv_cmd,10)

try:
    rclpy.spin(node)
except KeyboardInterrupt:
    pass

node.destroy_node()
rclpy.shutdown()
