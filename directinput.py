"""
This module provides direct input control functions for simulating keyboard
and mouse events on Windows. It is useful for automated testing, creating
macros, and other applications requiring simulated user input.
"""

import ctypes
import mss
import pyscreeze
import pyperclip
import threading
import time
import os

from time import sleep
from collections import namedtuple
from contextlib import contextmanager
from ctypes import windll, wintypes, byref
from numpy import array
from cv2 import imread, cvtColor, COLOR_BGR2GRAY, COLOR_BGR2RGB

# Constants
DEFAULT_INTERVAL = 0.01
Point = namedtuple("Point", "x y")
Size = namedtuple("Size", "width height")

# KeyBdInput Flags
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_UNICODE = 0x0004

# MapVirtualKey Map Types
MapVirtualKey = ctypes.windll.user32.MapVirtualKeyW

MAPVK_VK_TO_CHAR = 2
MAPVK_VK_TO_VSC = 0
MAPVK_VSC_TO_VK = 1
MAPVK_VSC_TO_VK_EX = 3

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
    'num/': MapVirtualKey(0x6F, MAPVK_VK_TO_VSC),
    'num.': 0x53,
    'num-': 0x4A,
    'num+': 0x4e,
    'num*': 0x37,
    # Arrow keys
    'up': MapVirtualKey(0x26, MAPVK_VK_TO_VSC),
    'left': MapVirtualKey(0x25, MAPVK_VK_TO_VSC),
    'down': MapVirtualKey(0x28, MAPVK_VK_TO_VSC),
    'right': MapVirtualKey(0x27, MAPVK_VK_TO_VSC),
    # Control keys
    'space': 0x39, ' ': 0x39,
    'esc': 0x01,
    'tab': 0x0F, '\t': 0x0F,
    'backspace': 0x0E, '\b': 0x0E,
    'enter': 0x1C, 'numenter': MapVirtualKey(0x0D, MAPVK_VK_TO_VSC), '\n': 0x1C, '\r': 0x1C,
    'shift': 0x2A, 'lshift': 0x2A, 'rshift': 0x36,
    'ctrl': 0x1D, 'lctrl': 0x1D, 'rctrl': MapVirtualKey(0x11, MAPVK_VK_TO_VSC),
    'alt': 0x38, 'lalt': 0x38, 'ralt': MapVirtualKey(0x12, MAPVK_VK_TO_VSC),
    'win': MapVirtualKey(0x5B, MAPVK_VK_TO_VSC), 'lwin': MapVirtualKey(0x5B, MAPVK_VK_TO_VSC), 'rwin': MapVirtualKey(0x5C, MAPVK_VK_TO_VSC),
    'apps': 0xDD,
    'capslock': 0x3A,
    'numlock': 0x45,
    'scrolllock': 0x46,
    'insert': MapVirtualKey(0x2D, MAPVK_VK_TO_VSC),
    'delete': MapVirtualKey(0x2E, MAPVK_VK_TO_VSC),
    'home': MapVirtualKey(0x24, MAPVK_VK_TO_VSC),
    'end': MapVirtualKey(0x23, MAPVK_VK_TO_VSC),
    'pageup': MapVirtualKey(0x21, MAPVK_VK_TO_VSC),
    'pagedown': MapVirtualKey(0x22, MAPVK_VK_TO_VSC),
    'prtsc': MapVirtualKey(0x6A, MAPVK_VK_TO_VSC), 'sysrq': MapVirtualKey(0x6A, MAPVK_VK_TO_VSC),
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
    'num.': 0x6E,
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
    'prtsc': 0x2C, 'sysrq': 0x2C,
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
SHIFT_KEYS = [
    ')', '!', '@', '#', '$', '%', '^', '&', '*', '(', '~', '_',
    '+', '{', '}', '|', ':', '"', '\n', '<', '>', '?',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
    'Y', 'Z'
]

EXTENDED_KEYS = [
    'up', 'down', 'left', 'right', 'numenter', 'num/',
    'home', 'end', 'delete', 'insert', 'pageup', 'pagedown',
    'prtsc', 'sysrq', 'ralt', 'rctrl', 'win', 'rwin', 'lwin'
]

# Define direct codes for mouse input (for SendInput)
MB_CODE = {
    'left': 0x0002,
    'right': 0x0008,
    'middle': 0x0020
}

# Define virtual codes for mouse detection
MVB_CODE = {
    'left_mouse': 0x01,
    'right_mouse': 0x02,
    'middle_mouse': 0x04,
    'xbutton1': 0x05,
    'xbutton2': 0x06
}

# Define mouse_event flags
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_XDOWN = 0x0080
MOUSEEVENTF_XUP = 0x0100

