from machine import Pin
from neopixel import NeoPixel
from time import sleep

LED_PIN = 16
NUM_LEDS = 5
BRIGHTNESS = 1  # 0～255，数值越小越暗

leds = NeoPixel(Pin(LED_PIN), NUM_LEDS)

colors = [
    (255, 0, 0),    # 红
    (0, 255, 0),    # 绿
    (0, 0, 255),    # 蓝
    (255, 255, 0),  # 黄
    (0, 255, 255),  # 青
    (255, 0, 255),  # 紫
    (0, 0, 0),      # 关灯
]

def dim(color):
    return tuple(channel * BRIGHTNESS // 255 for channel in color)

while True:
    for color in colors:
        leds.fill(dim(color))
        leds.write()
        sleep(1)