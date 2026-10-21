from machine import Pin, I2C, time_pulse_us
from time import sleep_us, sleep
import ssd1306

# HC-SR04 引脚
TRIG_PIN = 4
ECHO_PIN = 27

# OLED I2C 引脚
SDA_PIN = 23
SCL_PIN = 18
OLED_ADDR = 0x3C

# 初始化 OLED
i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=400000)
devices = i2c.scan()
print("I2C devices:", [hex(addr) for addr in devices])

if OLED_ADDR not in devices:
    raise Exception("没有找到 OLED，请检查 I2C 引脚和地址")

oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=OLED_ADDR)

# 初始化 HC-SR04
trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)
trig.value(0)


def measure_cm():
    # 发送触发脉冲
    trig.value(0)
    sleep_us(2)
    trig.value(1)
    sleep_us(10)
    trig.value(0)

    # 测量 ECHO 高电平时间，最长等待 30ms
    duration = time_pulse_us(echo, 1, 30000)

    if duration < 0:
        return None

    # 声波往返距离除以 2，换算为厘米
    return duration * 0.0343 / 2


while True:
    distance = measure_cm()

    oled.fill(0)

    if distance is None:
        oled.text("Dist: No echo", 0, 40)
        print("未收到回波，请检查接线或目标距离")
    else:
        oled.text("Dist: {:.1f} cm".format(distance), 0, 40)
        print("距离: {:.1f} cm".format(distance))

    oled.show()
    sleep(0.5)