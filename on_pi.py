import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO

#def on_connect(client, userdata, flags, rc):
#	print("remote connected with result code: ",str(rc))
#	client.subscribe("hello/light")
        #client.subscribe("hello/light2")
        #client.subscribe("hello/fan")
        #client.subscribe("hello/sensor")

#def on_message(client, userdata, msg):
#	print "recived from remote",msg.payload.decode()
	#lc = mqtt.Client("rpi_local")
	#lc.username_pw_set("ximpact","ximpact.in")
	#lc.connect("localhost",1883,60)
#	local_client.publish(msg.topic,msg.payload.decode())

def on_connect_local(client, userdata, flags, rc):
	print("local connected with result code: ",str(rc))
        local_client.subscribe("hello/light")
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(12, GPIO.OUT, initial=0)
#        local_client.subscribe("hello/light2")
#        local_client.subscribe("hello/fan")
#        local_client.subscribe("hello/sensor")

def on_message_local(client, userdata, msg):
	data = msg.payload.decode()
	print data
	if data == "ON":
		GPIO.output(12, GPIO.HIGH)
	else:
		GPIO.output(12, GPIO.LOW)
	#client.publish("ack"+msg.topic,msg.payload.decode())


#client = mqtt.Client("remote_sanket"+time.time().__str__(), clean_session=False)
#client.username_pw_set("ximpact","ximpact.in")
#client.connect("18.188.220.135",1883)
#client.on_connect = on_connect
#client.on_message = on_message
#client.loop_start()


local_client = mqtt.Client("local_sanket"+time.time().__str__(), clean_session=False)
local_client.username_pw_set("ximpact","ximpact.in")
local_client.connect("localhost",1883)
local_client.on_connect = on_connect_local
local_client.on_message = on_message_local
local_client.loop_forever()
#client.loop_forever()