# Define mouse data values for xbuttons (for mouse_event)
XBUTTON_DATA = {
    'xbutton1': 0x0001,
    'xbutton2': 0x0002
}

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
    """
    Simulate pressing down one or more keys.

    Parameters:
    *keys : str
        One or more keys to press down. The key names should correspond to
        the key mappings.

    Example:
    keyDown('x', 'y') or keyDown('a')
    """

    # Get virtual key code
    virtual_key_codes = []
    for key in keys:
        try:
            hexKeyCode = DK_CODE[key.lower()]
        except Exception:
            hexKeyCode = 0x00
        virtual_key_codes.append((key.lower(), hexKeyCode))

    for key, hexKeyCode in virtual_key_codes:
        keybdFlags = KEYEVENTF_SCANCODE

        # Check if the character is in the shiftKeys list
        if key in SHIFT_KEYS:
            # Press the shift key
            ctypes.windll.user32.keybd_event(0x10, 0, 0, 0)

        # Check if the key is an arrow key and set the extended key flag
        if key in EXTENDED_KEYS:
            keybdFlags |= KEYEVENTF_EXTENDEDKEY
            # Handle Num Lock state for arrow keys
            if ctypes.windll.user32.GetKeyState(0x90):
                # Send additional scancode if Num Lock is on
                extra = ctypes.c_ulong(0)
                ii_ = Input_I()
                ii_.ki = KeyBdInput(
                    0, 0xE0, KEYEVENTF_SCANCODE, 0, ctypes.pointer(extra)
                )
                x = Input(ctypes.c_ulong(1), ii_)
                ctypes.windll.user32.SendInput(
                    1, ctypes.pointer(x), ctypes.sizeof(x)
                )

        # Press the key
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(
            0, hexKeyCode, keybdFlags, 0, ctypes.pointer(extra)
        )
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(
            1, ctypes.pointer(x), ctypes.sizeof(x)
        )

        # Check if the character is in the shiftKeys list
        if key in SHIFT_KEYS:
            # Release the shift key
            ctypes.windll.user32.keybd_event(0x10, 0, 2, 0)


def keyUp(*keys):
    """
    Simulate releasing one or more keys.

    Parameters:
    *keys : str
        One or more keys to release. The key names should correspond to
        the key mappings.

    Example:
    keyUp('x', 'y') or keyUp('a')
    """

    # Get virtual key code
    virtual_key_codes = []
    for key in keys:
        try:
            hexKeyCode = DK_CODE[key.lower()]
        except Exception:
            hexKeyCode = 0x00
        virtual_key_codes.append((key.lower(), hexKeyCode))

    for key, hexKeyCode in virtual_key_codes:
        keybdFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP

        # Check if the character is in the shiftKeys list
        if key in SHIFT_KEYS:
            # Press the shift key
            ctypes.windll.user32.keybd_event(0x10, 0, 0, 0)

        # Check if the key is an arrow key and set the extended key flag
        if key in EXTENDED_KEYS:
            keybdFlags |= KEYEVENTF_EXTENDEDKEY
            # Handle Num Lock state for arrow keys
            if ctypes.windll.user32.GetKeyState(0x90):
                # Send additional scancode if Num Lock is on
                extra = ctypes.c_ulong(0)
                ii_ = Input_I()
                ii_.ki = KeyBdInput(
                    0, 0xE0, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0,
                    ctypes.pointer(extra)
                )
                x = Input(ctypes.c_ulong(1), ii_)
                ctypes.windll.user32.SendInput(
                    1, ctypes.pointer(x), ctypes.sizeof(x)
                )

        # Release the key
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(
            0, hexKeyCode, keybdFlags, 0, ctypes.pointer(extra)
        )
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(
            1, ctypes.pointer(x), ctypes.sizeof(x)
        )

        # Check if the character is in the shiftKeys list
        if key in SHIFT_KEYS:
            # Release the shift key
            ctypes.windll.user32.keybd_event(0x10, 0, 2, 0)


@contextmanager
def keyHold(*keys):
    """
    Simulate holding down one or more specified keys.

    This function simulates pressing and holding one or more specified keys.
    The keys parameter should be a string, not a list. This function should be
    used with a `with` statement to ensure that the keys are released after the
    block of code is executed.

    Parameters:
    *keys : str
        One or more keys to hold down. The key names should correspond to
        the key mappings.

    Example:
    with keyHold('ctrl', 'shift'):
        keyPress('esc')
    """

    # Get the virtual key codes
    virtual_key_codes = []
    for key in keys:
        try:
            hexKeyCode = DK_CODE[key.lower()]
        except Exception:
            hexKeyCode = 0x00
        virtual_key_codes.append((key.lower(), hexKeyCode))

    for key, hexKeyCode in virtual_key_codes:
        keybdFlags = KEYEVENTF_SCANCODE

        # Check if the key is an arrow key and set the extended key flag
        if key in EXTENDED_KEYS:
            keybdFlags |= KEYEVENTF_EXTENDEDKEY
            # Handle Num Lock state for arrow keys
            if ctypes.windll.user32.GetKeyState(0x90):
                # Send additional scancode if Num Lock is on
                extra = ctypes.c_ulong(0)
                ii_ = Input_I()
                ii_.ki = KeyBdInput(
                    0, 0xE0, KEYEVENTF_SCANCODE, 0, ctypes.pointer(extra)
                )
                x = Input(ctypes.c_ulong(1), ii_)
                ctypes.windll.user32.SendInput(
                    1, ctypes.pointer(x), ctypes.sizeof(x)
                )

        # Press the key
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(
            0, hexKeyCode, keybdFlags, 0, ctypes.pointer(extra)
        )
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(
            1, ctypes.pointer(x), ctypes.sizeof(x)
        )

    # Yield control to the calling function
    yield

    for key, hexKeyCode in virtual_key_codes:
        keybdFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP

        # Check if the key is an arrow key and set the extended key flag
        if key in EXTENDED_KEYS:
            keybdFlags |= KEYEVENTF_EXTENDEDKEY
            # Handle Num Lock state for arrow keys
            if ctypes.windll.user32.GetKeyState(0x90):
                # Send additional scancode if Num Lock is on
                extra = ctypes.c_ulong(0)
                ii_ = Input_I()
                ii_.ki = KeyBdInput(
                    0, 0xE0, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0,
                    ctypes.pointer(extra)
                )
                x = Input(ctypes.c_ulong(1), ii_)
                ctypes.windll.user32.SendInput(
                    1, ctypes.pointer(x), ctypes.sizeof(x)
                )

        # Release the key
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(
            0, hexKeyCode, keybdFlags, 0, ctypes.pointer(extra)
        )
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(
            1, ctypes.pointer(x), ctypes.sizeof(x)
        )


