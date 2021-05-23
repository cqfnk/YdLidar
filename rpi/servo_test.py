import pigpio

FS90R = {
    'bcm_pin': { 'R': 18, 'L': 19 },
    'freq': 50,
    'halt': 7.5, 'drive': 0.5,
    'duration':0.1,
}

# 送信用のduty cycle パラメータに変換
def to_pgdc(dcr,factor=10000.0):
    return int(dcr * factor)

pi = pigpio.pi()

def set_dc(bcms=FS90R['bcm_pin'].values(),
           freq=FS90R['freq'],
           dc=0):
    for bcm in [bcms] if isinstance(bcms,int) else bcms:
        pi.hardware_PWM(bcm,freq,to_pgdc(FS90R['halt']+dc))

def init_FS90R():
    for wheel in ('R','L'):
        bcm = FS90R['bcm_pin'][wheel]
        pi.set_mode(bcm,pigpio.OUTPUT)
        set_dc()
                    
init_FS90R()

from time import sleep

set_dc(dc=FS90R['drive'])
sleep(1)
set_dc()
