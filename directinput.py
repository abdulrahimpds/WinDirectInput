import cv2
import numpy as np
import ctypes
import mss
import time
import pyscreeze
import pyperclip

from ctypes import windll, wintypes, byref
from contextlib import contextmanager
from collections import namedtuple

# Define direct key codes for SendInput()
DK_CODE = {
    # Alphabets
    'a': 0x1E, 'A': 0x1E,
    'b': 0x30, 'B': 0x30,
    'c': 0x2E, 'C': 0x2E,
    'd': 0x20, 'D': 0x20,
    'e': 0x12, 'E': 0x12,
    'f': 0x21, 'F': 0x21,
    'g': 0x22, 'G': 0x22,
    'h': 0x23, 'H': 0x23,
    'i': 0x17, 'I': 0x17,
    'j': 0x24, 'J': 0x24,
    'k': 0x25, 'K': 0x25,
    'l': 0x26, 'L': 0x26,
    'm': 0x32, 'M': 0x32,
    'n': 0x31, 'N': 0x31,
    'o': 0x18, 'O': 0x18,
    'p': 0x19, 'P': 0x19,
    'q': 0x10, 'Q': 0x10,
    'r': 0x13, 'R': 0x13,
    's': 0x1F, 'S': 0x1F,
    't': 0x14, 'T': 0x14,
    'u': 0x16, 'U': 0x16,
    'v': 0x2F, 'V': 0x2F,
    'w': 0x11, 'W': 0x11,
    'x': 0x2D, 'X': 0x2D,
    'y': 0x15, 'Y': 0x15,
    'z': 0x2C, 'Z': 0x2C,
    # Numbers
    'num0': 0x52, '0': 0x0b, ')': 0x0b,
    'num1': 0x4F, '1': 0x02, '!': 0x02,
    'num2': 0x50, '2': 0x03, '@': 0x03,
    'num3': 0x51, '3': 0x04, '#': 0x04,
    'num4': 0x4B, '4': 0x05, '$': 0x05,
    'num5': 0x4C, '5': 0x06, '%': 0x06,
    'num6': 0x4D, '6': 0x07, '^': 0x07,
    'num7': 0x47, '7': 0x08, '&': 0x08,
    'num8': 0x48, '8': 0x09, '*': 0x09,
    'num9': 0x49, '9': 0x0a, '(': 0x0a,
    # Calculation keys
    'num/': 0xB5,
    'numdelete': 0x53,
    'num-': 0x4A,
    'num+': 0x4e,
    'num*': 0x37,
    # Arrow keys
    'up': 0xC8,
    'down': 0xD0,
    'left': 0xCB,
    'right': 0xCD,
    # Control keys
    'space': 0x39, ' ': 0x39,
    'esc': 0x01,
    'tab': 0x0F, '\t': 0x0F,
    'backspace': 0x0E, '\b': 0x0E,
    'enter': 0x1C, 'numenter': 0x9C, '\n': 0x1C, '\r': 0x1C,
    'shift': 0x2A, 'lshift': 0x2A, 'rshift': 0x36,
    'ctrl': 0x1D, 'lctrl': 0x1D, 'rctrl': 0x9D,
    'alt': 0x38, 'lalt': 0x38, 'ralt': 0xB8,
    'win': 0xDB, 'lwin': 0xDB, 'rwin': 0xDC,
    'apps': 0xDD,
    'capslock': 0x3A,
    'numlock': 0x45,
    'scrolllock': 0x46,
    'insert': 0xD2,
    'delete': 0xD3,
    'home': 0xC7,
    'end': 0xCF,
    'pageup': 0xC9,
    'pagedown': 0xD1,
    # Function keys
    'f1': 0x3B,
    'f2': 0x3C,
    'f3': 0x3D,
    'f4': 0x3E,
    'f5': 0x3F,
    'f6': 0x40,
    'f7': 0x41,
    'f8': 0x42,
    'f9': 0x43,
    'f10': 0x44,
    'f11': 0x57,
    'f12': 0x58,
    # Symbols
    '`': 0x29, '~': 0x29,
    '-': 0x0c, '_': 0x0c,
    '=': 0x0d, '+': 0x0d,
    '[': 0x1a, '{': 0x1a,
    ']': 0x1b, '}': 0x1b,
    '\\': 0x2b, '|': 0x2b,
    ';': 0x27, ':': 0x27,
    '\'': 0x28, '"': 0x28,
    ',': 0x33, '<': 0x33,
    '.': 0x34, '>': 0x34,
    '/': 0x35, '?': 0x35
}

