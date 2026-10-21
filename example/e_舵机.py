from machine import Pin, PWM
from time import sleep

SERVO_GPIO = 17  # 示例：信号线接 GPIO18 时用 18；否则改成实际 GPIO

# 舵机控制信号：50 Hz，每个周期 20 ms
servo = PWM(Pin(SERVO_GPIO), freq=50)

def set_angle(angle):
    # 先限制在 0～180 度
    angle = max(0, min(180, angle))

    # 用较保守的 1000～2000 微秒脉宽控制
    pulse_us = 1000 + (angle * 1000 // 180)
    servo.duty_ns(pulse_us * 1000)

while True:
    for angle in (45, 90, 135, 90):
        print("转到", angle, "度")
        set_angle(angle)
        sleep(1)