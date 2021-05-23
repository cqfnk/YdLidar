import PyLidar3
port = '/dev/ttyUSB0'

obj = PyLidar3.YdLidarX4(port) 
obj.Connect()

gen=obj.StartScanning()

data = next(gen)
for angle,distance in data.items():
    print(angle,distance)

obj.StopScanning()
obj.Disconnect()