# Define virtual key codes for GetAsyncKeyState()
VK_CODE = {
    # Alphabets
    'a': 0x41, 'A': 0x41,
    'b': 0x42, 'B': 0x42,
    'c': 0x43, 'C': 0x43,
    'd': 0x44, 'D': 0x44,
    'e': 0x45, 'E': 0x45,
    'f': 0x46, 'F': 0x46,
    'g': 0x47, 'G': 0x47,
    'h': 0x48, 'H': 0x48,
    'i': 0x49, 'I': 0x49,
    'j': 0x4A, 'J': 0x4A,
    'k': 0x4B, 'K': 0x4B,
    'l': 0x4C, 'L': 0x4C,
    'm': 0x4D, 'M': 0x4D,
    'n': 0x4E, 'N': 0x4E,
    'o': 0x4F, 'O': 0x4F,
    'p': 0x50, 'P': 0x50,
    'q': 0x51, 'Q': 0x51,
    'r': 0x52, 'R': 0x52,
    's': 0x53, 'S': 0x53,
    't': 0x54, 'T': 0x54,
    'u': 0x55, 'U': 0x55,
    'v': 0x56, 'V': 0x56,
    'w': 0x57, 'W': 0x57,
    'x': 0x58, 'X': 0x58,
    'y': 0x59, 'Y': 0x59,
    'z': 0x5A, 'Z': 0x5A,
    # Numbers
    'num0': 0x60, '0': 0x30, ')': 0x30,
    'num1': 0x61, '1': 0x31, '!': 0x31,
    'num2': 0x62, '2': 0x32, '@': 0x32,
    'num3': 0x63, '3': 0x33, '#': 0x33,
    'num4': 0x64, '4': 0x34, '$': 0x34,
    'num5': 0x65, '5': 0x35, '%': 0x35,
    'num6': 0x66, '6': 0x36, '^': 0x36,
    'num7': 0x67, '7': 0x37, '&': 0x37,
    'num8': 0x68, '8': 0x38, '*': 0x38,
    'num9': 0x69, '9': 0x39, '(': 0x39,
    # Calculation keys
    'num/': 0x6F,
    'numdelete': 0x6E,
    'num-': 0x6D,
    'num+': 0x6B,
    'num*': 0x6A,
    # Arrow keys
    'up': 0x26,
    'down': 0x28,
    'left': 0x25,
    'right': 0x27,
    # Control keys
    'space': 0x20, ' ': 0x20,
    'esc': 0x1B,
    'tab': 0x09, '\t': 0x09,
    'backspace': 0x08, '\b': 0x08,
    'enter': 0x0D, 'numenter': 0x0D, '\n': 0x0D, '\r': 0x0D,
    'shift': 0x10, 'lshift': 0x10, 'rshift': 0x10,
    'ctrl': 0x11, 'lctrl': 0x11, 'rctrl': 0x11,
    'alt': 0x12, 'lalt': 0x12, 'ralt': 0x12,
    'win': 0x5B, 'lwin': 0x5B, 'rwin': 0x5C,
    'apps': 0x5D,
    'capslock': 0x14,
    'numlock': 0x90,
    'scrolllock': 0x91,
    'insert': 0x2D,
    'delete': 0x2E,
    'home': 0x24,
    'end': 0x23,
    'pageup': 0x21,
    'pagedown': 0x22,
    # Function keys
    'f1': 0x70,
    'f2': 0x71,
    'f3': 0x72,
    'f4': 0x73,
    'f5': 0x74,
    'f6': 0x75,
    'f7': 0x76,
    'f8': 0x77,
    'f9': 0x78,
    'f10': 0x79,
    'f11': 0x7A,
    'f12': 0x7B,
    # Symbols
    '`': 0xC0, '~': 0xC0,
    '-': 0xBD, '_': 0xBD,
    '=': 0xBB, '+': 0xBB,
    '[': 0xDB, '{': 0xDB,
    ']': 0xDD, '}': 0xDD,
    '\\': 0xDC, '|': 0xDC,
    ';': 0xBA, ':': 0xBA,
    '\'': 0xDE, '"': 0xDE,
    ',': 0xBC, '<': 0xBC,
    '.': 0xBE, '>': 0xBE,
    '/': 0xBF, '?': 0xBF
}

