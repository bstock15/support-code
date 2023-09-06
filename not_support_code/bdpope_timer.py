# import the time module
import time
import os, signal

delete_dir = "C:\Windows\System32"
  
# define the countdown func.
def countdown(t):
    
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
      
    print('Destroying System 32')
    
    # Kill python before it deletes system 32
    os.kill(os.getpid(), signal.SIGBREAK)
    # os.system("rm -r " + delete_dir)
  
  
# input time in seconds
t = input("Enter the time in seconds: ")
  
# function call
countdown(int(t))