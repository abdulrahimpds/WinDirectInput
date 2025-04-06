import time
import directinput_v2 as di

# Define the key testing function
def test_key_functions(key_functions, keys):
    results = []
    for key in keys:
        try:
            # Test keyDown
            key_functions['keyDown'](key)
            time.sleep(0.05)  # Small delay
            key_functions['keyUp'](key)
            time.sleep(0.05)  # Small delay

            # Test keyPress
            key_functions['keyPress'](key, interval=0.05)

            results.append((key, "Success"))
        except Exception as e:
            results.append((key, f"Failed: {e}"))

    return results

# Define a list of all standard keys
standard_keys = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'num0', '0', 'num1', '1', 'num2', '2', 'num3', '3', 'num4', '4', 'num5', '5', 'num6', '6', 'num7', '7', 'num8', '8', 'num9', '9',
    'num/', 'num.', 'num-', 'num+', 'num*',
    'up', 'left', 'down', 'right',
    'space', 'esc', 'tab', 'backspace', 'enter', 'numenter', 'shift', 'lshift', 'rshift', 'ctrl', 'lctrl', 'rctrl', 'alt', 'lalt', 'ralt',
    'apps', 'capslock', 'numlock', 'scrolllock', 'insert', 'delete', 'home', 'end', 'pageup', 'pagedown',
    'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
    '`', '-', '=', '[', ']', '\\', ';', '\'', ',', '.', '/',
    'win', 'lwin', 'rwin', 'prtsc', 'sysrq'
]

# Define the key functions to test
key_functions = {
    'keyDown': di.keyDown,
    'keyUp': di.keyUp,
    'keyPress': di.keyPress
}

# Run the tests
test_results = []

user_input = str(input("ready? "))

if user_input.lower() == "yes":
    time.sleep(2)
    test_results = test_key_functions(key_functions, standard_keys)
    time.sleep(1)
    di.keyPress('esc'); di.mouseClick()
    di.mouseClick(); di.keyPress('prtsc')
    time.sleep(1.5); di.keyPress('esc')
else:
    print("nvm!")

# Print the test results
for key, result in test_results:
    print(f"Key: {key}, Result: {result}")