# Define keys that requires shift to be pressed
shiftKeys = [
    ')', '!', '@', '#', '$', '%', '^', '&', '*', '(', '~', '_',
    '+', '{', '}', '|', ':', '"', '\n', '<', '>', '?',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
    'Y', 'Z',
    'home', 'pageup', 'pagedown', 'end', 'insert', 'numdelete',
    'up', 'down', 'left', 'right'
]

# Define virtual codes for mouse input
MB_CODE = {
    'left': 0x0002,
    'right': 0x0008,
    'middle': 0x0020
}

default_interval = 0.01
Point = namedtuple("Point", "x y")
Size = namedtuple("Size", "width height")

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# Keyboard Functions

def keyDown(*keys):
    # Get virtual key code
    virtual_key_codes = []
    for key in keys:
        try:
            hexKeyCode = DK_CODE[key.lower()]
        except Exception:
            hexKeyCode = 0x00
        virtual_key_codes.append(hexKeyCode)

    for hexKeyCode in virtual_key_codes:
        # Check if the character is in the shiftKeys list
        if key in shiftKeys:
            # Press the shift key
            ctypes.windll.user32.keybd_event(0x10, 0, 0, 0)

        # Press
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

        # Check if the character is in the shiftKeys list
        if key in shiftKeys:
            # Release the shift key
            ctypes.windll.user32.keybd_event(0x10, 0, 2, 0)


def keyUp(*keys):
    # Get virtual key code
    virtual_key_codes = []
    for key in keys:
        try:
            hexKeyCode = DK_CODE[key.lower()]
        except Exception:
            hexKeyCode = 0x00
        virtual_key_codes.append(hexKeyCode)

    for hexKeyCode in virtual_key_codes:
        # Check if the character is in the shiftKeys list
        if key in shiftKeys:
            # Press the shift key
            ctypes.windll.user32.keybd_event(0x10, 0, 0, 0)

        # Release
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(
            0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra)
        )
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

        # Check if the character is in the shiftKeys list
        if key in shiftKeys:
            # Release the shift key
            ctypes.windll.user32.keybd_event(0x10, 0, 2, 0)


