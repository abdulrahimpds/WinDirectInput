import directinput as di

while True:
    try:
        if di.keyDetect('d'):
            print("pss")
            break
    except Exception as e:
        print(f'e')

##import ctypes
##
##user32 = ctypes.windll.user32
##
##VK_CODE_TEST_KEYS = [
##    'a', 'b', 'c', 'q', 'alt', 'ctrl', 'space', 'enter',
##    'shift', 'esc', 'tab', 'backspace', 'capslock', 'numlock',
##    'insert', 'delete', 'home', 'end', 'pageup', 'pagedown',
##    'up', 'down', 'left', 'right', 'win', 'lwin', 'rwin', 'prtsc'
##]
##
##print("Press each key and check its Virtual Key Code:")
##
##def get_key_vk_code():
##    for key_code in range(0x01, 0xFE):
##        key_state = user32.GetAsyncKeyState(key_code)
##        if key_state & 0x8000:
##            print(f"Key Code: {hex(key_code)} Pressed")
##    return None
##
##while True:
##    get_key_vk_code()
