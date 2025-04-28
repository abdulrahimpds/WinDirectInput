# WinDirectInput

**WinDirectInput** is born out of a desire to enhance and extend the capabilities left untouched by PyAutoGUI. It's a robust tool designed for developers and automation enthusiasts. This module excels in detecting key inputs and offers an improved screenshot functionality using mss, providing a faster alternative for real-time applications like object detection with OpenCV.

This module is a testament to innovation in automation, filling gaps and pushing the boundaries of what's possible in automated input control.

## Installation

To start using WinDirectInput, simply install it via pip:
```bash
pip install WinDirectInput
```

After installation, you can import and use the module in your Python scripts:
```Python
import directinput
```

## Dependencies

**WinDirectInput** thrives on the shoulders of powerful dependencies and requires Python 3.8 or higher. Key dependencies include:

- `opencv-python`: For image processing and object detection integrations.
- `numpy`: Essential for handling arrays and complex mathematical operations.
- `mss`: The secret ingredient for lightning-fast screenshots.
- `pyscreeze`, `pyperclip`: Supporting libraries enhancing the module's functionality.

## Functionalities

### Keyboard Functions

- **`keyDown(*keys)`**
  - Simulates pressing down one or more keys.
  - **Parameters:**
    - `*keys` (str): One or more keys to press down. Key names should correspond to key mappings.
  - **Example:**
    ```python
    directinput.keyDown('ctrl', 'a')
    ```

- **`keyUp(*keys)`**
  - Simulates releasing one or more keys.
  - **Parameters:**
    - `*keys` (str): One or more keys to release. Key names should correspond to key mappings.
  - **Example:**
    ```python
    directinput.keyUp('ctrl', 'shift')
    ```

- **`keyHold(*keys)`**
  - Simulates holding down one or more specified keys.
  - The keys parameter can be a single key or a list of keys.
  - This function should be used with a `with` statement to ensure that the keys are released after the block of code is executed.
  - **Parameters:**
    - `*keys` (str): One or more keys to hold down.
  - **Example:**
    ```python
    with directinput.keyHold("ctrl", "shift"):
        directinput.keyPress("esc")
    ```

- **`keyPress(keys, interval=0.01, presses=1, key_delay=0.01, simultaneously=False)`**
  - Simulates pressing one or more keys.
  - The `keys` parameter can be a single key or a list of keys.
  - Additionally, the `simultaneously` parameter can be set to `True` to press all keys at once, rather than sequentially.
  - **Parameters:**
    - `keys` (str or list of str): The key or list of keys to press. Key names should correspond to key mappings.
    - `interval` (float, optional): The interval between key presses in seconds. Default is 0.01.
    - `presses` (int, optional): The number of times to press the keys. Default is 1.
    - `key_delay` (float, optional): The delay between each key press and release in seconds. Default is 0.01.
    - `simultaneously` (bool, optional): Whether to press all keys at once. Default is False.
  - **Example:**
    ```python
    directinput.keyPress('a')
    directinput.keyPress(['ctrl', 'c'])
    directinput.keyPress(['ctrl', 'shift'], simultaneously=True)
    directinput.keyPress('b', presses=3, interval=0.5)
    ```

- **`hotKey(*keys, key_delay=0.01)`**
  - Simulates pressing a combination of keys, which are pressed down in order, and then released in reverse order.
  - This function can accept multiple key arguments.
  - **Parameters:**
    - `*keys` (str): One or more keys to press as part of the hotkey combination.
    - `key_delay` (float, optional): The delay between each key press and release in seconds. Default is 0.01.
  - **Example:**
    ```python
    directinput.hotKey('ctrl', 'shift', 'esc')
    ```

- **`write(text, interval=0.0, key_delay=0.03)`**
  - Types out a given text string.
  - Optionally, `interval` (in seconds) between key presses can be specified to simulate a more natural typing speed.
  - **Parameters:**
    - `text` (str): The text string to type out.
    - `interval` (float, optional): The interval between each character in seconds. Default is 0.0.
    - `key_delay` (float, optional): The delay between key press and release for each character in seconds. Default is 0.03.
  - **Example:**
    ```python
    directinput.write("Hello, World!", interval=0.1)
    ```

- **`keyDetect(*keys)`**
  - Checks if one or more specified keys are currently pressed.
  - The `keys` parameter can be a single key (as a string) or a list of keys.
  - **Parameters:**
    - `*keys` (str): The key or a combination of keys to check. It can take keyboard keys and also mouse buttons.
  - **Returns:**
    - `bool`: `True` if all specified keys are pressed, `False` otherwise.
  - **Example:**
    ```python
    directinput.keyDetect('a')           # Check if the 'a' key is pressed.
    directinput.keyDetect('ctrl', 'c')   # Check if both 'ctrl' and 'c' keys are pressed.
    directinput.keyDetect('left_mouse')  # Check if left mouse button is pressed.
    directinput.keyDetect('xbutton1')    # Check if mouse xbutton1 is pressed.
    ```