def keyPress(keys, interval=0, presses=1,
             key_delay=DEFAULT_INTERVAL, simultaneously=False):
    """
    Simulate pressing one or more keys.

    This function simulates pressing and releasing one or more specified keys.
    The keys parameter can be a single key or a list of keys. The keys can be
    pressed either simultaneously or sequentially based on the
    `simultaneously` parameter. Additionally, the function allows specifying
    the number of times to press the keys and the interval between presses.

    Parameters:
    keys : str or list of str
        The key or list of keys to press. The key names should correspond to
        the key mappings.
    interval : float, optional
        The interval between key presses in seconds (default is 0.01).
    presses : int, optional
        The number of times to press the keys (default is 1).
    key_delay : float, optional
        The delay between each key press and release in seconds (default is 0.01).
    simultaneously : bool, optional
        Whether to press all keys at once (default is False).
        If False, keys are pressed sequentially.

    Example:
    keyPress('a')                                      # Press the 'a' key once.
    keyPress(['ctrl', 'c'])                            # Press 'ctrl' and 'c' sequentially.
    keyPress(['ctrl', 'shift'], simultaneously=True)   # Press 'ctrl' and 'shift' simultaneously.
    keyPress('b', presses=3, interval=0.5)             # Press the 'b' key 3 times with 0.5-second interval.
    """

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

                keybdFlags = KEYEVENTF_SCANCODE

                # Check if the character is in the shiftKeys list
                if key in SHIFT_KEYS:
                    # Press the shift key
                    ctypes.windll.user32.keybd_event(0x10, 0, 0, 0)

                # Check if the key is an arrow key and set the extended key flag
                if key in EXTENDED_KEYS:
                    keybdFlags |= KEYEVENTF_EXTENDEDKEY
                    # Handle Num Lock state for arrow keys
                    if ctypes.windll.user32.GetKeyState(0x90):
                        # Send additional scancode if Num Lock is on
                        extra = ctypes.c_ulong(0)
                        ii_ = Input_I()
                        ii_.ki = KeyBdInput(
                            0, 0xE0, KEYEVENTF_SCANCODE, 0, ctypes.pointer(extra)
                        )
                        x = Input(ctypes.c_ulong(1), ii_)
                        ctypes.windll.user32.SendInput(
                            1, ctypes.pointer(x), ctypes.sizeof(x)
                        )

                # Press
                extra = ctypes.c_ulong(0)
                ii_ = Input_I()
                ii_.ki = KeyBdInput(
                    0, hexKeyCode, keybdFlags, 0, ctypes.pointer(extra)
                )
                press_inputs.append(Input(ctypes.c_ulong(1), ii_))

                # Release
                extra = ctypes.c_ulong(0)
                ii_ = Input_I()
                ii_.ki = KeyBdInput(
                    0, hexKeyCode, keybdFlags | KEYEVENTF_KEYUP, 0,
                    ctypes.pointer(extra)
                )
                release_inputs.append(Input(ctypes.c_ulong(1), ii_))

                # Check if the character is in the shiftKeys list
                if key in SHIFT_KEYS:
                    # Release the shift key
                    ctypes.windll.user32.keybd_event(0x10, 0, 2, 0)

            press_inputs_array = (Input * len(keys))()
            for i, input_obj in enumerate(press_inputs):
                press_inputs_array[i] = input_obj
            ctypes.windll.user32.SendInput(
                len(keys), ctypes.pointer(press_inputs_array),
                ctypes.sizeof(Input)
            )

            sleep(key_delay)

            release_inputs_array = (Input * len(keys))()
            for i, input_obj in enumerate(release_inputs):
                release_inputs_array[i] = input_obj
            ctypes.windll.user32.SendInput(
                len(keys), ctypes.pointer(release_inputs_array),
                ctypes.sizeof(Input)
            )

            sleep(interval)

    else:
        for _ in range(presses):
            for key in keys:
                # Get virtual key code
                try:
                    hexKeyCode = DK_CODE[key.lower()]
                except Exception:
                    hexKeyCode = 0x00

                keybdFlags = KEYEVENTF_SCANCODE

                # Check if the character is in the shiftKeys list
                if key in SHIFT_KEYS:
                    # Press the shift key
                    ctypes.windll.user32.keybd_event(0x10, 0, 0, 0)

                # Check if the key is an arrow key and set the extended key flag
                if key in EXTENDED_KEYS:
                    keybdFlags |= KEYEVENTF_EXTENDEDKEY
                    # Handle Num Lock state for arrow keys
                    if ctypes.windll.user32.GetKeyState(0x90):
                        # Send additional scancode if Num Lock is on
                        extra = ctypes.c_ulong(0)
                        ii_ = Input_I()
                        ii_.ki = KeyBdInput(
                            0, 0xE0, KEYEVENTF_SCANCODE, 0, ctypes.pointer(extra)
                        )
                        x = Input(ctypes.c_ulong(1), ii_)
                        ctypes.windll.user32.SendInput(
                            1, ctypes.pointer(x), ctypes.sizeof(x)
                        )

                # Press
                extra = ctypes.c_ulong(0)
                ii_ = Input_I()
                ii_.ki = KeyBdInput(
                    0, hexKeyCode, keybdFlags, 0, ctypes.pointer(extra)
                )
                x = Input(ctypes.c_ulong(1), ii_)
                ctypes.windll.user32.SendInput(
                    1, ctypes.pointer(x), ctypes.sizeof(x)
                )

                sleep(key_delay)

                # Release
                extra = ctypes.c_ulong(0)
                ii_ = Input_I()
                ii_.ki = KeyBdInput(
                    0, hexKeyCode, keybdFlags | KEYEVENTF_KEYUP, 0, ctypes.pointer(extra)
                )
                x = Input(ctypes.c_ulong(1), ii_)
                ctypes.windll.user32.SendInput(
                    1, ctypes.pointer(x), ctypes.sizeof(x)
                )

                # Check if the character is in the shiftKeys list
                if key in SHIFT_KEYS:
                    # Release the shift key
                    ctypes.windll.user32.keybd_event(0x10, 0, 2, 0)

                sleep(interval)


