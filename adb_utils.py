import subprocess
import numpy as np
import pygetwindow as gw
import time
import pyautogui
import psutil
from datetime import datetime
from pynput.mouse import Controller
from pywinauto import Application
from adb_shell.adb_device import AdbDeviceTcp
import win32gui
import win32con

# Mouse Controller
mouse = Controller()

# -----------------------------------------------
# ✅ Function to Start BlueStacks
# -----------------------------------------------

def is_bluestacks_running():
    """Check if BlueStacks process is running."""
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if "HD-Player.exe" in proc.info['name']:
            return True
    return False

def start_bluestacks():
    """Start BlueStacks if not already running."""
    if not is_bluestacks_running():
        try:
            print("[+] Starting BlueStacks...")
            subprocess.Popen(BLUESTACKS_PATH)
        except Exception as e:
            print(f"[-] Failed to start BlueStacks: {e}")
    else:
        print("[+] BlueStacks is already running.")

def Terminate(window_title): 
    try:
        print("process terminating ...")
        app = Application(backend="win32").connect(title=window_title, timeout=10)
        ##pid = app.process
        app.kill()
        print("process terminated ...")
        return True
    except Exception as e:
        print(f"process terminattion faild : {e}") 
        return False

# -----------------------------------------------
# ✅ Function to Manage Windows
# -----------------------------------------------

def is_window_open(window_title):
    windows = gw.getWindowsWithTitle(window_title)
    return len(windows) > 0

def move_and_focus_window(window_title):
    """Move the given window to the top-left corner and bring it to the foreground."""
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        print(f"[-] No window found with title: {window_title}")
        return False

    window = windows[0]
    hwnd = window._hWnd

    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Restore if minimized
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)  # Ensure it's visible
    window.moveTo(0, 0)

    time.sleep(0.1)
    try:
        win32gui.SetForegroundWindow(hwnd)
    except Exception as e:
        print(f"[-] SetForegroundWindow failed: {e}, simulating user interaction...")
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        time.sleep(0.2)
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        pyautogui.click(window.left + window.width // 2, window.top + window.height // 2)

    return True


# -----------------------------------------------
# ✅ ADB Device Connection with Retry
# -----------------------------------------------

def connect_adb(host="127.0.0.1", port=5555, max_retries=3):
    """Connect to BlueStacks via ADB with retry mechanism."""
    device = AdbDeviceTcp(host, port)  # Use AdbDeviceTcp instead of AdbDevice
    
    for attempt in range(max_retries):
        try:
            device.connect()
            if device.available:
                print(f"[+] Connected to BlueStacks (Attempt {attempt+1})")
                return device
        except Exception as e:
            print(f"[-] ADB Connection failed (Attempt {attempt+1}): {e}")
        time.sleep(3)
    
    print("[-] Failed to connect to BlueStacks after multiple attempts.")
    return None


# -----------------------------------------------
# ✅ Install & Uninstall APKs
# -----------------------------------------------

def is_app_installed(package_name):
    """Check if an app is installed on BlueStacks."""
    device = connect_adb()
    if not device:
        print("[-] No ADB device connected.")
        return False

    try:
        output = device.shell("pm list packages")
        installed_packages = output.split("\n")
        return any(f"package:{package_name}" in pkg for pkg in installed_packages)
    except Exception as e:
        print(f"[-] is_app_installed Error: {e}")
        return False

def install_apk(apk_path, package_name):
    """Install an APK on BlueStacks only if not already installed."""
    device = connect_adb()
    if not device:
        return "ADB connection failed."

    if is_app_installed(package_name):
        print(f"[+] {package_name} is already installed.")
        return "Already Installed"

    bluestacks_apk_path = "/data/local/tmp/Haganboy.apk"  # Path inside BlueStacks

    try:
        print(f"[+] Pushing APK to BlueStacks...")
        device.push(apk_path, bluestacks_apk_path)  # ✅ Pass file path, not file object

        print(f"[+] Installing APK from {bluestacks_apk_path}...")
        install_output = device.shell(f"pm install -r {bluestacks_apk_path}")

        print(f"[+] Install output: {install_output}")
        return install_output
    except Exception as e:
        print(f"[-] Install error: {e}")
        return f"[-] Install error: {e}"

def uninstall_apk(package_name):
    """Uninstall an app from BlueStacks."""
    device = connect_adb()
    if not device:
        return "ADB connection failed."

    try:
        uninstall_output = device.shell(f"pm uninstall {package_name}")
        print(f"[+] Uninstalled {package_name}")
        return uninstall_output
    except Exception as e:
        return f"[-] Uninstall Error: {e}"


# -----------------------------------------------
# ✅ Launch App on BlueStacks
# -----------------------------------------------

def launch_app(package_name):
    """Launch an app on BlueStacks."""
    device = connect_adb()
    if not device:
        return "ADB connection failed."

    try:
        device.shell(f"monkey -p {package_name} -c android.intent.category.LAUNCHER 1")
        print(f"[+] Launched {package_name} successfully!")
    except Exception as e:
        print(f"[-] Failed to launch {package_name}: {e}")

def terminate_app(package_name):
    """Force stop a running app in BlueStacks using ADB."""
    device = connect_adb()  # Ensure we have an ADB connection
    if not device:
        return "ADB connection failed."

    try:
        print(f"[+] Terminating {package_name}...")
        device.shell(f"am force-stop {package_name}")  # Force stop the app
        print(f"[+] {package_name} has been terminated.")
        return True
    except Exception as e:
        print(f"[-] Error terminating app: {e}")
        return False

def is_app_running(package_name):
    """Check if an app is currently running on BlueStacks."""
    device = connect_adb()  # Ensure we have an ADB connection
    if not device:
        return False

    try:
        output = device.shell(f"pidof {package_name}")  # Get process ID
        return bool(output.strip())  # If output is not empty, the app is running
    except Exception as e:
        print(f"[-] Error checking if app is running: {e}")
        return False
    
# -----------------------------------------------
# ✅ Screen Resolution 
# -----------------------------------------------

def change_resolution(width, height, dpi=240):
    """Change BlueStacks screen resolution using ADB."""
    device = connect_adb()
    if not device:
        print("[-] ADB connection failed.")
        return False

    try:
        print(f"[+] Setting resolution to {width}x{height} and DPI to {dpi}...")
        device.shell(f"wm size {width}x{height}")  # Change screen size
        device.shell(f"wm density {dpi}")  # Change DPI
        print("[+] Resolution changed successfully!")
        return True
    except Exception as e:
        print(f"[-] Error changing resolution: {e}")
        return False