import sys

import rclpy
from std_msgs.msg import Int8MultiArray

# Don't care about win32 for simplicity (msvcrt)
import termios,tty

def getKey(current):
    tty.setraw(sys.stdin.fileno())
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, current)

    return key

cmds = {
    'k': ( 0, 0),
    'i': ( 1, 1),
    ',': (-1,-1),
    'u': ( 1, 0),
    'o': ( 0, 1),
    'm': (-1, 0),
    '.': ( 0,-1),
    'j': ( 1,-1),
    'l': (-1, 1),
}
    
current = termios.tcgetattr(sys.stdin)

rclpy.init()

node = rclpy.create_node('remocon_sender')
pub = node.create_publisher(Int8MultiArray, 'rcmd', 10)

try:
    while True:
        k = getKey(current)
        if k in cmds.keys():
            data = Int8MultiArray(data=cmds[k])
            print(data)
            pub.publish(data)
        else:
            if k == 'q' or k == '\x03': break

except Exception as e:
    print(e)

finally:
    pub.publish(Int8MultiArray(data=(0,0)))
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, current)
