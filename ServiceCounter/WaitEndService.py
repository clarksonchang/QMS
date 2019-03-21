import RPi.GPIO as GPIO
from time import sleep,time
from gpiozero import Button
import json
import requests

endButton = 37
gpiozeroButton = 26
URL = "https://smart-iot-test-05032019.azurewebsites.net/api/LogServiceEndDateTime?code=zifwP2CGhjaG30ie9jueBwtcQXBZ7aMstxudwZqJCo0i7/KKHXcdjg=="

def updateEndService():
    #post json here
    dataJson = {"QueueNumberID":QueueNumberID, "LocationName":"Suva"}
    print("Sending POST Request... : " + str(dataJson))
    r = requests.post(URL, json = dataJson)
    if r.status_code != 200:
        print("Error: "+ str(r.status_code))
    response = r.json()
    print(response)

def WaitEndService(QueueNumberID):
    global QueueNumberID = QueueNumberID
    print("Please rate the service")
    button = Button(gpiozeroButton)
    button.when_pressed = updateEndService()
    print(QueueNumberID)
    

