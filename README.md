# Monitor Firefox Process on Idle Monitor

This Python script is designed to monitor the activity of the user's system and terminate all running instances of the Firefox browser when the monitor is idle (e.g., powered off or in sleep mode). It logs all actions to the terminal, providing a simple yet effective solution for managing processes based on monitor activity.

Use firefoxkiller.exe to run the program in the background. You can run it together with Windows startup.
Use firefoxkillercmd.exe to see log files in the terminal.

## Features

- **Idle Detection**: The script uses Windows API to determine the system's idle time (time since the last user interaction such as keyboard or mouse input). If the idle time exceeds a specified threshold, the monitor is considered idle or powered off.
- **Firefox Termination**: If the monitor is idle, the script identifies and terminates all running processes of Firefox.
- **Real-time Monitoring**: The script checks the monitor's activity status every second and logs all events and actions to the terminal.
- **Cross-process Handling**: It ensures that all instances of Firefox (if multiple processes are running) are terminated.
- **User-friendly Logs**: Logs are displayed in the terminal with timestamps for easier debugging and monitoring.

## Requirements

- **Python 3.6+**
- Required Python libraries:
  - `psutil`: For process management.
  - `ctypes`: For accessing Windows API.

Install the dependencies using:
```bash
pip install psutil
