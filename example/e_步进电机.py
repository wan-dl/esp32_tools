from machine import Pin
from time import sleep_ms, ticks_ms, ticks_diff

# ULN2003 的 IN1、IN2、IN3、IN4
MOTOR_PINS = [15, 2, 0, 4]

# 按键：正转/停止、反转/停止、加速、减速
KEY_PINS = [14, 27, 26, 25]

motor = [Pin(pin, Pin.OUT) for pin in MOTOR_PINS]
keys = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in KEY_PINS]

sequence = (
    (1, 0, 0, 0),
    (1, 1, 0, 0),
    (0, 1, 0, 0),
    (0, 1, 1, 0),
    (0, 0, 1, 0),
    (0, 0, 1, 1),
    (0, 0, 0, 1),
    (1, 0, 0, 1),
)

step_index = 0
step_delay = 5
MIN_DELAY = 2
MAX_DELAY = 20

# direction: 0=停止，1=正转，-1=反转
direction = 0

# 按键消抖状态
raw_last = [key.value() for key in keys]
stable_state = raw_last[:]
changed_at = [ticks_ms()] * len(keys)
DEBOUNCE_MS = 30

last_step_at = ticks_ms()

def release_motor():
    for pin in motor:
        pin.value(0)

def do_step(direction):
    global step_index

    step_index = (step_index + direction) % len(sequence)
    for pin, value in zip(motor, sequence[step_index]):
        pin.value(value)

print("GPIO14：按一下持续正转，再按停止")
print("GPIO27：按一下持续反转，再按停止")
print("GPIO26：加速；GPIO25：减速")

while True:
    now = ticks_ms()

    # 读取按键并消抖；按下时为 0
    for i, key in enumerate(keys):
        raw = key.value()

        if raw != raw_last[i]:
            raw_last[i] = raw
            changed_at[i] = now

        elif raw != stable_state[i] and ticks_diff(now, changed_at[i]) >= DEBOUNCE_MS:
            stable_state[i] = raw

            # 只在确认按下时执行一次
            if stable_state[i] == 0:
                if i == 0:
                    direction = 0 if direction == 1 else 1
                    print("正转" if direction == 1 else "停止")

                elif i == 1:
                    direction = 0 if direction == -1 else -1
                    print("反转" if direction == -1 else "停止")

                elif i == 2:
                    old_delay = step_delay
                    step_delay = max(MIN_DELAY, step_delay - 1)
                    print("加速，间隔:", step_delay, "ms" if step_delay != old_delay else "（已最快）")

                elif i == 3:
                    old_delay = step_delay
                    step_delay = min(MAX_DELAY, step_delay + 1)
                    print("减速，间隔:", step_delay, "ms" if step_delay != old_delay else "（已最慢）")

    # 持续转动，不需要一直按住
    if direction != 0 and ticks_diff(now, last_step_at) >= step_delay:
        do_step(direction)
        last_step_at = now
    elif direction == 0:
        release_motor()

    sleep_ms(1)