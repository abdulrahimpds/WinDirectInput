"""
Test script for the failsafe mechanism in WinDirectInput.

This script demonstrates how to use the failsafe mechanism in WinDirectInput.
It will move the mouse cursor in a circle pattern until you trigger the failsafe
by holding down the Esc key for 5 seconds (default) or by holding down the
configured key(s) for the specified duration.
"""

import directinput
import time
import math

def main():
    print("Testing the failsafe mechanism in WinDirectInput")
    print("By default, hold ESC for 5 seconds to trigger the failsafe")
    print("This script will move the mouse cursor in a circle pattern")
    
    # Uncomment to configure a different failsafe key and duration
    # directinput.configureFailsafe('f12', 3.0)
    # print("Configured failsafe: Hold F12 for 3 seconds to trigger")
    
    # Get the screen dimensions
    screen_size = directinput.getDisplaySize()
    center_x = screen_size.width // 2
    center_y = screen_size.height // 2
    radius = min(center_x, center_y) // 3
    
    print("\nMoving mouse in a circle pattern...")
    print("Hold the failsafe key(s) to abort")
    
    try:
        angle = 0
        while True:
            # Calculate the next position on the circle
            x = center_x + int(radius * math.cos(angle))
            y = center_y + int(radius * math.sin(angle))
            
            # Move the mouse to the new position
            directinput.moveMouseTo(x, y, duration=0.01)
            
            # Increment the angle for the next position
            angle += 0.05
            if angle >= 2 * math.pi:
                angle = 0
                
            # Small delay to make the movement visible
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        print("\nScript terminated by user (Ctrl+C)")
    except SystemExit:
        print("\nScript terminated by failsafe")
    
    print("Test completed")

if __name__ == "__main__":
    main()
