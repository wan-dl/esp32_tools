from machine import Pin, time_pulse_us
import time

# 普中板载红外接收头的信号脚
IR_PIN = 14
ir = Pin(IR_PIN, Pin.IN, Pin.PULL_UP)

def pulse(level, timeout_us):
    """测量指定电平脉冲；超时返回负数。"""
    try:
        return time_pulse_us(ir, level, timeout_us)
    except OSError:
        return -1

def read_nec():
    # NEC 起始信号：约 9ms 低电平 + 4.5ms 高电平
    start_low = pulse(0, 12000)
    if not 7000 <= start_low <= 11000:
        return None

    start_high = pulse(1, 7000)

    # 长按时的 NEC 重复码
    if 1800 <= start_high <= 2800:
        pulse(0, 1500)  # 读取重复码尾部脉冲
        return "REPEAT"

    if not 3500 <= start_high <= 5500:
        return None

    # 读取 32 位数据，NEC 协议先传低位
    value = 0
    for bit_index in range(32):
        low_time = pulse(0, 1500)
        high_time = pulse(1, 2500)

        if low_time < 0 or high_time < 0:
            return None

        if not 300 <= low_time <= 900:
            return None

        if 350 <= high_time <= 900:
            bit = 0
        elif 1200 <= high_time <= 2000:
            bit = 1
        else:
            return None

        value |= bit << bit_index

    # 检查命令字节及其反码
    address = value & 0xFF
    address2 = (value >> 8) & 0xFF
    command = (value >> 16) & 0xFF
    command_inverse = (value >> 24) & 0xFF

    if (command ^ command_inverse) != 0xFF:
        return None

    return address, address2, command

print("红外接收已启动：请对准接收头按遥控器。")

while True:
    result = read_nec()

    if result == "REPEAT":
        print("长按重复信号")
    elif result is not None:
        address, address2, command = result
        print("地址: 0x%02X 0x%02X，按键码: 0x%02X" %
              (address, address2, command))

    time.sleep_ms(20)