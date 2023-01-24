# Receiving/Sending from Processing
# Processing to send 'type', 'path', 'keyword,keyword,keyword'(if applicable)
import socket
import imgbbpy
import time
import keras
import tensorflow as tf
import os
import cv2
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import to_categorical
from keras.preprocessing import image
import numpy as np
import pandas as pd  
from matplotlib import pyplot as plt
import matplotlib as mpl
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from csv import writer
from PIL import Image
from skimage import data
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray
import uuid
import logging
import argparse
import replicate
import urllib
import numpy as np
import base64
import json
import socket
import time
import syphonpy
import threading   

import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import Syphon
from Syphon import Server
from urllib.request import urlopen, Request
from face_detection import select_face
from face_swap import face_swap
#from Syserver import main
from grayServer import main
#from syphonpy import Server

testMode = True

HOST = ''              
PORT = 5008

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen(1)
	conn, addr = s.accept()
	with conn:
		print(f'Connected by', addr)
		while True:
			# Receiving from Processing
			data = conn.recv(1024)
			if not data:
				break
			stringdata = data.decode('utf-8')
			print(f'Received | ' + stringdata)

			splitMessage = stringdata.split(',')
					
			# face or userSelected
			if splitMessage[0] == 'cameraNoMask':
				print(f'Removed any existing masks')
				print(f'Sending...')
				conn.sendall(b"cameraNoMaskReady")
			elif splitMessage[0] == 'faceCaptured':
				# Receives face image and uploads file to imgbb
				client = imgbbpy.SyncClient('f3bab68417be3af86d5abb25a77fec64')
				if testMode == False:
					face = client.upload(file='/Users/sgm_tech/Documents/sp-interactive/interactive/data/face.jpg', expiration=600)
				else: 
					face = client.upload(file='/Users/j.rosenbaum/Documents/GitHub/FaceSwap/interactive/data/face.jpg', expiration=600)
				print(face.url)
				init = face.url

				# When prompt is ready, send back to Processing
				print(f'Sending...')
				filelist = ['face.jpg'] #local, 
				for imagefile in filelist:
					img = tf.keras.utils.load_img(imagefile,target_size=(400,400,3))
					img = tf.keras.utils.img_to_array(img)
					img = img/255
				# save the image file to dataset
					img_save = tf.keras.utils.img_to_array(img)
					# unique_filename = str(uuid.uuid4())
					# Saved_img = tf.keras.utils.save_img(unique_filename + '.jpg', img_save, file_format='jpeg',)

					# get the model
					train = pd.read_csv('traitsdataset/train.csv') # don't forget to update this to the dataset
					model = keras.models.load_model('traitsdataset.h5') # don't forget to update this to the dataset
					classes = np.array(train.columns[2:])
					proba = model.predict(img.reshape(1,400,400,3))
					top_6 = np.argsort(proba[0])[:-9:-1]

					terms = str(classes[top_6])
					terms = terms.replace("['", "")
					terms = terms.replace("']", "")
					terms = terms.replace("' '", ", ")
					print (terms)
					
					#create a variable separating all of the terms
					terms = (classes[top_6[0]]) + " " + (classes[top_6[1]]) + " " + (classes[top_6[2]]) + " " + (classes[top_6[3]]) + " " + (classes[top_6[4]]) + " " + (classes[top_6[5]])

					#create a variable with terms separated into bytes
					analysis = (classes[top_6[0]]).encode() + b"&" + (classes[top_6[1]]).encode() + b"&" + (classes[top_6[2]]).encode() + b"&" + (classes[top_6[3]]).encode() + b"&" + (classes[top_6[4]]).encode() + b"&" + (classes[top_6[5]]).encode()
					response = b"analysisComplete,"

					analysisComplete = response + analysis

					#generate a string for the prompt using the prediction results
					promptString = "a head and shoulders portrait of a person, full face, with a neutral expression of a person who is " + terms + " painted by a portrait artist"

					print (promptString)

					#StableDiffusion code for replicate. requires a replicate account and a export code
					def stable_diffusion(prompt, init_image, src_img, prompt_strength):
						prompt = promptString
						model = replicate.models.get("stability-ai/stable-diffusion")
						version = model.versions.get("27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478")
						#version.predict(prompt="a 19th century portrait of a wombat gentleman")
						init_image = init
						prompt_strength = 0.3
						output_url = version.predict(prompt=(promptString), init_image=init)[0]
						print(output_url)
						# download the image, convert it to a NumPy array, and then read
						# it into OpenCV format
						request_site = Request(output_url, headers={"User-Agent": "Mozilla/5.0"})
						req = urlopen(request_site)
						arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
						img = cv2.imdecode(arr, -1) # 'Load it as it is'
						img = np.array(img)
						dream = cv2.imwrite('interactive/data/dream.jpg', img)

						return dream
		
					stable_diffusion(prompt = promptString, init_image=init, src_img='interactive/data/dream.jpg', prompt_strength=0.3)
					
					#print ("analysis complete," + analysisComplete) #send as server command

					conn.sendall(analysisComplete)
				#conn.sendall(b"analysisComplete,musical&level-headed&visionary&risk-taker&creative")
				print(f'Analysis complete. Mask and Keywords sent.')

				 # face swap video from webcam class
				# src_img='interactive/data/dream.jpg'
				# parser = argparse.ArgumentParser(description='FaceSwap Video')
				# parser.add_argument('--src_img', required=False, default=src_img, help='Path for source image')
				# parser.add_argument('--video_path', default=0,help='Path for video')
				# parser.add_argument('--warp_2d', default=False, action='store_true', help='2d or 3d warp')
				# parser.add_argument('--correct_color', default=False, action='store_true', help='Correct color')
				# parser.add_argument('--show', default=False, action='store_true', help='Show')
				# parser.add_argument('--save_path', required=False, default= "test/test.avi", help='Path for storing output video')
				# parser.add_argument('--prompt', type=str, required=False, default = promptString, help='Prompt for generation')
				# parser.add_argument('--strength', type=str, required=False, help='Prompt for generation')
				# parser.add_argument('--init', type=str, default=init, required=False, help='Prompt for generation')
				# args = parser.parse_args()

				# dir_path = os.path.dirname(args.save_path)
				# if not os.path.isdir(dir_path):
				# 	os.makedirs(dir_path)

				# class VideoHandler(object):

				# 	def __init__(self, video_path=0, img_path=None, prompt=None, args=None):
				# 		self.src_points, self.src_shape, self.src_face = select_face(cv2.imread(img_path))
				# 		self.args = args
				# 		self.video = cv2.VideoCapture(video_path)
				# 		self.writer = cv2.VideoWriter(args.save_path, cv2.VideoWriter_fourcc(*'MJPG'), self.video.get(cv2.CAP_PROP_FPS),
				# 									(int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))))

					# def start(self):
						# # window details
						# size = (640, 400)

						# # window setup
						# # server1 = Syphon.Server("Server RGB", size, show=False) # Syphon.Server("window and syphon server name", frame size, show)
						# server2 = Syphon.Server("python", size, show=False)


						# cap = cv2.VideoCapture(0)
						# if cap.isOpened() is False:
						# 	raise("IO Error")
							
						# # loop
						# # while not server1.should_close() and not server2.should_close():
						# while not server2.should_close():
						# 	ret, frame = cap.read() #read camera image
						# 	frame = cv2.resize(frame, size)
						# 	frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #BGR --> RGB
						# 	frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #BGR --> GRAY
						# 	frame_gray = cv2.cvtColor(frame_gray, cv2.COLOR_GRAY2RGB) # GRAY (3 channels)
							
						# 	#cv2.imshow("rgb", frame)
						# 	#server1.draw_and_send(frame_rgb) # Syphon.Server.draw_and_send(frame) draw frame using opengl and send it to syphon
							
						# 	cv2.imshow("python", frame_gray)
						# 	server2.draw_and_send(frame_gray)
								
						# 	if cv2.waitKey(1) & 0xFF == ord('q'):
						# 		break
						# start syphon server
						#size = (640, 400)
						# server = Server("python", size)
						# while self.video.isOpened():
						# 	if cv2.waitKey(1) & 0xFF == ord('q'):
						# 		break
						# 	_, dst_img = self.video.read()
						# 	dst_points, dst_shape, dst_face = select_face(dst_img, choose=False)
						# 	if dst_points is not None:
						# 		dst_img = face_swap(self.src_face, dst_face, self.src_points, dst_points, dst_shape, dst_img, self.args, 68)
						# 	self.writer.write(dst_img)
						# 	#if self.args.show:
						# 	#set window size to 640x480
						# 	height = 480
						# 	width = 640
						# 	cv2.resizeWindow("python", width, height)
						# 	cv2.imshow("python", dst_img)
						# 	# Send the face swapped frame to the Processing sketch
						# 	# server.draw_and_send(dst_img)
					
						# self.video.release()
						# self.writer.release()
						# cv2.destroyAllWindows()

			elif splitMessage[0] == 'userSelected':
				#listen for the userSelected message
				userSelected = splitMessage[1]
				promptString = "a head and shoulders portrait of a person, full face, with a neutral expression of a person who is " + userSelected + " painted by a portrait artist"
				print(promptString)
						
				#StableDiffusion code for replicate. requires a replicate account and a export code
				stable_diffusion(prompt = promptString, init_image=init, src_img='/interactive/data/dream.jpg', prompt_strength=0.3)
				print(f'Fetching mask...')
				time.sleep(4)
				print(f'Sending...')                
				conn.sendall(b"cameraMaskReady,window frame name")
				print(f'Analysis complete. Mask and Keywords sent.')

				main()
				# VideoHandler(args.video_path, args.src_img, args.prompt, args).start()
				
			# 	counter = 0
			# 	while True:
			# 		try:
			# 			# face swap video from webcam class
			# 			VideoHandler(args.video_path, args.src_img, args.prompt, args).start()
			# 		except TypeError:
			# 			counter += 1
			# 			stable_diffusion(prompt = promptString, init_image=init, src_img='/interactive/data/dream.jpg', prompt_strength=0.3)
			# 			print(f'retrying mask...')
			# 			time.sleep(4)
			# 			print(f'Sending...')                
			# 			conn.sendall(b"cameraMaskReady,window frame name")
			# 			print(f'Analysis complete. new Mask and Keywords sent.')
			# 			raise counter
			# 		if counter == 2:
			# 			print(f'using existing mask')
			# 			src_img = '/Users/j.rosenbaum/Documents/GitHub/FaceSwap/interactive/data/dream2.jpg'
			# 			VideoHandler(args.video_path, args.src_img, args.prompt, args).start()
			# 			break        
			# else:
			# 	print(f'Message type not identified')
			# 	conn.sendall(b"messageTypeNotIdentified")

