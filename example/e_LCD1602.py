from machine import Pin, I2C
from time import sleep_ms, sleep_us

# ESP32 I2C：SDA 接 GPIO21，SCL 接 GPIO22
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

addresses = i2c.scan()
print("扫描到的 I2C 地址:", [hex(addr) for addr in addresses])

# LCD1602 常见地址为 0x27 或 0x3F
if 0x27 in addresses:
    lcd_address = 0x27
elif 0x3F in addresses:
    lcd_address = 0x3F
elif addresses:
    lcd_address = addresses[0]
else:
    print("没有发现 I2C 设备，请检查 SDA、SCL、VCC 和 GND 接线")
    while True:
        sleep_ms(1000)


# 常见 PCF8574 LCD 转接板引脚映射
# P0=RS, P1=RW, P2=EN, P3=背光, P4-P7=D4-D7
class LCD1602:
    def __init__(self, i2c, address):
        self.i2c = i2c
        self.address = address
        self.backlight = 0x08
        sleep_ms(50)

        # 初始化为 4-bit 模式
        self._write_nibble(0x30, 0)
        sleep_ms(5)
        self._write_nibble(0x30, 0)
        sleep_us(150)
        self._write_nibble(0x30, 0)
        self._write_nibble(0x20, 0)

        self.command(0x28)  # 4-bit、两行显示
        self.command(0x0C)  # 显示开，光标关
        self.command(0x06)  # 写入后光标右移
        self.clear()

    def _expander_write(self, value):
        self.i2c.writeto(self.address, bytes([value | self.backlight]))

    def _write_nibble(self, nibble, rs):
        value = (nibble & 0xF0) | (0x01 if rs else 0)
        self._expander_write(value | 0x04)  # EN 高
        sleep_us(1)
        self._expander_write(value)         # EN 低
        sleep_us(50)

    def _write_byte(self, value, rs):
        self._write_nibble(value & 0xF0, rs)
        self._write_nibble((value << 4) & 0xF0, rs)

    def command(self, value):
        self._write_byte(value, 0)

    def write_char(self, char):
        self._write_byte(ord(char), 1)

    def clear(self):
        self.command(0x01)
        sleep_ms(2)

    def move_to(self, column, row):
        row_offsets = (0x00, 0x40)
        self.command(0x80 | (column + row_offsets[row]))

    def putstr(self, text):
        for char in text:
            self.write_char(char)


lcd = LCD1602(i2c, lcd_address)
lcd.move_to(0, 0)
lcd.putstr("2026")
lcd.move_to(0, 1)
lcd.putstr("Addr: 0x{:02X}".format(lcd_address))