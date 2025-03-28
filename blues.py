import adb_utils 
from adb_utils import start_bluestacks, is_app_installed, install_apk, is_app_running, launch_app, is_window_open , move_and_focus_window
import time 

# BlueStacks Config
BLUESTACKS_PATH = r"C:\Program Files\BlueStacks_nxt\HD-Player.exe --instance Tiramisu64"
WINDOW_TITLE = "BlueStacks App Player"


# -----------------------------------------------
# ✅ Main Logic - Monitor & Restart BlueStacks
# -----------------------------------------------
def monitor_bluestacks():

    while True:

        if not is_window_open(WINDOW_TITLE):
            print("[-] BlueStacks crashed or closed. Restarting...")
            start_bluestacks()

        move_and_focus_window(WINDOW_TITLE)


        time.sleep(2)  



if __name__ == "__main__":
    print("[+] Initializing BlueStacks automation...")

    start_bluestacks()
    time.sleep(15)  # Allow time for BlueStacks to fully load
    
    package_name = "com.elnimr.haganboy"

    if not is_app_installed(package_name):
        install_apk(r"C:\Users\elnimr\Desktop\mainRepo\mainrepo\apk\Haganboy.apk", package_name)
        time.sleep(10)

    if not is_app_running(package_name):
        #launch_app(package_name)
        print("[+] application not running")

    # Example Usage
    #package_name = "com.elnimr.shadowops"
    #uninstall_apk(package_name)

    #package_name = "com.elnimr.haganboy"
    #Install APK (Uncomment if needed)
    #install_apk(r"C:\Users\elnimr\Desktop\mainRepo\mainrepo\apk\Haganboy.apk", package_name)

    #time.sleep(15) 
    
    #uninstall_apk(package_name)

    # Launch App (Uncomment if needed)
    #package_name = "com.elnimr.haganboy"
    #launch_app(package_name)
    #terminate_app(package_name)
    # Start Monitoring
    monitor_bluestacks()