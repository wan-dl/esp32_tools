from machine import Pin, PWM
from time import sleep_ms

LED_PIN = 25

# 初始化 PWM
led = PWM(Pin(LED_PIN), freq=1000)

# 兼容支持 duty_u16() 和旧版 duty() 的 MicroPython
use_duty_u16 = hasattr(led, "duty_u16")

def set_brightness(value):
    # value 范围：0～1023
    if use_duty_u16:
        led.duty_u16(value * 65535 // 1023)
    else:
        led.duty(value)

try:
    while True:
        # 渐亮
        for brightness in range(0, 1024, 8):
            set_brightness(brightness)
            sleep_ms(10)

        # 渐暗
        for brightness in range(1023, -1, -8):
            set_brightness(brightness)
            sleep_ms(10)

except KeyboardInterrupt:
    set_brightness(0)
    led.deinit()