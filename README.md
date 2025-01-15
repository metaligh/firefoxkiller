# Monitor Firefox Process on Idle Monitor v1.2

![FirefoxKiller](https://i.ibb.co/6m2DRnS/ff.webp)

In Windows 11 24H2, when Firefox is running, the `wma.exe` process can consume CPU resources when the screen is turned off or the computer is locked. To prevent this, the script monitors power setting changes and terminates all running Firefox instances when the screen turns off.

This Python script listens for power setting notifications related to the monitor's activity (screen on/off). If the monitor turns off (screen goes to sleep), the script automatically closes all Firefox processes. It logs all actions, providing an easy-to-use solution to manage Firefox based on the monitor’s state.

Use `firefoxkiller.exe` to run the program in the background. You can configure it to start automatically with Windows.

Use `firefoxkillercmd.exe` to view logs in the terminal.

[Release Page](https://github.com/metaligh/firefoxkiller/releases/tag/1.2)

## Features

- **Monitor Power Settings**: The script listens for power setting changes related to the monitor and system (e.g., screen turning off).
- **Firefox Process Termination**: When the screen is turned off, the script automatically terminates all running Firefox processes (`firefox.exe`).
- **Logging**: The script logs important events, including power setting changes and actions taken (such as terminating Firefox processes), into a log file (`firefoxkiller.log`).

## Requirements

- **Python 3.x** (preferably)
- **Windows OS**: The script uses `win32api`, `win32con`, `win32gui`, and `psutil` libraries to interact with the operating system.

## Dependencies

- **pywin32**: For Windows API interaction.
- **psutil**: For process management (terminating Firefox processes).
- **comtypes**: For handling GUIDs.

Install dependencies using:

```bash
pip install pywin32 psutil comtypes
