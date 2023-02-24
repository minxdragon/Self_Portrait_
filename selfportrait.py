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
import random

from urllib.request import urlopen, Request
from face_detection import select_face
from face_swap import face_swap

# ### Face detection
#import the cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def TakeSnapshotAndSave():
	# access the webcam (every webcam has a number, the default is 0)
	cap = cv2.VideoCapture(0)

	num = 0 
	while num<1:
		# Capture frame-by-frame
		frameWidth = 640
		frameHeight = 480
		cap = cv2.VideoCapture(0)
		cap.set(3, frameWidth)
		cap.set(4, frameHeight)
		cap.set(10,100)

		while cap.isOpened():
			success, img = cap.read()
			if success:
				cv2.imshow("Result", img)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break
					
				# to detect faces in video
				# Convert into grayscale
				gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

				# Load the cascade
				face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

				# Detect faces
				faces = face_cascade.detectMultiScale(gray, 1.1, 4)

				# Draw rectangle around the faces and crop the faces
				for (x, y, w, h) in faces:
					center_x = x + w/2
					center_y = y + h/2
					# adjust the crop size and position to center the face
					crop_size = min(w, h) * 1.5
					crop_x = int(center_x - crop_size/2)
					crop_y = int(center_y - crop_size/2)
					faces = img[crop_y:crop_y + int(crop_size), crop_x:crop_x + int(crop_size)]

					cv2.imshow("face", faces)
					cv2.imwrite('opencv'+str(num)+'.jpg', faces)
					
			else:
				break

		# Release the capture and destroy all windows
		cap.release()
		cv2.destroyAllWindows()
			
		# Display the output
		#cv2.imwrite('face.jpg', faces)
		#cv2.imshow('img', img)
		#cv2.waitKey()

		#older code after
		x = 100
		y = 100
		text_color = (0,255,0)

		cv2.imwrite('face.jpg',faces)
		cv2.namedWindow("output", cv2.WINDOW_AUTOSIZE)    # Create window with freedom of dimensions
		im = cv2.imread('opencv0.jpg')                    # Read image
		#imS = cv2.resize(im, (940, 540))                # Resize image
		cv2.imshow("output", im)                       # Show image
		cv2.waitKey(0)                                  # Display the image infinitely until any keypress
		num = num+1
		
	# When everything done, release the capture

	cap.release()
	cv2.destroyAllWindows()

