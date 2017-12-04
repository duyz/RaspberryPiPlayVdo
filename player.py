import sys
import time
import subprocess
import RPi.GPIO as GPIO

default_path = "/home/pi/Videos/default.mp4"
vdo1_path = "/home/pi/Videos/vdo1.mp4"
vdo2_path = "/home/pi/Videos/vdo2.mp4"
vdo3_path = "/home/pi/Videos/vdo3.mp4"

BTNS = [17, 4, 3, 2] #2 exit program
LAMPS = [10, 22, 27]

process = None
curVdo = None

#============ Setup GPIO ============
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for btn in BTNS:
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

for lamp in LAMPS:
        GPIO.setup(lamp, GPIO.OUT)
        GPIO.output(lamp, True)
#====================================

def play(vdo):
    global process, curVdo
    try:
        if not process is None and process.poll() is None:
            process.stdin.write('q')
            curVdo = None
            time.sleep(0.5)        
        #process = subprocess.Popen(['omxplayer','--win','20,20,200,100',vdo],stdin=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
        process = subprocess.Popen(['omxplayer','-b','--no-osd','-o','hdmi',vdo],stdin=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
        curVdo = vdo
    except:
        None

while True:
    
    if process is None or not process.poll() is None:
        time.sleep(1)
        play(default_path)
        GPIO.output(LAMPS[0], True)
        GPIO.output(LAMPS[1], True)
        GPIO.output(LAMPS[2], True)

    if(GPIO.input(BTNS[0]) == False):
        time.sleep(1)
        play(vdo1_path)
        GPIO.output(LAMPS[0], False)
        GPIO.output(LAMPS[1], True)
        GPIO.output(LAMPS[2], True)
        
    elif(GPIO.input(BTNS[1]) == False):
        time.sleep(1)
        play(vdo2_path)
        GPIO.output(LAMPS[0], True)
        GPIO.output(LAMPS[1], False)
        GPIO.output(LAMPS[2], True)

    elif(GPIO.input(BTNS[2]) == False):
        time.sleep(1)
        play(vdo3_path)
        GPIO.output(LAMPS[0], True)
        GPIO.output(LAMPS[1], True)
        GPIO.output(LAMPS[2], False)
        
    elif(GPIO.input(BTNS[3]) == False):
        time.sleep(1)
        process.stdin.write('q')
        GPIO.output(LAMPS[0], True)
        GPIO.output(LAMPS[1], True)
        GPIO.output(LAMPS[2], True)
        break
        
    time.sleep(0.01)

GPIO.cleanup()

