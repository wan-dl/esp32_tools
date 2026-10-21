from machine import Pin, PWM
from time import sleep

MOTOR_PIN = 15

motor = PWM(Pin(MOTOR_PIN), freq=1000)

def set_speed(percent):
    """设置速度百分比：0～100"""
    percent = max(0, min(100, percent))

    # 兼容不同版本的 MicroPython
    if hasattr(motor, "duty_u16"):
        motor.duty_u16(percent * 65535 // 100)
    else:
        motor.duty(percent * 1023 // 100)

while True:
    set_speed(40)   # 以约 40% PWM 占空比运行，可调低或调高
    sleep(2)        # 转 2 秒

    set_speed(0)    # 停止
    sleep(3)        # 停 3 秒