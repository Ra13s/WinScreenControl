# WinScreenControl

A simple tool to control monitor brightness and contrast using DDC/CI.

## Why use this tool?

Most monitors require you to manually adjust brightness and contrast using the physical buttons on the monitor. This can be inconvenient, especially if you want to change your monitor settings frequently.

This tool allows you to control your monitor's brightness and contrast directly from your computer. It is particularly useful for reducing the amount of blue light at nighttime, which can help to improve your sleep.

There are very few apps that support this kind of monitor control, which makes this tool a unique solution for those who want more control over their monitor settings.

## Installation

1.  **Install Python:**
    *   Download and install Python from [python.org](https://www.python.org/downloads/).
    *   Make sure to check the box "Add Python to PATH" during installation.

2.  **Install Dependencies:**
    *   Open a command prompt or PowerShell.
    *   Run the following command to install the required `monitorcontrol` library:
        ```
        pip install monitorcontrol
        ```

## Usage

*   Double-click one of the `.bat` files to set your monitor to a predefined brightness and contrast level:
    *   `set-30.bat`: Sets brightness and contrast to 30%.
    *   `set-40.bat`: Sets brightness and contrast to 40%.
    *   `set-75.bat`: Sets brightness and contrast to 75%.

*   You can also run the scripts from the command line and specify a monitor index:
    ```
    set-30.bat 1  // Sets monitor 1 to 30%
    ```

### Advanced Usage

The `monitor_control.py` script can be used directly for more advanced control:

```
# List available monitors
python monitor_control.py list

# Get current settings for monitor 0
python monitor_control.py get 0

# Set brightness to 75% for monitor 0
python monitor_control.py brightness 75 0

# Set contrast to 40% for monitor 0
python monitor_control.py contrast 40 0

# Apply the "reading" preset to monitor 0
python monitor_control.py preset reading 0

# Adjust brightness down by 10% for monitor 0
python monitor_control.py adjust-brightness -10 0
```