### Mouse Functions

- **`mouseClick(button='left', interval=0.01, presses=1, key_delay=0.01)`**
  - Simulates mouse click events.
  - **Parameters:**
    - `button` (str, optional): The mouse button to click ('left', 'right', 'middle', 'xbutton1', or 'xbutton2'). Default is 'left'.
    - `interval` (float, optional): The interval (in seconds) between each click. Default is 0.01.
    - `presses` (int, optional): The number of times to click the mouse button. Default is 1.
    - `key_delay` (float, optional): The delay (in seconds) between each click down and click release. Default is 0.01.
  - **Example:**
    ```python
    directinput.mouseClick('left')
    directinput.mouseClick('right', presses=2, interval=0.5)
    directinput.mouseClick('middle', presses=3)
    directinput.mouseClick('xbutton1')
    directinput.mouseClick('xbutton2')
    ```

- **`mouseDown(button='left')`**
  - Simulates pressing down a mouse button.
  - **Parameters:**
    - `button` (str, optional): The mouse button to press ('left', 'right', 'middle', 'xbutton1', or 'xbutton2'). Default is 'left'.
  - **Example:**
    ```python
    directinput.mouseDown('left')
    directinput.mouseDown('right')
    directinput.mouseDown('middle')
    directinput.mouseDown('xbutton1')
    directinput.mouseDown('xbutton2')
    ```

- **`mouseUp(button='left')`**
  - Simulates releasing a mouse button.
  - **Parameters:**
    - `button` (str, optional): The mouse button to release ('left', 'right', 'middle', 'xbutton1', or 'xbutton2'). Default is 'left'.
  - **Example:**
    ```python
    directinput.mouseUp('left')
    directinput.mouseUp('right')
    directinput.mouseUp('middle')
    directinput.mouseUp('xbutton1')
    directinput.mouseUp('xbutton2')
    ```

- **`mouseHold(button='left')`**
  - Simulates holding down a specified mouse button, similar to the `keyHold` function.
  - The `button` parameter can be 'left', 'right', 'middle', 'xbutton1', or 'xbutton2'.
  - This function should be used with a `with` statement to ensure that the mouse button is released after the block of code is executed.
  - **Parameters:**
    - `button` (str, optional): The mouse button to hold down ('left', 'right', 'middle', 'xbutton1', or 'xbutton2'). Default is 'left'.
  - **Example:**
    ```python
    with directinput.mouseHold('right'):
        directinput.keyPress("esc")
    with directinput.mouseHold('xbutton1'):
        directinput.keyPress("a")
    ```

- **`moveMouseTo(x=None, y=None, duration=0.0)`**
  - Moves the mouse cursor to a specified position over a given duration.
  - **Parameters:**
    - `x` (int or float, optional): The target x-coordinate for the mouse cursor. If not specified, the current x-coordinate is used.
    - `y` (int or float, optional): The target y-coordinate for the mouse cursor. If not specified, the current y-coordinate is used.
    - `duration` (int or float, optional): The duration over which the mouse cursor should move to the target position, in seconds. Default is 0.0.
  - **Example:**
    ```python
    directinput.moveMouseTo(100, 200)
    directinput.moveMouseTo(300, 400, 1.0)
    directinput.moveMouseTo(y=500, duration=0.5)
    ```

- **`moveMouse(xOffset=0, yOffset=0, duration=0.0)`**
  - Moves the mouse cursor relative to its current position by specified x and y offsets over a specified duration.
  - **Parameters:**
    - `xOffset` (int or float, optional): The offset in the x direction to move the mouse cursor. Default is 0.
    - `yOffset` (int or float, optional): The offset in the y direction to move the mouse cursor. Default is 0.
    - `duration` (int or float, optional): The duration over which the mouse cursor should move to the new position, in seconds. Default is 0.0.
  - **Example:**
    ```python
    directinput.moveMouse(100, 50)
    directinput.moveMouse(-50, 0, 1.0)
    directinput.moveMouse(yOffset=100, duration=0.5)
    ```

- **`scrollMouse(clicks)`**
  - Scrolls the mouse wheel vertically.
  - The `clicks` parameter determines the amount and direction of the scroll: a positive value scrolls up, while a negative value scrolls down.
  - For a visible result, it is recommended to use a value of 100 or more, as smaller numbers may not produce a significant scrolling.
  - **Parameters:**
    - `clicks` (int): The number of clicks to scroll. Positive values scroll up, negative values scroll down.
  - **Example:**
    ```python
    directinput.scrollMouse(120)   # Scroll up with a value of 120 clicks.
    directinput.scrollMouse(-100)  # Scroll down with a value of 100 clicks.
    ```

