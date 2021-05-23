import pigpio

FS90R = {
    'bcm_pin': { 'R': 18, 'L': 19 },
    'freq': 50,
    'halt': 7.5, 'drive': 0.5,
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

from time import sleep

set_dc(FS90R['bcm_pin']['R'], freq, to_dc(FS90R['drive']))
set_dc(FS90R['bcm_pin']['L'], freq, to_dc(FS90R['drive']))
sleep(1)
set_dc(FS90R['bcm_pin']['R'], freq, 0)
set_dc(FS90R['bcm_pin']['L'], freq, 0)