def hotKey(*keys, **kwargs):
    """
    Simulate pressing a combination of keys simultaneously.

    This function simulates pressing and holding down a combination of keys simultaneously,
    followed by releasing them.
    The keys parameter can accept multiple key arguments to form the hotkey combination.

    Parameters:
    *keys : str
        One or more keys to press as part of the hotkey combination.
        The key names should correspond to
        the key mappings.
    key_delay : float, optional
        The delay between each key press and release in seconds (default is 0.01).

    Example:
    hotKey('ctrl', 'shift', 'esc')  # Simulate pressing 'Ctrl + Shift + Esc' simultaneously.
    """
    key_delay = kwargs.get('key_delay', DEFAULT_INTERVAL)

    # Get the virtual key codes for the keys in the hotkey sequence
    virtual_key_codes = []
    for key in keys:
        # Get virtual key code
        try:
            hexKeyCode = DK_CODE[key.lower()]
        except Exception:
            hexKeyCode = 0x00
        virtual_key_codes.append((key.lower(), hexKeyCode))

    # Press the keys in the hotkey sequence
    for key, hexKeyCode in virtual_key_codes:
        keybdFlags = KEYEVENTF_SCANCODE

        # Check if the key is an arrow key and set the extended key flag
        if key in EXTENDED_KEYS:
            keybdFlags |= KEYEVENTF_EXTENDEDKEY
            # Handle Num Lock state for arrow keys
            if ctypes.windll.user32.GetKeyState(0x90):
                # Send additional scancode if Num Lock is on
                extra = ctypes.c_ulong(0)
                ii_ = Input_I()
                ii_.ki = KeyBdInput(
                    0, 0xE0, KEYEVENTF_SCANCODE, 0, ctypes.pointer(extra)
                )
                x = Input(ctypes.c_ulong(1), ii_)
                ctypes.windll.user32.SendInput(
                    1, ctypes.pointer(x), ctypes.sizeof(x)
                )

        # Press
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(
            0, hexKeyCode, keybdFlags, 0, ctypes.pointer(extra)
        )
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(
            1, ctypes.pointer(x), ctypes.sizeof(x)
        )

        sleep(key_delay)

    # Release the keys in reverse order
    for key, hexKeyCode in reversed(virtual_key_codes):
        keybdFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP

        # Check if the key is an arrow key and set the extended key flag
        if key in EXTENDED_KEYS:
            keybdFlags |= KEYEVENTF_EXTENDEDKEY
            # Handle Num Lock state for arrow keys
            if ctypes.windll.user32.GetKeyState(0x90):
                # Send additional scancode if Num Lock is on
                extra = ctypes.c_ulong(0)
                ii_ = Input_I()
                ii_.ki = KeyBdInput(
                    0, 0xE0, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0,
                    ctypes.pointer(extra)
                )
                x = Input(ctypes.c_ulong(1), ii_)
                ctypes.windll.user32.SendInput(
                    1, ctypes.pointer(x), ctypes.sizeof(x)
                )

        # Release
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(
            0, hexKeyCode, keybdFlags, 0, ctypes.pointer(extra)
        )
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(
            1, ctypes.pointer(x), ctypes.sizeof(x)
        )

        sleep(key_delay)


def write(text: str, interval=0.0, key_delay=0.03):
    """
    Types out a given text string.

    This function simulates typing out a given text string character by character.
    Optionally, a speed (in seconds) between key presses can be specified to
    simulate a more natural typing speed. If a character is not recognized,
    it will be copied and pasted from the clipboard.

    Parameters:
    text : str
        The text string to type out.
    interval : float, optional
        The interval (in seconds) between each character (default is 0.0).
    key_delay : float, optional
        The delay between key press and release for each character (default is 0.03 seconds).

    Example:
    write("Hello, World!", interval=0.1)
    """

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
            hotKey('ctrl', 'v', interval=key_delay)
        else:
            # Check if the character is in the shiftKeys list
            if c in SHIFT_KEYS:
                # Press the shift key
                user32.keybd_event(0x10, 0, 0, 0)

            # Send a WM_KEYDOWN message for the key
            # corresponding to the virtual key code
            user32.keybd_event(vk_code, 0, 0, 0)

            sleep(key_delay)

            # Send a WM_KEYUP message for the key
            # corresponding to the virtual key code
            user32.keybd_event(vk_code, 0, 2, 0)

            # Check if the character is in the shiftKeys list
            if c in SHIFT_KEYS:
                # Release the shift key
                user32.keybd_event(0x10, 0, 2, 0)

        # Define the time delay between each characters
        sleep(interval)


