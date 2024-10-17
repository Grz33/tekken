import pyautogui
import random
import time

from .keys import *

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

down_arrow_key = 0x53  # S key
left_arrow_key = 0x41  # A key
right_arrow_key = 0x44  # D key
cross = 0x45  # E key
square = 0x52  # R key
circle = 0x54  # T key
triangle = 0x59  # Y key
R1 = 0x51  # Q key
TOUCHPAD = 0x58  # X keya
OPTIONS = 0x58  # F3 key
up_arrow_key = 0x45  # W GORE key

down_left = (left_arrow_key, down_arrow_key)
down_right = (right_arrow_key, down_arrow_key)
up_left = (left_arrow_key, up_arrow_key)
right_up = (right_arrow_key, up_arrow_key)

cross_square = (cross, square)
cross_circle = (cross, circle)
triangle_circle = (triangle, circle)
square_triangle = (square, triangle)

attack = [0, triangle, circle, cross, square, down_left, cross_square, down_right, cross_circle, triangle_circle]

direction = [0, up_arrow_key, down_arrow_key, left_arrow_key, right_arrow_key, down_right, down_left,
             up_left, right_up]

valid_actions = [(x, y) for x in attack for y in direction]


def quick_press_delay():
    time.sleep(random.uniform(0.05, 0.07))


def get_actions(amount):
    actions = [[]]

    for i in range(amount):
        move_or_fight = random.randint(0, 1)

        if move_or_fight == 0:
            action = direction[random.randint(0, len(direction) - 1)]
        else:
            action = attack[random.randint(0, len(direction) - 1)]

        if action != 0:
            actions.append(action)

    return actions


def get_action(index):
    print(valid_actions[index])
    return valid_actions[index]


def press_key(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def release_key(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def delay():
    time.sleep(random.uniform(0.1, 0.3))


def execute(actionIndex):
    action = valid_actions[actionIndex]
    # patzy czy 1 elemnt listy krotka jest
    if isinstance(action[0], tuple):
        if action[0][0] != 0:
            press_key(action[0][0])
            quick_press_delay()

        if action[0][1] != 0:
            press_key(action[0][1])
            quick_press_delay()
    else:
        if action[0] != 0:
            press_key(action[0])
            quick_press_delay()

    if isinstance(action[1], tuple):
        if action[1][0] != 0:
            press_key(action[1][0])
            quick_press_delay()

        if action[1][1] != 0:
            press_key(action[1][1])
            quick_press_delay()

    else:
        if action[1] != 0:
            press_key(action[1])
            quick_press_delay()

    if isinstance(action[0], tuple):
        if action[0][0] != 0:
            release_key(action[0][0])

        if action[0][1] != 0:
            release_key(action[0][1])
    else:
        if action[0] != 0:
            release_key(action[0])
            quick_press_delay()
    if isinstance(action[1], tuple):
        if action[1][0] != 0:
            release_key(action[1][0])
        if action[1][1] != 0:
            release_key(action[1][1])
    else:
        if action[1] != 0:
            release_key(action[1])


def reset_players():
    pyautogui.press('x')
