import discord
from discord.ext import commands
import json
import threading
import cv2 as cv

with open("settings.json", "r") as read_file:
	data = json.load(read_file)

client = commands.Bot(command_prefix=data['prefix'])

cap = cv.VideoCapture(0)

haar_cascade = cv.CascadeClassifier('haar_face.xml')

ready_to_send = False

def face_detection():
	global cap
	global haar_cascade
	global client
	global ready_to_send
	while True:
    		ret, frame = cap.read()
    		
    		gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    		
    		face_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
    		
    		for (x,y,w,h) in face_rect:
    			cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), thickness=2)
    			
    		cv.imshow('Cam view', frame)
    		
    		if cv.waitKey(1) & 0xFF == ord('q'):
        		break
        		
    		if len(face_rect) > 0:
    			break
    			
	cv.imwrite('intruder.jpg', frame)
	cap.release()
	cv.destroyAllWindows()
	ready_to_send = True

main_thread = threading.Thread(target=face_detection)

async def send_file():
	channel = client.get_channel(data['channel_id'])
	global ready_to_send
	while True:
		if ready_to_send:
			await channel.send(data['message'], file=discord.File(r'intruder.jpg'))
			ready_to_send = False
			break

@client.event
async def on_ready():
  print('I am ready')
  main_thread.start()
  client.loop.create_task(send_file())

token = data['token']
client.run(token)
