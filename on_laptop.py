import numpy as np
import argparse
import cv2
import os
import paho.mqtt.client as mqtt
import time


class flg:
	start = 1


def on_connect(client, userdata, flags, rc):
	print("connected with result code: ",str(rc))

def on_message(client, userdata, msg):
	print("started")
	if msg.payload.decode() == "ON":
		flg.start = 1
	else:
		flg.start = 0	
	print(msg.payload.decode(),flg.start)


print "Connecting RPi..."
lc = mqtt.Client("sensor")
lc.username_pw_set("ximpact","ximpact.in")
lc.connect("192.168.43.4",1883,60)
lc.on_connect = on_connect
lc.on_message = on_message
lc.loop_start()


time.sleep(1)
conf = 0.57

print("loading model...")
net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")

cap=cv2.VideoCapture(1)

main_cnt_on = 0
main_cnt = 0
switch = 0




while True:
	if flg.start == 1:
		_, image=cap.read()
		(h, w) = image.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
		net.setInput(blob)
		detections = net.forward()
		human = 0
		for i in np.arange(0, detections.shape[2]):
			confidence = detections[0, 0, i, 2]
			os.system("clear")
			if confidence > conf:
				idx = int(detections[0, 0, i, 1])
				print idx
				if idx==15:
					human+=1
					box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
					(startX, startY, endX, endY) = box.astype("int")
					
					label = "person"+(confidence * 100).__str__()
					cv2.rectangle(image, (startX, startY), (endX, endY), [0,0,255], 2)
					y = startY - 15 if startY - 15 > 15 else startY + 15
					cv2.putText(image, label, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,255], 2)
		print human	
		if human>=1:
			if switch == 0:
				main_cnt += 1
				if main_cnt > 12:
					lc.publish("hello/light","ON")
					switch = 1
					main_cnt = 0
					main_cnt_on = 0
		
		else:
			if switch == 1:
				main_cnt_on += 1
				if main_cnt_on > 30:
					lc.publish("hello/light","OFF")
					switch = 0
					main_cnt = 0
					main_cnt_on = 0
		#print(human)
		cv2.imshow('Original',image)
		#lc.publish("hello/light","OFF")
		k=cv2.waitKey(30) & 0xFF
		if k==27:
			lc.publish("hello/light","OFF")
			break
	else:
		#os.system("clear")
		print("Sensor is diabled")
		main_cnt_on = 0
		main_cnt = 0
		switch = 0


		