### Failsafe Mechanism

WinDirectInput includes a failsafe mechanism that allows you to abort script execution by holding down specific keys for a set duration. This is useful for regaining control if your automation script goes awry.

By default, the failsafe is enabled when you import the module and will terminate the script if you hold down the **Esc key for 5 seconds**. This behavior can be customized using the functions below.

- **`enableFailsafe()`**
  - Enables the failsafe mechanism.
  - By default, the failsafe is enabled when the module is imported.
  - **Example:**
    ```python
    directinput.enableFailsafe()  # Enable the default failsafe (Esc key for 5 seconds)
    ```

- **`disableFailsafe()`**
  - Disables the failsafe mechanism.
  - Use this with caution, as it removes your safety net.
  - When disabled, the failsafe keys can be held down without triggering script termination.
  - This is useful for sections of code where you need to use the failsafe keys for other purposes.
  - **Example:**
    ```python
    # Disable failsafe completely for the entire script
    directinput.disableFailsafe()

    # Or disable temporarily for a specific section
    directinput.disableFailsafe()
    try:
        # Run operations where failsafe might interfere
        # ...
    finally:
        # Re-enable failsafe when done
        directinput.enableFailsafe()
    ```

- **`configFailsafe(trigger_keys=None, hold_time=None, callback=None)`**
  - Configures the failsafe mechanism.
  - **Parameters:**
    - `trigger_keys` (str or list, optional): The key or list of keys that trigger the failsafe when held down. Default is ['esc'] (the Escape key).
    - `hold_time` (float, optional): The duration in seconds that the keys must be held to trigger the failsafe. Default is 5.0 seconds.
    - `callback` (callable, optional): A function to call when the failsafe is triggered. If not specified, the script will forcefully terminate using os._exit(1).
  - **Example:**
    ```python
    # Configure failsafe to trigger when Ctrl+Alt is held for 3 seconds
    directinput.configFailsafe(['ctrl', 'alt'], 3.0)

    # Configure failsafe to trigger when F12 is held for 2 seconds
    directinput.configFailsafe('f12', 2.0)

    # Configure failsafe with a custom callback function
    def my_failsafe_handler():
        print("Failsafe triggered! Cleaning up...")
        # Custom cleanup code here

    directinput.configFailsafe('esc', 5.0, my_failsafe_handler)
    ```

### Utility Functions

- **`screenshot(filename=None, region=None)`**
  - Takes a screenshot of the entire screen.
  - Additionally, there's a `region` parameter which captures specified region of the screen.
  - It takes a tuple specifying the top-left x, top-left y, width, and height.
  - **Parameters:**
    - `filename` (str, optional): The file path to save the screenshot. This can be any valid file type such as .png, .jpg, .pdf, etc. If not specified, the screenshot is not saved.
    - `region` (tuple, optional): A tuple specifying the region to capture (top-left x, top-left y, width, height). If not specified, captures the entire screen.
  - **Returns:**
    - `Image`: The captured screenshot as an Image object.
  - **Example:**
    ```python
    directinput.screenshot('screenshot.png')
    directinput.screenshot(region=(0, 0, 800, 600))
    directinput.screenshot('region.png', region=(100, 100, 300, 200))
    ```

- **`getMousePosition()`**
  - Returns the current (x, y) position of the mouse cursor.
  - **Returns:**
    - `Point`: The current mouse cursor position as (x, y).
  - **Example:**
    ```python
    position = directinput.getMousePosition()
    print(position.x, position.y)
    ```

- **`getDisplaySize()`**
  - Returns the width and height of the primary display.
  - **Returns:**
    - `Size`: The size of the primary display as (width, height).
  - **Example:**
    ```python
    display_size = directinput.getDisplaySize()
    print(display_size.width, display_size.height)
    ```

- **`locateImage(needleImage, haystackImage=None, grayscale=False, region=None, threshold=0.999)`**
  - Searches for an image (`needleImage`) within another image (`haystackImage`) or the screen.
  - If `haystackImage` is not provided, the entire screen is used.
  - The `grayscale` parameter can be set to `True` to perform the search in grayscale, which can improve performance.
  - The `region` parameter can specify a specific area to search within, and `threshold` sets the accuracy required for a match.
  - **Parameters:**
    - `needleImage` (str): The file path of the image to locate.
    - `haystackImage` (str, optional): The file path of the image in which to search. If not provided, the entire screen is used.
    - `grayscale` (bool, optional): Whether to perform the search in grayscale. Default is False.
    - `region` (tuple, optional): A tuple specifying the region to search within (top-left x, top-left y, width, height). If not specified, the entire image or screen is used.
    - `threshold` (float, optional): The confidence threshold for image matching. Default is 0.999.
  - **Returns:**
    - `Point` or `None`: The center coordinates of the located image as (x, y), or None if the image is not found.
  - **Example:**
    ```python
    position = directinput.locateImage('needle.png')
    position = directinput.locateImage('needle.png', 'haystack.png', grayscale=True, threshold=0.95)
    position = directinput.locateImage('needle.png', region=(0, 0, 800, 600))
    ```

