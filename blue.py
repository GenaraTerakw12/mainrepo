import subprocess
import cv2
import numpy as np
import mss
import pygetwindow as gw
import time
import pyautogui
from datetime import datetime
from datetime import timedelta
import random
import pytesseract
#import win32api
#import win32con
#import win32gui
import mss.tools
from PIL import Image
from pynput.mouse import Controller,Button
mouse = Controller()
from pywinauto import Application

window_title = r"BlueStacks App Player"
storeTitle   = r"BlueStacks Store"

instalPath   = r"C:\Users\elnimr\Desktop\blue\blue.exe"
HDPlayerExe  = r"C:\Program Files\BlueStacks_nxt\HD-Player.exe"
HDAdb        = r"C:\Program Files\BlueStacks_nxt\Adb.exe.exe"
apkPath      = r"C:\Users\elnimr\Documents\Unity\Shadow Ops\builds\Shadow_Ops.apk"

instalPath_g   = r"D:\a\mainrepo\mainrepo\blue\blue.exe"
HDPlayerExe_g  = r"C:\Program Files\BlueStacks_nxt\HD-Player.exe"
HDAdb_g        = r"C:\Program Files\BlueStacks_nxt\Adb.exe.exe"
apkPath_g      = r"D:\a\mainrepo\mainrepo\apk\Shadow_Ops.apk"

close_x_position    = 1697 
close_y_position    = 123 
close_x_position_g    = 924 
close_y_position_g    = 155 


skip_x_position    = 191 
skip_y_position    = 156 
skip_x_position_g     = 54 
skip_y_position_g     = 153 

lunch_x_position    = 1317 
lunch_y_position    = 735
lunch_x_position_g    = 785 
lunch_y_position_g    = 545

confirm_x = 1551 ##close popup window controls .
confirm_y = 409
confirm_x_g = 822 
confirm_y_g = 379


progress_bar_height = 4 
toolbar_width       = 40
progress_bar_height_g = 4 
toolbar_width_g       = 40


startTime       = datetime.now()
motion          = False 
isRunningAds    = False  
ad_duration     = timedelta() 

def changeEnveronment():
    global instalPath   
    instalPath = instalPath_g
    global HDPlayerExe  
    HDPlayerExe = HDPlayerExe_g
    global HDAdb        
    HDAdb = HDAdb_g
    global apkPath      
    apkPath = apkPath_g

    global close_x_position   
    close_x_position = close_x_position_g 
    global close_y_position    
    close_y_position= close_y_position_g 

    global skip_x_position    
    skip_x_position = skip_x_position_g 
    global skip_y_position    
    skip_y_position = skip_y_position_g 

    global lunch_x_position       
    lunch_x_position = lunch_x_position_g   
    global lunch_y_position  
    lunch_y_position = lunch_y_position_g   

    global confirm_x 
    confirm_x = confirm_x_g 
    global confirm_y 
    confirm_y = confirm_y_g

    

    

def random_between(min_num, max_num):
    return random.randint(min_num, max_num)

def Click(x,y,duration):
    try:
        pyautogui.click(x,y,duration=duration)
        return True 
    except Exception as e :
        print(f"StartProcess : {e}") 
        return False

def Close(_duration):
    Click(close_x_position,close_y_position,duration=_duration)

def Skip(_duration):
    Click(skip_x_position,skip_y_position,duration=_duration)

def Setup():
    command = [
        instalPath,
        "--defaultImageName", "Tiramisu64",
        "--imageToLaunch", "Tiramisu64"
    ]
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Wait for the process to complete and capture output
        #stdout, stderr = process.communicate()
        # Print the output and error (if any)
        #if stdout:
        #    print("Output:", stdout)
        #if stderr:
        #    print("Error:", stderr)
        # Check the return code
        #if process.returncode != 0:
        #    print(f"Command failed with return code: {process.returncode}")
        #else:
        #    print("Command executed successfully.")
    except Exception as e:
        print(f"Setup : {e}") 
        return False 

    Click(lunch_x_position,lunch_y_position,18)
    Click(lunch_x_position,lunch_y_position,2)
    Click(lunch_x_position,lunch_y_position,120)
    return True 

def StartProcess(path):
    try :
        result = subprocess.Popen(HDPlayerExe) 
        return True 
    except Exception as e:
        print(f"StartProcess : {e}") 
        return False 

def Terminate(title): 
    try:
        app = Application(backend="win32").connect(title=title, timeout=10)
        ##pid = app.process
        app.kill()
        return True
    except Exception as e:
        print(f"Terminate : {e}") 
        return False

def InstallApk(path):
    try :
        result = subprocess.run(['start', '', path], shell=True, check=True) 
        return True 
    except Exception as e:
        return False 
    
def LunchApk(playerPath,packgeName,):
    try :
        result = subprocess.Popen([playerPath,"--instance","Android13","--cmd","launchApp","--package",packgeName])
        return True 
    except Exception as e:
        return False 

def capture_window(title):
    try:
        window = gw.getWindowsWithTitle(title)[0]  # Get window by title
        if not window:
            print(f"⚠️ Window with title '{title}' not found!")
            return None

        with mss.mss() as sct:
            region = {
                "top": window.top, 
                "left": window.left, 
                "width": window.width, 
                "height": window.height
            }
            screenshot = sct.grab(region)
            img = np.array(screenshot)  # Convert to NumPy array
            
            return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)  # Convert to grayscale
    except Exception as e:
        print(f"⚠️ Error capturing window: {e}")
        return None

