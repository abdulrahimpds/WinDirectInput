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
- `keyDown(key=str)`
- `keyUp(key=str)`
- `keyHold(key=str)`: Simulates holding down one or more specified keys. The keys parameter can be a single key or a list of keys. This function should be used with a with statement to ensure that the keys are released after the block of code is executed. For example:
    ```python
    with directinput.keyHold("ctrl", "shift"):
        directinput.keyPress("esc")
    ```
- `keyPress(key=str, presses=int, simultaneously=bool)`: Simulates pressing one or more keys. The `keys` parameter can be a single key or a list of keys. Additionally, the `simultaneously` parameter can be set to True to press all keys at once, rather than sequentially.
- `hotKey(*keys=str)`: Simulates pressing a combination of keys simultaneously. This function can accept multiple key arguments, e.g., `hotKey('ctrl', 'shift', 's')`.
- `write(text=str, speed=float)`: Types out a given text string. Optionally, `speed` (in seconds) between key presses can be specified to simulate a more natural typing speed.
- `keyDetect(key=str)`: Checks if one or more specified keys are currently pressed. The `keys` parameter can be a single key (as a string) or a list of keys. The function returns `True` if all specified keys are pressed, and `False` if any key is not pressed or not recognized.
- `mouseClick(button=str, presses=int)`
- `mouseDown(button=str)`
- `mouseUp(button=str)`
- `mouseHold(button=str)`: Simulates holding down a specified mouse button, similar to the `keyHold` function. The `button` parameter can be 'left', 'right', or 'middle'. This function should be used with a `with` statement to ensure that the mouse button is released after the block of code is executed.
- `moveMouseTo(x=int/float, y=int/float, duration=int/float)`
- `moveMouse(xOffset=int/float, yOffset=int/float, duration=int/float)`: Moves the mouse cursor relative to its current position by specified x and y offsets over a specified duration.
- `scrollMouse(clicks=int)`: Scrolls the mouse wheel vertically. The `clicks` parameter determines the amount and direction of the scroll: a positive value scrolls up, while a negative value scrolls down. For a visible result, it is recommended to use a value of 100 or more, as smaller numbers may not produce a significant scrolling.
- `screenshot(filename=str, region=tuple)`: Takes a screenshot of the entire screen. Additionally, there's a `region` parameter which captures specified region of the screen. It takes a tuple specifying the top-left x, top-left y, width, and height.
- `getMousePosition()`: Returns the current (x, y) position of the mouse cursor.
- `getDisplaySize()`
- `locateImage(needleImage=str, haystackImage=str, grayscale=bool, region=tuple, threshold=float)`: Searches for an image (`needleImage`) within another image (`haystackImage`) or the screen. If `haystackImage` is not provided, the entire screen is used. The `grayscale` parameter can be set to `True` to perform the search in grayscale, which can improve performance. The `region` parameter can specify a specific area to search within, and `threshold` sets the accuracy required for a match.

## Example Usage

### Writing Complex Strings

```Python
import directinput

# Writing a string with special characters
directinput.write("Hello, world! 😃👍 #PythonRocks")
```

This demonstrates the enhanced write function, capable of handling a wide range of characters, surpassing limitations you might find in other modules.

### Detecting Key Presses

```Python
import directinput

# Detect if the 'A' key is being pressed
if directinput.keyDetect('a'):
    print("The 'A' key is pressed!")
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

Advanced Usage
- `locateImage` comes with several parameters for refined control:
- `needleImage`: Path to the image you want to find.
- `haystackImage`: Path to the screenshot or image in which to search. If not provided, it captures the entire screen.
- `grayscale`: Set to True for grayscale comparison, which can improve performance.
- `region`: A specific region on the screen to search in.
- `threshold`: The confidence level for image matching, allowing for slight variations.

This functionality is especially useful in scenarios where you need to interact with UI elements based on their appearance, or in cases where dynamic content changes the screen layout.

## How Does It Work?

**WinDirectInput** is tailored for Windows 10 or higher systems, harnessing the underlying Windows API to deliver its functionalities. This specific design choice ensures compatibility and performance, particularly in how keyboard and mouse inputs are handled and how screenshots are captured and processed.

## Your Contribution Matters

Your insights and contributions are pivotal to the evolution of WinDirectInput. Here's how you can get involved:

- Report Bugs or Request Features: Encounter a bug or have an idea for a new feature? Open an issue on our [GitHub](https://github.com/abdulrahimpds/WinDirectInput) page.
- Code Contributions: Got a fix or enhancement? Submit a pull request to improve the codebase.