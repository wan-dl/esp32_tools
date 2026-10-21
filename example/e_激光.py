from machine import Pin
from time import sleep

# 激光模块 S/IN 接 GPIO33
laser = Pin(33, Pin.OUT)
laser.value(0)  # 启动时先关闭

while True:
    laser.value(1)  # 开
    sleep(1)
    laser.value(0)  # 关
    sleep(1)