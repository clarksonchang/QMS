from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import RPi.GPIO as GPIO
from time import sleep

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
	help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())


#initialization
print("Starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
buzzer = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer,GPIO.OUT)

# open the output CSV file for writing and initialize the set of
# barcodes found thus far
csv = open(args["output"], "w")
found = set()

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it to
	# have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	# find the barcodes in the frame and decode each of the barcodes
	barcodes = pyzbar.decode(frame)

# Go through all detected barcodes
	for barcode in barcodes:
		# Extract boundary box coordinates and use to draw a red box
		(x, y, w, h) = barcode.rect
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # Convert barcodeData from bytes to string
		barcodeData = barcode.data.decode("utf-8")
		barcodeType = barcode.type
		# Display the barcode data on the video stream
		text = "{} ({})".format(barcodeData, barcodeType)
		cv2.putText(frame, text, (x, y - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		# Activate buzzer sound
		GPIO.output(buzzer,GPIO.HIGH)
		sleep(1)
		GPIO.output(buzzer,GPIO.LOW)
		# if the barcode text is currently not in our CSV file, write
		# the timestamp + barcode to disk and update the set
		if barcodeData not in found:
			csv.write("{},{}\n".format(datetime.datetime.now(),
				barcodeData))
			csv.flush()
			found.add(barcodeData)
# Show video frame
	cv2.imshow("Barcode Scanner", frame)
	key = cv2.waitKey(1) & 0xFF
	# Press Q to quit
	if key == ord("q"):
		break
# Close CSV file
print("[INFO] cleaning up...")
csv.close()
cv2.destroyAllWindows()
vs.stop()