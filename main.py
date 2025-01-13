import time
import psutil
from datetime import datetime
import ctypes

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

def log(message):
    """Logs messages with a timestamp to the terminal."""
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")

def get_idle_time():
    """Gets the system idle time in seconds."""
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000.0
    else:
        log("Failed to get the last input time.")
        return 0

def kill_firefox():
    """Terminates all Firefox processes if they are running."""
    firefox_found = False
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and "firefox" in proc.info['name'].lower():
                proc.terminate()
                log(f"Terminated Firefox process with PID {proc.pid}.")
                firefox_found = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    if firefox_found:
        return True
    return False


def monitor():
    """Main monitoring loop."""
    log("Starting monitoring.")
    idle_threshold = 60  # Consider the monitor off if idle for more than 60 seconds

    try:
        while True:
            idle_time = get_idle_time()

            if idle_time > idle_threshold:
                log("Monitor is off. Checking Firefox.")
                if kill_firefox():
                    log("Firefox was found and terminated.")
                else:
                    log("Firefox was not found.")
            else:
                log("Monitor is on. Doing nothing.")

            time.sleep(1)  # Check every second

    except KeyboardInterrupt:
        log("Monitoring stopped by user.")

if __name__ == "__main__":
    monitor()
