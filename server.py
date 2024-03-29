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
				#client = imgbbpy.SyncClient('f3bab68417be3af86d5abb25a77fec64')
				if testMode == False:
					face = ('/Users/sgm_tech/Documents/sp-interactive/interactive/data/face.jpg')
				else: 
					face = ('/Users/j.rosenbaum/Documents/GitHub/FaceSwap/interactive/data/face.jpg')
				print(face)
				init = face

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

					style_list = ['watercolor', 'oils', 'impasto', 'pastel', 'acrylic', 'charcoal', 'ink', 'pencil', 'marker']
					random_index = random.randint(0, len(style_list) - 1)
					random_style = style_list[random_index]

					#generate a string for the prompt using the prediction results
					promptString = "a " + random_style + " head and shoulders painted portrait of a person, full face, with a neutral expression of a person who is " + terms + " painted by a portrait artist, full face, full head and shoulders, entire head"
					negative = "photograph, photographic, naked, nude, longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality"
					print (promptString)

					#StableDiffusion code for replicate. requires a replicate account and a export code
					def stable_diffusion(prompt, image, scale, n_prompt,):
						model = replicate.models.get("jagilley/controlnet-pose")
						version = model.versions.get("0304f7f774ba7341ef754231f794b1ba3d129e3c46af3022241325ae0c50fb99")
						# https://replicate.com/jagilley/controlnet-hed/versions/cde353130c86f37d0af4060cd757ab3009cac68eb58df216768f907f0d0a0653#input
						inputs = {
							# Input image
							'image': open(image, "rb"),

							# Prompt for the model
							'prompt': prompt,

							# Number of samples (higher values may OOM)
							'num_samples': "1",

							# Image resolution to be generated
							'image_resolution': "512",

							# Steps
							'ddim_steps': 20,

							# Guidance Scale
							# Range: 0.1 to 30
							'scale': scale,

							# Seed
							# 'seed': ...,

							# Canny line detection low threshold
							# Range: 1 to 255
							'low_threshold': 100,

							# Canny line detection high threshold
							# Range: 1 to 255
							'high_threshold': 200,

							# eta (DDIM)
							'eta': 0,

							# Added Prompt
							'a_prompt': "painting, best quality, extremely detailed",

							# Negative Prompt
							'n_prompt': n_prompt,

							# Resolution for detection)
							# Range: 128 to 1024
							'detect_resolution': 512,
						}

						# https://replicate.com/jagilley/controlnet-hed/versions/cde353130c86f37d0af4060cd757ab3009cac68eb58df216768f907f0d0a0653#output-schema
						output = version.predict(**inputs)
						print(output)
						second_url = output[1] # select the second URL from the output list
						request_site = Request(second_url, headers={"User-Agent": "Mozilla/5.0"})
						req = urlopen(request_site)
						arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
						img = cv2.imdecode(arr, -1)
						img = np.array(img)
						dream = cv2.imwrite('interactive/data/dream.jpg', img)

						
						try:
							# download the image, convert it to a NumPy array, and then read
							# it into OpenCV format
							second_url = output[1] # select the second URL from the output list
							request_site = Request(second_url, headers={"User-Agent": "Mozilla/5.0"})
							req = urlopen(request_site)
							arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
							img = cv2.imdecode(arr, -1)
							img = np.array(img)
							dream = cv2.imwrite('interactive/data/dream.jpg', img)

						#NSFW error handling
						except replicate.exceptions.ModelError as e:
							print(e)
							print("Model error")
							default_images = ['dream1.jpg', 'dream2.jpg', 'dream3.jpg', 'dream4.jpg','dream5.jpg', 'dream6.jpg', 'dream7.jpg', 'dream8.jpg', 'dream9.jpg', 'dream10.jpg', 'dream11.jpg', 'dream12.jpg', 'dream13.jpg', 'dream14.jpg', 'dream15.jpg', 'dream16.jpg', 'dream17.jpg', 'dream18.jpg', 'dream19.jpg', 'dream20.jpg', 'dream21.jpg', 'dream22.jpg']
							random_index = random.randint(0, len(default_images) - 1)
							default_image = default_images[random_index]

							default_img = cv2.imread('interactive/data/' + default_image)
							dream = cv2.imwrite('interactive/data/dream.jpg', default_img)
							print('Using random default image')
							# unableToGetMask = b"unableToGetMask"
							# conn.sendall(unableToGetMask)
								
							return dream			
					
					#print ("analysis complete," + analysisComplete) #send as server command
					stable_diffusion(prompt = (promptString), image=face, scale=9, n_prompt=negative)
					conn.sendall(analysisComplete)
					
				
				#conn.sendall(b"analysisComplete,musical&level-headed&visionary&risk-taker&creative")
				print(f'Analysis complete. Mask and Keywords sent.')

			elif splitMessage[0] == 'userSelected':
				#listen for the userSelected message
				userSelected = splitMessage[1]
				promptString = "a " + random_style + " full head and shoulders painted portrait of a person, full face, with a neutral expression of a person who is " + userSelected + " painted by a portrait artist, full face, full head and shoulders, entire head"
				#negative = "NSFW, nude, sexual, sexy, profile, abstract, cropped, animal, cartoon, landscape, food, text, logo"
				print(promptString)

				#StableDiffusion code for replicate. requires a replicate account and a export code
				stable_diffusion(prompt = (promptString), image=face, scale=9, n_prompt=negative)
				print(f'Fetching mask...')
				time.sleep(4)
				print(f'Sending...')                
				conn.sendall(b"cameraMaskReady,window frame name")
				print(f'Analysis complete. Mask and Keywords sent.')

			elif splitMessage[0] == 'connectSyphonServer':
				print(f'Received | Request to connect Syphon Server')
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

					try:
						VideoHandler(video_path=0, img_path='interactive/data/dream.jpg', args=args).start()
					except TypeError as e:
						print(e)
						default_images = ['dream1.jpg', 'dream2.jpg', 'dream3.jpg', 'dream4.jpg','dream5.jpg', 'dream6.jpg', 'dream7.jpg', 'dream8.jpg', 'dream9.jpg', 'dream10.jpg', 'dream11.jpg', 'dream12.jpg', 'dream13.jpg', 'dream14.jpg', 'dream15.jpg', 'dream16.jpg', 'dream17.jpg', 'dream18.jpg', 'dream19.jpg', 'dream20.jpg', 'dream21.jpg', 'dream22.jpg']						
						random_index = random.randint(0, len(default_images) - 1)
						default_image = default_images[random_index]

						default_img = cv2.imread('interactive/data/' + default_image)
						VideoHandler(video_path=0, img_path=default_img, args=args).start()
						
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

