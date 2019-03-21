import RPi.GPIO as GPIO
import requests
import json
import time
import argparse
import sys
if 'threading' in sys.modules:
    del sys.modules['threading']

def button_callback_negative(channel):
    global time_stamp
    time_now = time.time()
    if (time_now - time_stamp) >= 0.5: 
        print("[INFO] NEGATIVE Button Pressed")
        dataJson = {"QueueNumberID":QueueNumberID, "LocationName":"Suva", "Rating":0}
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
    
def button_callback_positive(channel):
    global time_stamp
    time_now = time.time()
    if (time_now - time_stamp) >= 0.5: 
        print("[INFO] POSITIVE Button Pressed")
        dataJson = {"QueueNumberID":QueueNumberID, "LocationName":"Suva", "Rating":2}
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
    

print("Service in progress... Please rate the service when done")
URL = "https://smart-iot-test-05032019.azurewebsites.net/api/LogServiceEndDateTime?code=zifwP2CGhjaG30ie9jueBwtcQXBZ7aMstxudwZqJCo0i7/KKHXcdjg=="    
negativeButton = 37
positiveButton = 35
QueueNumberID = int(sys.argv[1]) #toget from args
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(negativeButton,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(positiveButton,GPIO.IN, pull_up_down=GPIO.PUD_UP)
time_stamp = time.time()
GPIO.add_event_detect(negativeButton, GPIO.RISING,callback = button_callback_negative, bouncetime = 500)
GPIO.add_event_detect(positiveButton, GPIO.RISING,callback = button_callback_positive, bouncetime = 500)
try:
    while True : pass
except:
    GPIO.cleanup()
    
    


