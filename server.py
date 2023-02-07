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
import queue
import random

import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import Syphon
from Syphon import Server
from urllib.request import urlopen, Request
from face_detection import select_face
import sySwap
from sySwap import VideoHandler
from Syserver import main
#from grayServer import main
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
				filelist = ['interactive/data/face.jpg'] #local, 
				for imagefile in filelist:
					img = tf.keras.utils.load_img(imagefile,target_size=(400,400,3))
					img = tf.keras.utils.img_to_array(img)
					img = img/255
				# save the image file to dataset
					img_save = tf.keras.utils.img_to_array(img)

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
					terms = terms.replace("'''", "")
					print (terms)
					
					#create a variable separating all of the terms
					terms = (classes[top_6[0]]) + " " + (classes[top_6[1]]) + " " + (classes[top_6[2]]) + " " + (classes[top_6[3]]) + " " + (classes[top_6[4]]) + " " + (classes[top_6[5]])

					#create a variable with terms separated into bytes
					analysis = (classes[top_6[0]]).encode() + b"&" + (classes[top_6[1]]).encode() + b"&" + (classes[top_6[2]]).encode() + b"&" + (classes[top_6[3]]).encode() + b"&" + (classes[top_6[4]]).encode() + b"&" + (classes[top_6[5]]).encode()
					response = b"analysisComplete,"

					analysisComplete = response + analysis

					#generate a string for the prompt using the prediction results
					promptString = "a head and shoulders portrait of a person, full face, with a neutral expression of a person who is " + terms + " painted by a portrait artist, full face, full head and shoulders, entire head"
					negative = "NSFW, nude, sexual, sexy, profile, abstract, cropped, animal, cartoon, landscape, food, text, logo, side view, outline, silhouette, contour, shape, form, figure, multiple faces, multiple people, partial faces, partial people, partial body, partial head, partial shoulders, partial neck, partial chest, partial arms, partial hands, partial legs, partial feet, partial hair, partial eyes, partial nose, partial mouth, partial ears, partial eyebrows, partial eyelashes, partial beard, partial mustache,"
					print (promptString)

					#StableDiffusion code for replicate. requires a replicate account and a export code
					def stable_diffusion(prompt, init_image, prompt_strength, negative_prompt):
						prompt = promptString
						model = replicate.models.get("stability-ai/stable-diffusion")
						version = model.versions.get("27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478")
						#version.predict(prompt="a 19th century portrait of a wombat gentleman")
						init_image = init
						prompt_strength = 0.7
						negative = "NSFW, nude, sexual, sexy, profile, abstract, cropped, animal, cartoon, landscape, food, text, logo, side view, outline, silhouette, contour, shape, form, figure, multiple faces, multiple people, partial faces,"
						
						try:
							output_url = version.predict(prompt=(promptString), init_image=init, negative_prompt=(negative), prompt_strength=0.7)[0] #this is the one that parses the information
							print(output_url)
							# download the image, convert it to a NumPy array, and then read
							# it into OpenCV format
							request_site = Request(output_url, headers={"User-Agent": "Mozilla/5.0"})
							req = urlopen(request_site)
							arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
							img = cv2.imdecode(arr, -1) # 'Load it as it is'
							img = np.array(img)
							dream = cv2.imwrite('interactive/data/dream.jpg', img)

						#NSFW error handling
						except replicate.exceptions.ModelError as e:
							print(e)
							print("Model error")
							unableToGetMask = b"unableToGetMask"
							conn.sendall(unableToGetMask)
							return None

						return dream			
					
					#print ("analysis complete," + analysisComplete) #send as server command
					stable_diffusion(prompt = promptString, init_image=init, prompt_strength=0.7, negative_prompt=negative)
					conn.sendall(analysisComplete)
					
				
				#conn.sendall(b"analysisComplete,musical&level-headed&visionary&risk-taker&creative")
				print(f'Analysis complete. Mask and Keywords sent.')

			elif splitMessage[0] == 'userSelected':
				#listen for the userSelected message
				userSelected = splitMessage[1]
				promptString = "a full head and shoulders portrait of a person, full face, with a neutral expression of a person who is " + userSelected + " painted by a portrait artist, full face, full head and shoulders, entire head"
				negative = "NSFW, nude, sexual, sexy, profile, abstract, cropped, animal, cartoon, landscape, food, text, logo"
				print(promptString)

				#StableDiffusion code for replicate. requires a replicate account and a export code
				stable_diffusion(prompt = promptString, init_image=init, prompt_strength=0.7, negative_prompt=negative)
				print(f'Fetching mask...')
				time.sleep(4)
				print(f'Sending...')                
				conn.sendall(b"cameraMaskReady,window frame name")
				print(f'Analysis complete. Mask and Keywords sent.')
				# run videoHandler from the syswap file
				if __name__ == '__main__':
					print('starting sySwap.py')
					logging.basicConfig(level=logging.INFO,
										format="%(levelname)s:%(lineno)d:%(message)s")

					parser = argparse.ArgumentParser(description='FaceSwap Video')
					parser.add_argument('--src_img', required=False, default='interactive/data/dream.jpg',
										help='Path for source image')
					parser.add_argument('--video_path', default=0,
										help='Path for video')
					parser.add_argument('--warp_2d', default=False, action='store_true', help='2d or 3d warp')
					parser.add_argument('--correct_color', default=False, action='store_true', help='Correct color')
					parser.add_argument('--show', default=False, action='store_true', help='Show')
					parser.add_argument('--save_path', required=False, default="test/test.avi", help='Path for storing output video')
					args = parser.parse_args()

					dir_path = os.path.dirname(args.save_path)
					if not os.path.isdir(dir_path):
						os.makedirs(dir_path)

					
					VideoHandler(video_path=0, img_path='interactive/data/dream.jpg', args=args).start()

						#VideoHandler.self.stopped = True
					#add timeout code for cv2.imshow
					#cv2.waitKey(5000)

			elif splitMessage[0] == 'videoCaptured':
					print('videoCaptured')
					#listen for the userSelected message
					#quit videoHandler
					print('stopping videoHandler')
					#VideoHandler.self.stopped = True
					#close window
					#glfw.destroy_window(window=server2.window)
			else:
				print('message not recognized')




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

