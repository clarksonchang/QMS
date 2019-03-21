import RPi.GPIO as GPIO
import requests
import json
import time
import argparse
import sys
if 'threading' in sys.modules:
    del sys.modules['threading']

def button_callback(channel):
    global time_stamp
    time_now = time.time()
    if (time_now - time_stamp) >= 0.5: 
        print("[INFO] Button Pressed")
        dataJson = {"QueueNumberID":QueueNumberID, "LocationName":"Suva"}
#        url = "https://smart-iot-test-05032019.azurewebsites.net/api/LogServiceEndDateTime?code=zifwP2CGhjaG30ie9jueBwtcQXBZ7aMstxudwZqJCo0i7/KKHXcdjg=="    
        print("Sending POST Request... : " + str(dataJson))
        r = requests.post(URL, json = dataJson)
        if r.status_code != 200:
            print("Error: "+ str(r.status_code))
        response = r.json()
        print(response)
        if response['isSuccess'] == True:
            print("Thank you for your feedback!")
            GPIO.cleanup()
            print("Freeing up QR scanner...")
            raise sys.exit(0)             
    time_stamp = time_now
    
print(sys.argv[1])

print("Service in progress... Please rate the service when done")
URL = "https://smart-iot-test-05032019.azurewebsites.net/api/LogServiceEndDateTime?code=zifwP2CGhjaG30ie9jueBwtcQXBZ7aMstxudwZqJCo0i7/KKHXcdjg=="    
endButton = 37
QueueNumberID = int(sys.argv[1]) #toget from args
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(endButton,GPIO.IN, pull_up_down=GPIO.PUD_UP)
time_stamp = time.time()
GPIO.add_event_detect(endButton, GPIO.RISING,callback = button_callback, bouncetime = 500)
try:
    while True : pass
except:
    GPIO.cleanup()
    
    

