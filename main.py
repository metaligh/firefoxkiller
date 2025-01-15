import ctypes
import win32api
import win32con
import win32gui
import time
import os
import psutil
from ctypes import Structure, c_uint, c_void_p, POINTER
from comtypes import GUID
import uuid

PBT_POWERSETTINGCHANGE = 0x8013


# Структура для хранения данных, передаваемых через lparam
class POWERBROADCAST_SETTING(Structure):
    _fields_ = [("PowerSetting", c_void_p),  # Указатель на GUID настройки
                ("DataLength", c_uint),  # Длина данных
                ("Data", c_void_p)]  # Указатель на данные (состояние устройства)


def log_info(msg):
    """Логирование в файл"""
    print(msg)
    with open("test.log", "a+") as f:
        f.write(msg + "\n")


def terminate_firefox_processes():
    """Завершаем все процессы firefox.exe"""
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == 'firefox.exe':
            try:
                proc.terminate()
                log_info(f"Terminated firefox process with PID {proc.info['pid']}")
            except psutil.NoSuchProcess:
                log_info(f"Process {proc.info['pid']} already terminated.")


def process_power_setting_change(lparam):
    """Обработка изменения настроек питания"""
    # Попробуем использовать ctypes.cast для приведения lparam к указателю на структуру
    setting = ctypes.cast(lparam, POINTER(POWERBROADCAST_SETTING))

    # Разбираем данные в lparam
    power_setting_guid = setting.contents.PowerSetting
    data_length = setting.contents.DataLength
    data = setting.contents.Data

    # Преобразуем GUID в строковый вид (если это GUID, а не числовое значение)
    power_setting_guid_str = str(uuid.UUID(int=power_setting_guid))

    # Логируем GUID
    log_info(f"Power Setting GUID: {power_setting_guid_str}")

    # Если данные равны 4, экран погас
    if data_length > 0:
        if data == 4:
            log_info("Screen turned off. Terminating firefox processes.")
            terminate_firefox_processes()  # Закрыть все процессы Firefox


def wndproc(hwnd, msg, wparam, lparam):
    """Обработка сообщений"""
    if msg == win32con.WM_POWERBROADCAST:
        if wparam == PBT_POWERSETTINGCHANGE:
            log_info('Power setting changed...')
            try:
                process_power_setting_change(lparam)  # Обработка данных из lparam
            except Exception as e:
                log_info(f"Error processing power setting change: {e}")
                return 0

    return 0


def main():
    """Главная функция для запуска обработчика сообщений"""
    log_info("*** STARTING ***")

    # Инициализация окна
    hinst = win32api.GetModuleHandle(None)
    wndclass = win32gui.WNDCLASS()
    wndclass.hInstance = hinst
    wndclass.lpszClassName = "testWindowClass"
    messageMap = {win32con.WM_POWERBROADCAST: wndproc}
    wndclass.lpfnWndProc = messageMap

    try:
        myWindowClass = win32gui.RegisterClass(wndclass)
        hwnd = win32gui.CreateWindowEx(win32con.WS_EX_LEFT,
                                       myWindowClass,
                                       "testMsgWindow",
                                       0,
                                       0,
                                       0,
                                       win32con.CW_USEDEFAULT,
                                       win32con.CW_USEDEFAULT,
                                       0,
                                       0,
                                       hinst,
                                       None)
    except Exception as e:
        log_info("Exception: %s" % str(e))

    if hwnd is None:
        log_info("hwnd is none!")
    else:
        log_info(f"Window created successfully with hwnd: {hwnd}")

    # Регистрация уведомлений для изменений настроек питания (монитор, система и т.д.)
    register_function = ctypes.windll.user32.RegisterPowerSettingNotification

    guids_info = {
        'GUID_MONITOR_POWER_ON': '{02731015-4510-4526-99e6-e5a17ebd1aea}',
        'GUID_SYSTEM_AWAYMODE': '{98a7f580-01f7-48aa-9c0f-44352c29e5C0}',
    }

    hwnd_pointer = ctypes.cast(hwnd, ctypes.c_void_p)  # Используем cast для приведения типа hwnd
    for name, guid_info in guids_info.items():
        result = register_function(hwnd_pointer, GUID(guid_info), 0)
        log_info(f"Registering {name} - result: {result}")

    log_info("\nEntering loop...")
    # Основной цикл для обработки сообщений
    while True:
        win32gui.PumpWaitingMessages()
        time.sleep(1)


if __name__ == "__main__":
    main()
