from machine import Pin, ADC
from time import sleep_ms

# 建议把 AO 从 GPIO15 改接 GPIO34
audio = ADC(Pin(15))
audio.atten(ADC.ATTN_11DB)

# DO 接 GPIO27，并启用上拉
sound_digital = Pin(34, Pin.IN, Pin.PULL_UP)

print("开始读取声音模块")

while True:
    analog_value = audio.read()
    digital_value = sound_digital.value()

    # 假设模块检测到声音时 DO 输出低电平
    sound_detected = (digital_value == 0)

    print("AO:", analog_value,
          " DO:", digital_value,
          "检测到声音:", sound_detected)

    sleep_ms(100)