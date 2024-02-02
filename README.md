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
`locateImage` comes with several parameters for refined control:
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
