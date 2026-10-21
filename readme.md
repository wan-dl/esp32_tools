## esp资源

固件下载地址：https://micropython.org/download/ESP32_GENERIC/

## 擦除 flash

```shell
esptool --chip esp32 --port COM3 erase-flash
```

```powershell
PS D:\> esptool --chip esp32 --port COM3 erase_flash
WARNING: Deprecated: Command 'erase_flash' is deprecated. Use 'erase-flash' instead.
esptool v5.5.0
Connected to ESP32 on COM3:
Chip type:          ESP32-D0WD-V3 (revision v3.1)
Features:           Wi-Fi, BT, Dual Core + LP Core, 240MHz, Vref calibration in eFuse, Coding Scheme None
Crystal frequency:  40MHz
MAC:                48:9d:31:01:a9:bc

Stub flasher running.

Flash memory erased successfully in 4.8 seconds.

Hard resetting via RTS pin.
```

## 刷入固件

```shell
esptool --chip esp32 --port COM3 --baud 115200 write_flash -z 0x1000 ESP32_GENERIC-20260824-v1.29.0.bin
```

```
D:\_project\tmp\esp32>esptool --chip esp32 --port COM3 --baud 115200 write_flash -z 0x1000 ESP32_GENERIC-20260824-v1.29.0.bin
WARNING: Deprecated: Command 'write_flash' is deprecated. Use 'write-flash' instead.
esptool v5.5.0
Connected to ESP32 on COM3:
Chip type:          ESP32-D0WD-V3 (revision v3.1)
Features:           Wi-Fi, BT, Dual Core + LP Core, 240MHz, Vref calibration in eFuse, Coding Scheme None
Crystal frequency:  40MHz
MAC:                48:9d:31:01:a9:bc

Stub flasher running.

Configuring flash size...
Flash will be erased from 0x00001000 to 0x001b6fff...
Wrote 1790544 bytes (1167582 compressed) at 0x00001000 in 104.6 seconds (137.0 kbit/s).
Hash of data verified.

Hard resetting via RTS pin...
```

## python

上传代码和运行

```shell
pip install esptool mpremote

# 确认 COM3 是 ESP32
python -m serial.tools.list_ports

# 连接 REPL
mpremote connect COM3 repl

# 同步
mpremote cp main.py :main.py
```

## py 示例代码1

```py
from machine import Pin
from time import sleep

for pin_num in [2, 4, 5, 12, 13, 15, 21, 22]:
    try:
        led = Pin(pin_num, Pin.OUT)
        print("testing", pin_num)
        led.value(1)
        sleep(0.3)
        led.value(0)
        sleep(0.3)
    except Exception as e:
        print(pin_num, e)
```

## py 示例代码2

```
```