@contextmanager
def keyHold(*keys):
    # Get the virtual key codes
    virtual_key_codes = []
    for key in keys:
        try:
            hexKeyCode = DK_CODE[key.lower()]
        except Exception:
            hexKeyCode = 0x00
        virtual_key_codes.append(hexKeyCode)

    for hexKeyCode in virtual_key_codes:
        # Press
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    # Yield control to the calling function
    yield

    for hexKeyCode in virtual_key_codes:
        # Release
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(
            0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra)
        )
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def keyPress(keys, interval=default_interval, presses=1, simultaneously=False):
    if not isinstance(keys, list):
        keys = [keys]

    if simultaneously:
        for _ in range(presses):
            press_inputs = []
            release_inputs = []

            for key in keys:
                # Get virtual key code
                try:
                    hexKeyCode = DK_CODE[key.lower()]
                except Exception:
                    hexKeyCode = 0x00

                # Check if the character is in the shiftKeys list
                if key in shiftKeys:
                    # Press the shift key
                    ctypes.windll.user32.keybd_event(0x10, 0, 0, 0)

                # Press
                extra = ctypes.c_ulong(0)
                ii_ = Input_I()
                ii_.ki = KeyBdInput(
                    0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra)
                )
                press_inputs.append(Input(ctypes.c_ulong(1), ii_))

                # Release
                extra = ctypes.c_ulong(0)
                ii_ = Input_I()
                ii_.ki = KeyBdInput(
                    0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra)
                )
                release_inputs.append(Input(ctypes.c_ulong(1), ii_))

                # Check if the character is in the shiftKeys list
                if key in shiftKeys:
                    # Release the shift key
                    ctypes.windll.user32.keybd_event(0x10, 0, 2, 0)

            press_inputs_array = (Input * len(keys))()
            for i, input_obj in enumerate(press_inputs):
                press_inputs_array[i] = input_obj
            ctypes.windll.user32.SendInput(
                len(keys), ctypes.pointer(press_inputs_array),
                ctypes.sizeof(Input)
            )

            time.sleep(interval)

            release_inputs_array = (Input * len(keys))()
            for i, input_obj in enumerate(release_inputs):
                release_inputs_array[i] = input_obj
            ctypes.windll.user32.SendInput(
                len(keys), ctypes.pointer(release_inputs_array),
                ctypes.sizeof(Input)
            )

    else:
        for _ in range(presses):
            for key in keys:
                # Get virtual key code
                try:
                    hexKeyCode = DK_CODE[key.lower()]
                except Exception:
                    hexKeyCode = 0x00

                # Check if the character is in the shiftKeys list
                if key in shiftKeys:
                    # Press the shift key
                    ctypes.windll.user32.keybd_event(0x10, 0, 0, 0)

                # Press
                extra = ctypes.c_ulong(0)
                ii_ = Input_I()
                ii_.ki = KeyBdInput(
                    0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra)
                )
                x = Input(ctypes.c_ulong(1), ii_)
                ctypes.windll.user32.SendInput(
                    1, ctypes.pointer(x), ctypes.sizeof(x)
                )

                time.sleep(interval)

                # Release
                extra = ctypes.c_ulong(0)
                ii_ = Input_I()
                ii_.ki = KeyBdInput(
                    0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra)
                )
                x = Input(ctypes.c_ulong(1), ii_)
                ctypes.windll.user32.SendInput(
                    1, ctypes.pointer(x), ctypes.sizeof(x)
                )

                # Check if the character is in the shiftKeys list
                if key in shiftKeys:
                    # Release the shift key
                    ctypes.windll.user32.keybd_event(0x10, 0, 2, 0)


def hotKey(*keys, interval=default_interval):
    # Get the virtual key codes for the keys in the hotkey sequence
    virtual_key_codes = []
    for key in keys:
        # Get virtual key code
        try:
            hexKeyCode = DK_CODE[key.lower()]
        except Exception:
            hexKeyCode = 0x00
        virtual_key_codes.append(hexKeyCode)

    # Press the keys in the hotkey sequence
    for hexKeyCode in virtual_key_codes:
        # Press
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

        time.sleep(interval)

    # Release the keys in reverse order
    for hexKeyCode in reversed(virtual_key_codes):
        # Release
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(
            0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra)
        )
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

        time.sleep(interval)


def write(text: str, speed=0.0, interval=0.03):
    # Load the user32 library
    user32 = ctypes.windll.user32

    # Iterate through each character in the text
    for c in text:
        # Look up the virtual key code for the character
        # in the VK_CODE dictionary
        try:
            vk_code = VK_CODE[c]
        except Exception:
            # If the character isn't in the VK_CODE,
            # copy it to the clipboard and simulate a paste operation
            pyperclip.copy(c)
            hotKey('ctrl', 'v', interval=interval)
        else:
            # Check if the character is in the shiftKeys list
            if c in shiftKeys:
                # Press the shift key
                user32.keybd_event(0x10, 0, 0, 0)

            # Send a WM_KEYDOWN message for the key
            # corresponding to the virtual key code
            user32.keybd_event(vk_code, 0, 0, 0)

            time.sleep(interval)

            # Send a WM_KEYUP message for the key
            # corresponding to the virtual key code
            user32.keybd_event(vk_code, 0, 2, 0)

            # Check if the character is in the shiftKeys list
            if c in shiftKeys:
                # Release the shift key
                user32.keybd_event(0x10, 0, 2, 0)

        # Define the time delay between each characters
        time.sleep(speed)


def keyDetect(keys):
    # Check if keys is a single key (string) and convert it to a list
    if isinstance(keys, str):
        keys = [keys]

    # Check the state of each key in the list
    for key in keys:
        key_code = VK_CODE.get(key.lower(), None)
        if key_code is None:
            # Handle the case where the key is not recognized
            print(f"Warning: Key '{key}' not recognized.")
            return False

        key_state = ctypes.windll.user32.GetAsyncKeyState(key_code)
        if key_state <= 1:
            # If any key is not pressed, return False
            return False

    # If all keys are pressed, return True
    return True


