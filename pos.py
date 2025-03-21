from pynput import mouse
import time
import math
import subprocess 
import os


click_times = []

# process = subprocess.Popen("urban.exe" , creationflags=subprocess.CREATE_NEW_CONSOLE) 

def on_click(x, y, button, pressed):
    if pressed:
        current_time = time.time()
        click_times.append(current_time)
        
        if len(click_times) > 1:
            duration = click_times[-1] - click_times[-2]
            line_to_append = f'({x},{y},{math.ceil(duration)})\n'
            os.system('cls') 
            print((x,y,math.ceil(duration)))
            with open('log.txt', 'a') as file:
                file.write(line_to_append)

with mouse.Listener(on_click=on_click) as listener:
    listener.join()
