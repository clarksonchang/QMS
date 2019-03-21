import RPi.GPIO as GPIO
import time
import requests
import json
import sys

counterNumber = 4
print("Press button to call the next number in line")

def button_callback(channel):
    global time_stamp
    time_now = time.time()
    if (time_now - time_stamp) >= 0.5: 
        print("Calling next queue number...")
        url = "https://smart-iot-test-05032019.azurewebsites.net/api/GetLatestQueueNumber?code=8d2hWbRMadjSi9R1Uoujaw3bydwgCYLNpiJ1js99UBAtnSZLa67cnQ=="
        r = requests.post(url, json = data)
        if r.status_code != 200:
            print("Error: "+ r.status_code)
        response = r.json()
        print("-----------------NOTIFICATION--------------------------------")
        print("Queue number called: " + str(response["QueueNumber"]))
        print("Counter number: " + str(response["CounterNumber"]))
    time_stamp = time_now

try:        
    data = {"LocationName": "Suva", "CounterNumber": counterNumber}
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    time_stamp = time.time()
    GPIO.add_event_detect(33,GPIO.RISING,callback = button_callback, bouncetime = 500)
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    sys.exit("[INFO] Cleaning up...")
finally:
    GPIO.cleanup()
    