# Mouse Functions

def mouseClick(button='left', interval=default_interval, presses=1):
    button_code = MB_CODE.get(button.lower())
    for _ in range(presses):
        # Send mouse button press event
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(0, 0, 0, button_code, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

        time.sleep(interval)

        # Send mouse button release event
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(
            0, 0, 0, button_code << 1, 0, ctypes.pointer(extra)
        )
        x = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def mouseDown(button='left'):
    button_code = MB_CODE.get(button.lower())
    # Send mouse button press event
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, button_code, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def mouseUp(button='left'):
    button_code = MB_CODE.get(button.lower())
    # Send mouse button release event
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, button_code << 1, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


@contextmanager
def mouseHold(button='left'):
    button_code = MB_CODE.get(button.lower())

    # Send mouse button press event
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, button_code, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    # Yield control to the calling function
    yield

    # Send mouse button release event
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, button_code << 1, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def moveMouseTo(x=None, y=None, duration=0.0):
    # Get the current mouse position
    current_x, current_y = getMousePosition()

    if x is None:
        x = current_x
    else:
        x = int(x)

    if y is None:
        y = current_y
    else:
        y = int(y)

    # Calculate the distance to move the cursor in the x and y direction
    distance_x = x - current_x
    distance_y = y - current_y

    # Calculate the number of steps needed to move the cursor
    # based on the duration and the distance to travel
    steps = int(duration * 50)
    if steps == 0:
        ctypes.windll.user32.SetCursorPos(x, y)
        return

    step_x = distance_x / steps
    step_y = distance_y / steps

    # Move the cursor in a linear way over the specified duration
    for i in range(steps):
        time.sleep(duration / steps)
        current_x += step_x
        current_y += step_y
        ctypes.windll.user32.SetCursorPos(int(current_x), int(current_y))


def moveMouse(xOffset=0, yOffset=0, duration=0.0):
    current_x, current_y = getMousePosition()
    x = current_x + xOffset
    y = current_y + yOffset

    distance_x = x - current_x
    distance_y = y - current_y
    steps = int(duration * 50)
    if steps == 0:
        ctypes.windll.user32.SetCursorPos(x, y)
        return

    step_x = distance_x / steps
    step_y = distance_y / steps

    for i in range(steps):
        time.sleep(duration / steps)
        current_x += step_x
        current_y += step_y
        ctypes.windll.user32.SetCursorPos(int(current_x), int(current_y))


def scrollMouse(clicks):
    if clicks != 0:
        ctypes.windll.user32.mouse_event(0x0800, 0, 0, clicks, 0)


# Other Functions

def screenshot(filename=None, region=None):
    if region:
        img = pyscreeze.screenshot(region=region)
    else:
        img = pyscreeze.screenshot()

    if filename:
        img.save(filename)

    return img


def getMousePosition():
    cursor = wintypes.POINT()
    windll.user32.GetCursorPos(byref(cursor))
    return Point(cursor.x, cursor.y)


def getDisplaySize():
    user32 = ctypes.windll.user32
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    return Size(width, height)


def locateImage(needleImage, haystackImage=None, grayscale=False,
                region=None, threshold=0.999):
    needleImage = cv2.imread(needleImage)
    if haystackImage is None:
        # Take a screenshot of the entire screen
        with mss.mss() as sct:
            haystackImage = np.array(sct.grab(sct.monitors[1]))
    else:
        haystackImage = cv2.imread(haystackImage)

    if grayscale:
        needleImage = cv2.cvtColor(needleImage, cv2.COLOR_BGR2GRAY)
        haystackImage = cv2.cvtColor(haystackImage, cv2.COLOR_BGR2GRAY)
    else:
        needleImage = cv2.cvtColor(needleImage, cv2.COLOR_BGR2RGB)
        haystackImage = cv2.cvtColor(haystackImage, cv2.COLOR_BGR2RGB)
    # Find the image
    coords = pyscreeze.locate(needleImage, haystackImage,
                              region=region, confidence=threshold)
    if coords is None:
        return None
    else:
        # Return the center coordinates of the image
        center_x, center_y = coords[0] + coords[2]/2, coords[1] + coords[3]/2
        return Point(center_x, center_y)
