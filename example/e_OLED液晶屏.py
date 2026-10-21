from machine import Pin, I2C
import ssd1306

# 示例引脚；若你的 OLED 接口使用其他 SDA/SCL，请按底板资料修改
i2c = I2C(0, sda=Pin(23), scl=Pin(18), freq=400000)

print("I2C devices:", [hex(addr) for addr in i2c.scan()])

oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

oled.fill(0)                 # 清屏
oled.text("chen xiao", 0, 0)    # 把这里改成想显示的英文/数字
oled.text("Height: 175CM", 10, 10)    # 把这里改成想显示的英文/数字
oled.show()

# from machine import Pin, I2C

# i2c = I2C(1, sda=Pin(18), scl=Pin(23), freq=100000)
# print([hex(addr) for addr in i2c.scan()])