def keyDetect(*keys):
    """
    Check if one or more specified keys are currently pressed.

    This function checks the state of one or more specified keys to determine
    if they are currently pressed. The keys parameter can be a single key (as a string) or a combination.
    The function returns True if all specified keys are pressed,
    and False if any key is not pressed or not recognized.

    Parameters:
    keys : str
        The key or list of keys to check. The key names should correspond to
        the key mappings.
        It can take keyboard keys and also mouse buttons.

    Returns:
    bool
        True if all specified keys are pressed, False otherwise.

    Example:
    keyDetect('a')           # Check if the 'a' key is pressed.
    keyDetect('ctrl', 'c')   # Check if both 'ctrl' and 'c' keys are pressed.
    keyDetect('left_mouse')  # Check if left mouse button is pressed.
    keyDetect('xbutton1')    # Check if mouse xbutton1 is pressed.
    """
    user32 = ctypes.windll.user32
    KEY_CODE = {**VK_CODE, **MVB_CODE}

    # Check if keys is a single key (string) and convert it to a list
    if isinstance(keys, str):
        keys = [keys]

    pressed_keys = []
    for key_code in range(0x01, 0xFE):
        key_state = user32.GetAsyncKeyState(key_code)
        if key_state & 0x8000:  # Check if key is held down
            pressed_keys.append(hex(key_code))

    for key in keys:
        if hex(KEY_CODE.get(key.lower(), 0)) not in pressed_keys:
            return False

    # If all keys are pressed, return True
    return True


# Mouse Functions

def mouseClick(button='left', interval=0, presses=1,
               key_delay=DEFAULT_INTERVAL):
    """
    Simulate mouse click events.

    This function simulates mouse click events for a specified mouse button.
    The button parameter determines which mouse button to click,
    and the presses parameter specifies the number of times to click the button.

    Parameters:
    button : str, optional
        The mouse button to click ('left', 'right', 'middle', 'xbutton1', or 'xbutton2'). Default is 'left'.
    interval : float, optional
        The interval (in seconds) between each clicks.
    presses : int, optional
        The number of times to click the mouse button. Default is 1.
    key_delay: float, optional
        The delay (in seconds) between each click down and click release.

    Example:
    mouseClick('left')                            # Click the left mouse button once.
    mouseClick('right', presses=2, interval=0.5)  # Double-click the right mouse button with a 0.5-second interval.
    mouseClick('middle', presses=3)               # Triple-click the middle mouse button.
    mouseClick('xbutton1')                        # Click the first extra mouse button (xbutton1).
    mouseClick('xbutton2')                        # Click the second extra mouse button (xbutton2).
    """

    button = button.lower()

    # Use different approach for xbuttons vs regular buttons
    if button in ['xbutton1', 'xbutton2']:
        # Get the xbutton data value
        mouse_data = XBUTTON_DATA.get(button, 0)

        for _ in range(presses):
            # Press the xbutton
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_XDOWN, 0, 0, mouse_data, 0)
            sleep(key_delay)

            # Release the xbutton
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_XUP, 0, 0, mouse_data, 0)
            sleep(interval)
    else:
        # Regular buttons use SendInput
        button_code = MB_CODE.get(button)

        for _ in range(presses):
            # Send mouse button press event
            extra = ctypes.c_ulong(0)
            ii_ = Input_I()
            ii_.mi = MouseInput(0, 0, 0, button_code, 0, ctypes.pointer(extra))
            x = Input(ctypes.c_ulong(0), ii_)
            ctypes.windll.user32.SendInput(
                1, ctypes.pointer(x), ctypes.sizeof(x)
            )

            sleep(key_delay)

            # Send mouse button release event
            extra = ctypes.c_ulong(0)
            ii_ = Input_I()
            ii_.mi = MouseInput(
                0, 0, 0, button_code << 1, 0, ctypes.pointer(extra)
            )
            x = Input(ctypes.c_ulong(0), ii_)
            ctypes.windll.user32.SendInput(
                1, ctypes.pointer(x), ctypes.sizeof(x)
            )

            sleep(interval)


