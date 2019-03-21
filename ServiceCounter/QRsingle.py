from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import RPi.GPIO as GPIO
from time import sleep
import requests
import json
import ast
import subprocess

# Initialization
print("Starting video stream...")
print("Hit CTRL-C to exit program")
vs = VideoStream(src=0).start()
time.sleep(2.0)
buzzer = 21
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer,GPIO.OUT)
global QueueNumberID

# Endpoint for scanning QR
URL = "https://smart-iot-test-05032019.azurewebsites.net/api/VerifyQueueNumber?code=rdTZDFfqNB4eT5AewullaaSb6IILbYNvOWujaStvMcMSsDL1PeQR9Q=="
    
def waitforQR():
    # Loop over frames from the video stream
    while True:
        # Grab the frame from the threaded video stream and resize to maximum width (400 pixels)
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        # Show video frame, can remove when system is packaged nicely
        cv2.imshow("QRScanner", frame)
        key = cv2.waitKey(1) & 0xFF
        # Find singular barcodes in the frame and decode the barcode
        barcodes = pyzbar.decode(frame)
        if len(barcodes) == 1:
            break
    return barcodes

try:
    while True:
        barcodes = waitforQR()
        
        # Process the detected barcode
        for barcode in barcodes:
            # Convert barcodeData from bytes to string, then to JSON
            barcodeData = barcode.data.decode("utf-8")
            barcodeJson = ast.literal_eval(barcodeData)

        # Make buzzer ring upon detection
        GPIO.output(buzzer,GPIO.HIGH)
        sleep(0.4)
        GPIO.output(buzzer,GPIO.LOW)
        
        # Send barcodeData as a POST Request to Azure Function
        print("Sending POST Request... : " + str(barcodeJson))
        r = requests.post(URL, json = barcodeJson)
        if r.status_code != 200:
            print("Error: "+ str(r.status_code))
        response = r.json()
        print(response)
        QueueNumberID = response['QueueNumberID']
        if(response['isSuccess']):
            subprocess.call(["python3", "/home/pi/ServiceCounter/endMultipleButtons.py",str(QueueNumberID)])
        else:
            print("QR code has already been scanned. Freeing up QR Scanner...")
        sleep(5)
        print("QR scanner ready!")
        
except KeyboardInterrupt:  
    print("[INFO] cleaning up...")
    GPIO.cleanup()
    cv2.destroyAllWindows()
    vs.stop()
