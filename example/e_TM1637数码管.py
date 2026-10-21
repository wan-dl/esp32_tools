from machine import Pin
from time import sleep
import tm1637

# CLK 接 GPIO16，DIO 接 GPIO17
display = tm1637.TM1637(
    clk=Pin(16),
    dio=Pin(17),
    brightness=2  # 亮度 0～7，数字越小越暗
)

number = 0

while True:
    display.number(number)
    number = (number + 1) % 10000
    sleep(1)