def mouseDown(button='left'):
    """
    Simulate pressing down a mouse button.

    This function simulates pressing down a specified mouse button.
    The button parameter determines which mouse button to press.

    Parameters:
    button : str, optional
        The mouse button to press ('left', 'right', 'middle', 'xbutton1', or 'xbutton2'). Default is 'left'.

    Example:
    mouseDown('left')     # Press down the left mouse button.
    mouseDown('right')    # Press down the right mouse button.
    mouseDown('middle')   # Press down the middle mouse button.
    mouseDown('xbutton1') # Press down the first extra mouse button.
    mouseDown('xbutton2') # Press down the second extra mouse button.
    """

    button = button.lower()

    # Use different approach for xbuttons vs regular buttons
    if button in ['xbutton1', 'xbutton2']:
        # Get the xbutton data value
        mouse_data = XBUTTON_DATA.get(button, 0)

        # Press the xbutton
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_XDOWN, 0, 0, mouse_data, 0)
    else:
        # Regular buttons use SendInput
        button_code = MB_CODE.get(button)

        # Send mouse button press event
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(0, 0, 0, button_code, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(
            1, ctypes.pointer(x), ctypes.sizeof(x)
        )


def mouseUp(button='left'):
    """
    Simulate releasing a mouse button.

    This function simulates releasing a specified mouse button.
    The button parameter determines which mouse button to release.

    Parameters:
    button : str, optional
        The mouse button to release ('left', 'right', 'middle', 'xbutton1', or 'xbutton2'). Default is 'left'.

    Example:
    mouseUp('left')     # Release the left mouse button.
    mouseUp('right')    # Release the right mouse button.
    mouseUp('middle')   # Release the middle mouse button.
    mouseUp('xbutton1') # Release the first extra mouse button.
    mouseUp('xbutton2') # Release the second extra mouse button.
    """

    button = button.lower()

    # Use different approach for xbuttons vs regular buttons
    if button in ['xbutton1', 'xbutton2']:
        # Get the xbutton data value
        mouse_data = XBUTTON_DATA.get(button, 0)

        # Release the xbutton
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_XUP, 0, 0, mouse_data, 0)
    else:
        # Regular buttons use SendInput
        button_code = MB_CODE.get(button)

        # Send mouse button release event
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(0, 0, 0, button_code << 1, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(
            1, ctypes.pointer(x), ctypes.sizeof(x)
        )


@contextmanager
def mouseHold(button='left'):
    """
    Simulate holding down a specified mouse button.

    This function simulates pressing and holding down a specified mouse button.
    The button parameter can be 'left', 'right', 'middle', 'xbutton1', or 'xbutton2'.
    This function should be used with a `with` statement to ensure that
    the mouse button is released after the block of code is executed.

    Parameters:
    button : str, optional
        The mouse button to hold down ('left', 'right', 'middle', 'xbutton1', or 'xbutton2'). Default is 'left'.

    Example:
    with mouseHold('left'):
        directinput.keyPress("esc")
    with mouseHold('xbutton1'):
        directinput.keyPress("a")
    """

    button = button.lower()

    # Use different approach for xbuttons vs regular buttons
    if button in ['xbutton1', 'xbutton2']:
        # Get the xbutton data value
        mouse_data = XBUTTON_DATA.get(button, 0)

        # Press the xbutton
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_XDOWN, 0, 0, mouse_data, 0)

        # Yield control to the calling function
        yield

        # Release the xbutton
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_XUP, 0, 0, mouse_data, 0)
    else:
        # Regular buttons use SendInput
        button_code = MB_CODE.get(button)

        # Send mouse button press event
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(0, 0, 0, button_code, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(
            1, ctypes.pointer(x), ctypes.sizeof(x)
        )

        # Yield control to the calling function
        yield

        # Send mouse button release event
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(0, 0, 0, button_code << 1, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(
            1, ctypes.pointer(x), ctypes.sizeof(x)
        )


def moveMouseTo(x=None, y=None, duration=0.0):
    """
    Move the mouse cursor to a specified position over a given duration.

    This function moves the mouse cursor to a specified (x, y) position on the screen
    over a specified duration. If either x or y is not provided,
    the current mouse position for that axis will be used.

    Parameters:
    x : int, optional
        The target x-coordinate for the mouse cursor. If not specified, the current x-coordinate is used.
    y : int, optional
        The target y-coordinate for the mouse cursor. If not specified, the current y-coordinate is used.
    duration : float, optional
        The duration over which the mouse cursor should move to the target position,
        in seconds. Default is 0.0, which moves the cursor instantly.

    Example:
    moveMouseTo(100, 200)             # Instantly move the cursor to (100, 200).
    moveMouseTo(300, 400, 1.0)        # Move the cursor to (300, 400) over 1 second.
    moveMouseTo(y=500, duration=0.5)  # Move the cursor vertically to y=500 over 0.5 seconds.
    """

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
        sleep(duration / steps)
        current_x += step_x
        current_y += step_y
        ctypes.windll.user32.SetCursorPos(int(current_x), int(current_y))


def moveMouse(xOffset=0, yOffset=0, duration=0.0):
    """
    Move the mouse cursor relative to its current position by specified offsets.

    This function moves the mouse cursor from its current position
    by a specified x and y offset over a given duration.

    Parameters:
    xOffset : int or float, optional
        The offset in the x direction to move the mouse cursor. Default is 0.
    yOffset : int or float, optional
        The offset in the y direction to move the mouse cursor. Default is 0.
    duration : float, optional
        The duration over which the mouse cursor should move to the new position,
        in seconds. Default is 0.0, which moves the cursor instantly.

    Example:
    moveMouse(100, 50)                    # Instantly move the cursor 100 pixels right and 50 pixels down.
    moveMouse(-50, 0, 1.0)                # Move the cursor 50 pixels left over 1 second.
    moveMouse(yOffset=100, duration=0.5)  # Move the cursor 100 pixels down over 0.5 seconds.
    """

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
        sleep(duration / steps)
        current_x += step_x
        current_y += step_y
        ctypes.windll.user32.SetCursorPos(int(current_x), int(current_y))


def scrollMouse(clicks):
    """
    Scroll the mouse wheel vertically.

    This function simulates scrolling the mouse wheel vertically.
    The `clicks` parameter determines the amount and direction of the scroll.
    Positive values scroll up, while negative values scroll down.
    For a visible result, it is recommended to use a value of 100 or more,
    as smaller numbers may not produce a significant scrolling effect.

    Parameters:
    clicks : int
        The number of clicks to scroll. Positive values scroll up, negative values scroll down.

    Example:
    scrollMouse(120)   # Scroll up with a value of 120 clicks.
    scrollMouse(-100)  # Scroll down with a value of 100 clicks.
    """

    if clicks != 0:
        ctypes.windll.user32.mouse_event(0x0800, 0, 0, clicks, 0)


# Utility Functions

def screenshot(filename=None, region=None):
    """
    Take a screenshot of the entire screen or a specified region.

    This function captures a screenshot of the entire screen or a specified region.
    If a region is specified, it captures the region defined
    by the tuple (top-left x, top-left y, width, height).
    The screenshot can be saved to a file if a filename is provided.

    Parameters:
    filename : str, optional
        The file path to save the screenshot. If not specified,
        the screenshot is not saved. You can put any file type such as .png, .jpg or .pdf.
    region : tuple, optional
        A tuple specifying the region to capture (top-left x, top-left y, width, height).
        If not specified, captures the entire screen.

    Returns:
    Image
        The captured screenshot as an Image object.

    Example:
    screenshot('screenshot.png')                           # Capture the entire screen and save as 'screenshot.png'.
    screenshot(region=(0, 0, 800, 600))                    # Capture a region of the screen.
    screenshot('region.png', region=(100, 100, 300, 200))  # Capture a region and save as 'region.png'.
    """

    if region:
        img = pyscreeze.screenshot(region=region)
    else:
        img = pyscreeze.screenshot()

    if filename:
        img.save(filename)

    return img


def getMousePosition():
    """
    Get the current position of the mouse cursor.

    This function returns the current position of the mouse cursor (x, y).

    Returns:
    Point
        The current mouse cursor position as (x, y).

    Example:
    position = getMousePosition()
    print(position.x, position.y)  # Output the current cursor position.
    """

    cursor = wintypes.POINT()
    windll.user32.GetCursorPos(byref(cursor))
    return Point(cursor.x, cursor.y)


def getDisplaySize():
    """
    Get the size of the primary display.

    This function returns the width and height of the primary display (width, height).

    Returns:
    Size
        The size of the primary display as (width, height).

    Example:
    display_size = getDisplaySize()
    print(display_size.width, display_size.height)  # Output the display size.
    """

    user32 = ctypes.windll.user32
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    return Size(width, height)


def locateImage(needleImage, haystackImage=None, grayscale=False,
                region=None, threshold=0.990):
    """
    Search for an image within another image or the screen.

    This function searches for a smaller image (needleImage)
    within a larger image (haystackImage) or the entire screen.
    If haystackImage is not provided, the function captures the entire screen for searching.
    The search can be performed in grayscale for improved performance,
    and a specific region can be defined for the search.
    The threshold parameter sets the accuracy required for a match.

    Parameters:
    needleImage : str
        The file path of the image to locate.
    haystackImage : str, optional
        The file path of the image in which to search. If not provided, the entire screen is used.
    grayscale : bool, optional
        Whether to perform the search in grayscale. Default is False.
    region : tuple, optional
        A tuple specifying the region to search
        within (top-left x, top-left y, width, height).
        If not specified, the entire image or screen is used.
    threshold : float, optional
        The confidence threshold for image matching. Default is 0.999.

    Returns:
    Point or None
        The center coordinates of the located image as (x, y), or None if the image is not found.

    Example:
    position = locateImage('needle.png')                                                  # Search for 'needle.png' on the entire screen.
    position = locateImage('needle.png', 'haystack.png', grayscale=True, threshold=0.95)  # Search within 'haystack.png' in grayscale with 95% confidence.
    position = locateImage('needle.png', region=(0, 0, 800, 600))                         # Search within a specific region of the screen.
    """

    needleImage = imread(needleImage)
    if haystackImage is None:
        # Take a screenshot of the entire screen
        with mss.mss() as sct:
            haystackImage = array(sct.grab(sct.monitors[1]))
    else:
        haystackImage = imread(haystackImage)

    if grayscale:
        needleImage = cvtColor(needleImage, COLOR_BGR2GRAY)
        haystackImage = cvtColor(haystackImage, COLOR_BGR2GRAY)
    else:
        needleImage = cvtColor(needleImage, COLOR_BGR2RGB)
        haystackImage = cvtColor(haystackImage, COLOR_BGR2RGB)
    # Find the image
    coords = pyscreeze.locate(needleImage, haystackImage,
                              region=region, confidence=threshold)
    if coords is None:
        return None
    else:
        # Return the center coordinates of the image
        center_x, center_y = float(coords[0] + coords[2]/2), float(coords[1] + coords[3]/2)
        return Point(center_x, center_y)


# Failsafe Mechanism

class Failsafe:
    """
    A failsafe mechanism to abort script execution when certain keys are held down.

    This class implements a failsafe mechanism that monitors for specified keys being
    held down for a certain duration. When triggered, it will abort the script execution.
    By default, it monitors the Esc key for 5 seconds.

    Attributes:
        enabled (bool): Whether the failsafe is enabled.
        trigger_keys (list): List of keys that trigger the failsafe when held down.
        hold_time (float): Duration in seconds that keys must be held to trigger.
        callback (callable): Function to call when failsafe is triggered.
        _thread (Thread): Background thread that monitors key states.
        _stop_event (Event): Event to signal the monitoring thread to stop.
    """

    def __init__(self, trigger_keys=['esc'], hold_time=5.0, callback=None):
        """
        Initialize the failsafe mechanism.

        Args:
            trigger_keys (list): Keys that trigger the failsafe when held down.
            hold_time (float): Duration in seconds that keys must be held to trigger.
            callback (callable): Function to call when failsafe is triggered.
                                If None, the script will exit with sys.exit(1).
        """
        self.enabled = True
        self.trigger_keys = trigger_keys if isinstance(trigger_keys, list) else [trigger_keys]
        self.hold_time = hold_time
        self.callback = callback
        self._thread = None
        self._stop_event = threading.Event()

        # Start the monitoring thread
        self._start_monitoring()

    def _start_monitoring(self):
        """Start the background thread that monitors key states."""
        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._monitor_keys, daemon=True)
            self._thread.start()

    def _monitor_keys(self):
        """Monitor key states in a background thread."""
        key_hold_start = None

        while not self._stop_event.is_set():
            if not self.enabled:
                key_hold_start = None
                time.sleep(0.1)
                continue

            # Check if all trigger keys are pressed
            all_keys_pressed = all(keyDetect(key) for key in self.trigger_keys)

            if all_keys_pressed:
                # If keys just started being pressed, record the time
                if key_hold_start is None:
                    key_hold_start = time.time()
                    print(f"Failsafe: Holding {', '.join(self.trigger_keys)} detected. "
                          f"Hold for {self.hold_time} seconds to trigger failsafe.")

                # Check if keys have been held long enough
                elif time.time() - key_hold_start >= self.hold_time:
                    self._trigger_failsafe()
                    return
            else:
                # Reset the timer if keys are released
                key_hold_start = None

            # Sleep to prevent high CPU usage
            time.sleep(0.1)

    def _trigger_failsafe(self):
        """Trigger the failsafe action."""
        print("\nFAILSAFE TRIGGERED!")
        print(f"Keys {', '.join(self.trigger_keys)} held for {self.hold_time} seconds.")

        if self.callback:
            self.callback()
        else:
            print("Aborting script execution.")
            # Use os._exit() to force immediate termination of the entire process
            # This is more forceful than sys.exit() and will terminate all threads
            os._exit(1)

    def stop(self):
        """Stop the failsafe monitoring thread."""
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)

    def enable(self):
        """Enable the failsafe mechanism."""
        self.enabled = True
        print("Failsafe enabled.")

    def disable(self):
        """Disable the failsafe mechanism."""
        self.enabled = False
        print("Failsafe disabled.")

    def configure(self, trigger_keys=None, hold_time=None, callback=None):
        """
        Configure the failsafe parameters.

        Args:
            trigger_keys (list or str, optional): Keys that trigger the failsafe.
            hold_time (float, optional): Duration in seconds keys must be held.
            callback (callable, optional): Function to call when triggered.
        """
        if trigger_keys is not None:
            self.trigger_keys = trigger_keys if isinstance(trigger_keys, list) else [trigger_keys]

        if hold_time is not None:
            self.hold_time = float(hold_time)

        if callback is not None:
            self.callback = callback

        print(f"Failsafe configured: Keys={self.trigger_keys}, Hold time={self.hold_time}s")