def Resize(_curr_frame,_prev_frame):   
    if _curr_frame.shape != _prev_frame.shape:
        # Resize frames if necessary
        return cv2.resize(_curr_frame, (_prev_frame.shape[1], _prev_frame.shape[0]))
    else:
        return _curr_frame 


def Difference(_prev_frame,_curr_frame):    
    diff = cv2.absdiff(_prev_frame, _curr_frame)  # Get pixel differences
    return  np.sum(diff)  # Sum of differences
    

def ProgressBar(target_color = [19, 101, 200] , tolerance=25, debug=False):
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        if debug:
            print("Window not found!")
        return None

    window = windows[0]  # Get the first matching window

    # Define the region: bottom 10 pixels of the window
    region = (window.left, window.top + window.height - progress_bar_height, window.width - toolbar_width , 4)
    
    if debug:
        print(f"Capturing region: {region}")

    # Capture the screen region
    screenshot = pyautogui.screenshot(region=region)

    # Convert to NumPy array (RGB format)
    img = np.array(screenshot)

    # Convert RGB to BGR (OpenCV uses BGR format)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Convert to LAB color space (perceptual color distance)
    img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
    target_lab = np.array(cv2.cvtColor(np.uint8([[target_color]]), cv2.COLOR_RGB2Lab))[0][0]

    # Compute the Euclidean distance in LAB color space
    distances = np.linalg.norm(img_lab - target_lab, axis=2)
    

    # Create a mask of pixels that are within the tolerance distance
    mask = distances <= tolerance

    # Calculate percentage of matching pixels
    total_pixels = mask.size
    matching_pixels = np.count_nonzero(mask)
    fill_percentage = (matching_pixels / total_pixels) * 100


    if debug:
        # Highlight detected pixels in red
        debug_img = img.copy()
        debug_img[mask] = [0, 0, 255]  # Set matching pixels to red

        # Show results
        cv2.imshow("Captured Region", img)
        cv2.imshow("Highlighted Pixels", debug_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        print(f"Matching pixels: {matching_pixels}/{total_pixels} ({fill_percentage:.2f}%)")

    return fill_percentage  


def SkipBar(target_color = [18, 151, 255], tolerance=25, debug=False):
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        if debug:
            print("Window not found!")
        return None

    window = windows[0]  # Get the first matching window

    # Define the region: bottom 10 pixels of the window
    region = (window.left, window.top + window.height - progress_bar_height, window.width - toolbar_width , 4)
    
    if debug:
        print(f"Capturing region: {region}")

    # Capture the screen region
    screenshot = pyautogui.screenshot(region=region)

    # Convert to NumPy array (RGB format)
    img = np.array(screenshot)

    # Convert RGB to BGR (OpenCV uses BGR format)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Convert to LAB color space (perceptual color distance)
    img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
    target_lab = np.array(cv2.cvtColor(np.uint8([[target_color]]), cv2.COLOR_RGB2Lab))[0][0]

    # Compute the Euclidean distance in LAB color space
    distances = np.linalg.norm(img_lab - target_lab, axis=2)
    
    # Create a mask of pixels that are within the tolerance distance
    mask = distances <= tolerance

    # Calculate percentage of matching pixels
    total_pixels = mask.size
    matching_pixels = np.count_nonzero(mask)
    fill_percentage = (matching_pixels / total_pixels) * 100


    if debug:
        # Highlight detected pixels in red
        debug_img = img.copy()
        debug_img[mask] = [0, 0, 255]  # Set matching pixels to red

        # Show results
        cv2.imshow("Captured Region", img)
        cv2.imshow("Highlighted Pixels", debug_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        print(f"Matching pixels: {matching_pixels}/{total_pixels} ({fill_percentage:.2f}%)")

    return fill_percentage  

def ProgressMapped(mappingValue=49):
    v1 = ProgressBar() 
    v2 = SkipBar() 
    progressTotal =  v1 + v2 
    return int((progressTotal * 100) / mappingValue)

def main(setup=True, changeToGit = False ):

    if changeToGit :
        changeEnveronment() 

    if setup :
        Setup() 
        time.sleep(2)

        Terminate("BlueStacks Store")
        time.sleep(2)

        StartProcess(HDPlayerExe) 
        time.sleep(30)

        InstallApk(apkPath)
        time.sleep(10) 

        LunchApk(HDPlayerExe,"com.elnimr.shadowops")
        time.sleep(10) 
       
        Click(confirm_x,confirm_y,2) ##close popup window controls .
        time.sleep(1) 
    else:
        LunchApk(HDPlayerExe,"com.elnimr.shadowops")
        time.sleep(1) 

def loop():

    prev_frame = capture_window(window_title)
    time.sleep(1)  # Wait before capturing the next frame

    
    
    while True:
        
        
        
        curr_frame = capture_window(window_title)
        curr_frame = Resize(curr_frame,prev_frame) 
        movement_score = Difference(prev_frame,curr_frame) 

        #print("Score:", movement_score) 

        if movement_score > 100000:  # Threshold for movement detection
            
            
           # ad started 
            if(ProgressMapped() > 10 ) :
                
                if(ProgressMapped() > 95 ):
                    Close(10)
                    Close(6)
                    Close(6)
                    Close(2)
                print("playing ad: ", ProgressMapped() ,"%")
            continue


        prev_frame = curr_frame  # Update previous frame 
        time.sleep(1) 


if __name__ == "__main__":

    main(True,False)
    loop()

    


    


