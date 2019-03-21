import RPi.GPIO as GPIO
import time
import requests
import json
from Libraries.thermalprinter.ticket import makeTicket
from Libraries.thermalprinter.Adafruit_Thermal import Adafruit_Thermal
import sys

def button_callback(channel):
    global time_stamp
    time_now = time.time()
    if (time_now - time_stamp) >= 0.5: 
        print("Fetching queue number from server...")
        url = "https://smart-iot-test-05032019.azurewebsites.net/api/IssueQueueNumber?code=1DdHilageHyrrel9XKBItYVxU3c3r2NGtnu5EZDvqrIgOM1Fm/LE7Q=="
        r = requests.post(url, json = data)
        if r.status_code != 200:
            print("Error: "+ r.status_code)
        response = r.json()
        print(response)
        makeTicket(printer, response)
    time_stamp = time_now
    
try:
    global printer
    data = {"LocationName": "Suva"}
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    printer = Adafruit_Thermal("/dev/serial0", 9600, timeout=3000)
    time_stamp = time.time()

    print("[INFO] Ticket Dispenser initialized")
    GPIO.add_event_detect(13,GPIO.RISING,callback = button_callback, bouncetime = 500)
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    sys.exit("[INFO] Cleaning up...")
finally:
    GPIO.cleanup()

    