# Create a global failsafe instance
_failsafe = Failsafe()

def enableFailsafe():
    """
    Enable the failsafe mechanism.

    The failsafe mechanism allows you to abort script execution by holding down
    the configured key(s) for the specified duration.

    Example:
    enableFailsafe()  # Enable the default failsafe (Esc key for 5 seconds)
    """
    global _failsafe
    _failsafe.enable()

def disableFailsafe():
    """
    Disable the failsafe mechanism.

    This function disables the failsafe mechanism, preventing it from
    aborting script execution when the trigger keys are held down.

    Example:
    disableFailsafe()  # Disable the failsafe mechanism
    """
    global _failsafe
    _failsafe.disable()

def configFailsafe(trigger_keys=None, hold_time=None, callback=None):
    """
    Configure the failsafe mechanism.

    This function allows you to customize the failsafe mechanism by specifying
    which keys trigger it, how long they need to be held, and what action to take.

    Parameters:
    trigger_keys : str or list, optional
        The key or list of keys that trigger the failsafe when held down.
        Default is ['esc'] (the Escape key).
    hold_time : float, optional
        The duration in seconds that the keys must be held to trigger the failsafe.
        Default is 5.0 seconds.
    callback : callable, optional
        A function to call when the failsafe is triggered. If not specified,
        the script will forcefully terminate using os._exit(1).

    Example:
    configureFailsafe(['ctrl', 'alt'], 3.0)  # Trigger when Ctrl+Alt is held for 3 seconds
    configureFailsafe('f12', 2.0)            # Trigger when F12 is held for 2 seconds
    """
    global _failsafe
    _failsafe.configure(trigger_keys, hold_time, callback)