## Classification
def selfPortrait():
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

		#define list here
		var_holder = {}
		prediction_0 = None
		prediction_1 = None
		prediction_2 = None
		prediction_3 = None
		prediction_4 = None
		prediction_5 = None
		for i in range(6):
			var_holder['prediction_' + str(i)] = "{:.3}".format(proba[0][top_6[i]]*100) #top 6 order
			#var_holder['prediction_' + str(i)] = "{:.3}".format(proba[0][i]*100) #for natural order
			map(lambda var_holder: var_holder.replace('+' , '.'), var_holder)
			print("{}".format(classes[top_6[i]])+" ({:.3})".format(proba[0][top_6[i]]*100))

			# for key in var_holder.keys():
			#     holder_clean = proba.replace('.', var_holder['+'])

		#print(var_holder)
		#break the results into separate variables for formatting
		locals().update(var_holder)
		map(lambda var_holder: var_holder.replace('+' , '.'), var_holder)
		#create a variable with terms separated into the top three results
		analysisComplete = str(classes[top_6[0]]) + "&" + str(classes[top_6[1]]) + "&" + str(classes[top_6[2]]) + "&" + str(classes[top_6[3]]) + "&" + str(classes[top_6[4]]) + "&" + str(classes[top_6[5]])
		# create a variable with terms separated into the bottom three results

		#generate a string for the prompt using the prediction results
		#promptString = "a head and shoulders portrait of a person, full face, with a neutral expression of a person who is " + analysisComplete + " painted by a portrait artist"

		

	### Face swap
	#will come from imagebb
	facefile = ()

	userSelected = None #convert array to string
	style_list = ['watercolor', 'oils', 'impasto', 'pastel', 'acrylic', 'charcoal', 'ink', 'pencil', 'marker']
	random_index = random.randint(0, len(style_list) - 1)
	random_style = style_list[random_index]
	chosenTerms = "intuitive, creative, conceptual, surreal"
	#promptString = "a " + random_style + " full head and shoulders portrait of a person, full face, with a neutral expression of a person who is " + chosenTerms + " painted by a portrait artist"
	promptString = "a " + random_style + " full head and shoulders portrait of a person, full face, with a neutral expression of a person who is " + analysisComplete + " painted by a portrait artist"
	print (promptString)
	# face swap video from webcam class
	class VideoHandler(object):

		def __init__(self, video_path=0, img_path=None, prompt=None, args=None):
			self.src_points, self.src_shape, self.src_face = select_face(cv2.imread(img_path))
			self.args = args
			self.video = cv2.VideoCapture(video_path)
			self.writer = cv2.VideoWriter(args.save_path, cv2.VideoWriter_fourcc(*'MJPG'), self.video.get(cv2.CAP_PROP_FPS),
										(int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))))

		def start(self):
			# Create a syphon client
			# client = Client()
			while self.video.isOpened():
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break

				_, dst_img = self.video.read()
				dst_points, dst_shape, dst_face = select_face(dst_img, choose=False)
				if dst_points is not None:
					dst_img = face_swap(self.src_face, dst_face, self.src_points, dst_points, dst_shape, dst_img, self.args, 68)
				self.writer.write(dst_img)
				# Send the frame to Syphon
				# client.publish(frame)
				#if self.args.show:
				cv2.imshow("Video", dst_img)

			self.video.release()
			self.writer.release()
			cv2.destroyAllWindows()

	#load the initial image. currently static, will make dynamic later
	filename = 'https://res.cloudinary.com/dj1ptpbol/image/upload/v1667791534/opencv0_o7mtqy.jpg' #Init image URL currently fixed, will make dynamic later

	if __name__ == '__main__':
		logging.basicConfig(level=logging.INFO,
							format="%(levelname)s:%(lineno)d:%(message)s")

	# argument parser for terminal input
		parser = argparse.ArgumentParser(description='FaceSwap Video')
		parser.add_argument('--src_img', required=False, default='interactive/data/dream.jpg', help='Path for source image')
		parser.add_argument('--video_path', default=0,help='Path for video')
		parser.add_argument('--warp_2d', default=False, action='store_true', help='2d or 3d warp')
		parser.add_argument('--correct_color', default=False, action='store_true', help='Correct color')
		parser.add_argument('--show', default=False, action='store_true', help='Show')
		parser.add_argument('--save_path', required=False, default= "test/test.avi", help='Path for storing output video')
		parser.add_argument('--prompt', type=str, required=False, default = promptString, help='Prompt for generation')
		parser.add_argument('--strength', type=str, required=False, help='Prompt for generation')
		parser.add_argument('--init', type=str, default=filename, required=False, help='Prompt for generation')
		args = parser.parse_args()

		dir_path = os.path.dirname(args.save_path)
		if not os.path.isdir(dir_path):
			os.makedirs(dir_path)

		#StableDiffusion code for replicate. requires a replicate account and a export code
		def stable_diffusion(prompt, image, scale, n_prompt,):
			model = replicate.models.get("jagilley/controlnet-depth2img")
			version = model.versions.get("922c7bb67b87ec32cbc2fd11b1d5f94f0ba4f5519c4dbd02856376444127cc60")
			# https://replicate.com/jagilley/controlnet-hed/versions/cde353130c86f37d0af4060cd757ab3009cac68eb58df216768f907f0d0a0653#input
			inputs = {
				# Input image
				'image': open("face.jpg", "rb"),

				# Prompt for the model
				'prompt': promptString,

				# Number of samples (higher values may OOM)
				'num_samples': "1",

				# Image resolution to be generated
				'image_resolution': "512",

				# Steps
				'ddim_steps': 20,

				# Guidance Scale
				# Range: 0.1 to 30
				'scale': 9,

				# Seed
				# 'seed': ...,

				# eta (DDIM)
				'eta': 0,

				# Added Prompt
				'a_prompt': "best quality, extremely detailed",

				# Negative Prompt
				'n_prompt': "photograph, naked, nude, longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality",

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

			return dream
		negative = "NSFW, profile, cropped, animal, cartoon, landscape, food, text, logo, side view,"
		try:
			stable_diffusion(prompt = (promptString), image=filename, scale=9, n_prompt=negative)
		except replicate.exceptions.ModelError as e:
			print(e)
			print("Model error")
		VideoHandler(args.video_path, args.src_img, args.prompt, args).start()

if __name__ == "__main__":
	TakeSnapshotAndSave()
	selfPortrait()
	
	# prediction metrics
	# Load the image