## Available Keys and Mouse Buttons

All the keys and mouse buttons listed can be both detected and pressed.

### Keyboard Keys

- **Alphabets**:
  - `a`, `A`, `b`, `B`, `c`, `C`, `d`, `D`, `e`, `E`, `f`, `F`, `g`, `G`, `h`, `H`, `i`, `I`, `j`, `J`, `k`, `K`, `l`, `L`, `m`, `M`, `n`, `N`, `o`, `O`, `p`, `P`, `q`, `Q`, `r`, `R`, `s`, `S`, `t`, `T`, `u`, `U`, `v`, `V`, `w`, `W`, `x`, `X`, `y`, `Y`, `z`, `Z`

- **Numbers**:
  - `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`
  - `num0`, `num1`, `num2`, `num3`, `num4`, `num5`, `num6`, `num7`, `num8`, `num9`

- **Symbols**:
  - `` ` ``, `~`, `!`, `@`, `#`, `$`, `%`, `^`, `&`, `*`, `(`, `)`, `-`, `_`, `=`, `+`, `[`, `{`, `]`, `}`, `\`, `|`, `;`, `:`, `'`, `"`, `,`, `<`, `.`, `>`, `/`, `?`

- **Function Keys**:
  - `f1`, `f2`, `f3`, `f4`, `f5`, `f6`, `f7`, `f8`, `f9`, `f10`, `f11`, `f12`

- **Control Keys**:
  - `space`, `esc`, `tab`, `backspace`, `enter`, `numenter`, `shift`, `lshift`, `rshift`, `ctrl`, `lctrl`, `rctrl`, `alt`, `lalt`, `ralt`, `win`, `lwin`, `rwin`, `apps`, `capslock`, `numlock`, `scrolllock`, `insert`, `delete`, `home`, `end`, `pageup`, `pagedown`, `prtsc`, `sysrq`

- **Calculation Keys**:
  - `num-`, `num/`, `num*`, `num+`, `num.`

- **Arrow Keys**:
  - `up`, `down`, `left`, `right`

### Mouse Buttons

- **Primary Buttons**:
  - `left`, `right`, `middle`

- **Additional Buttons**:
  - `xbutton1`, `xbutton2` (extra mouse buttons)

## Example Usage

### Writing Complex Strings

```Python
import directinput

# Writing a string with special characters
directinput.write("Hello, world! ✌️")
```

This demonstrates the enhanced write function, capable of handling a wide range of characters, surpassing limitations you might find in other modules.

### Detecting Key Presses

```Python
import directinput

# Detect if the 'A' key is being pressed
if directinput.keyDetect('a'):
    print("The 'A' key is pressed!")

# Detect if both 'left_mouse' and 'xbutton1' is being pressed
if directinput.keyDetect(['left_mouse', 'xbutton1']):
    print("Pressed!")
```

### Using the Failsafe Mechanism

The failsafe mechanism provides a safety net for your automation scripts, allowing you to regain control if something goes wrong.

```Python
import directinput
import time

# Configure the failsafe to use F12 key held for 3 seconds
directinput.configFailsafe('f12', 3.0)

# Run a potentially risky automation task
print("Starting automation. Hold F12 for 3 seconds to abort.")
for i in range(10):
    directinput.mouseClick()  # Click repeatedly
    time.sleep(1)
    print(f"Step {i+1}/10 completed")

print("Automation completed successfully")
```

### Locating an Image on the Screen

The locateImage function in WinDirectInput adds a layer of flexibility to image detection. Whether you're automating tasks based on visual cues or integrating with image processing, this function is incredibly handy.

```Python
import directinput

# Locate an image on the screen
point = directinput.locateImage("path_to_needle_image.png")

if point is not None:
    print(f"Image found at {point}")
else:
    print("Image not found")
```

## How Does It Work?

**WinDirectInput** is tailored for Windows 10 or higher systems, harnessing the underlying Windows API to deliver its functionalities. This specific design choice ensures compatibility and performance, particularly in how keyboard and mouse inputs are handled and how screenshots are captured and processed.

## Your Contribution Matters

Your insights and contributions are pivotal to the evolution of WinDirectInput. Here's how you can get involved:

- Report Bugs or Request Features: Encounter a bug or have an idea for a new feature? Open an issue on our [GitHub](https://github.com/abdulrahimpds/WinDirectInput) page.
- Code Contributions: Got a fix or enhancement? Submit a pull request to improve the codebase.