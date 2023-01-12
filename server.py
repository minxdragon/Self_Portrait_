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

from urllib.request import urlopen, Request
from face_detection import select_face
from face_swap import face_swap

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
                    face = client.upload(file='/Users/j.rosenbaum/Documents/GitHub/FaceSwap/opencv0.jpg', expiration=600)
                print(face.url)
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
                    # create a variable with terms
                    terms = str(classes[top_6[0]]) + " " + str(classes[top_6[1]]) + " " + str(classes[top_6[2]]) + " " + str(classes[top_6[3]]) + " " + str(classes[top_6[4]]) + " " + str(classes[top_6[5]])
                    
                    #create a variable with terms separated into bytes
                    analysis = (classes[top_6[0]]).encode() + b"&" + (classes[top_6[1]]).encode() + b"&" + (classes[top_6[2]]).encode() + b"&" + (classes[top_6[3]]).encode() + b"&" + (classes[top_6[4]]).encode() + b"&" + (classes[top_6[5]]).encode()
                    response = b"analysisComplete,"

                    analysisComplete = response + analysis

                    #generate a string for the prompt using the prediction results
                    promptString = "a head and shoulders portrait of a person, full face, with a neutral expression of a person who is " + terms + " painted by a portrait artist"

                    print (promptString)

                    #print ("analysis complete," + analysisComplete) #send as server command

                    conn.sendall(analysisComplete)
                #conn.sendall(b"analysisComplete,musical&level-headed&visionary&risk-taker&creative")
                print(f'Analysis complete. Mask and Keywords sent.')
            elif splitMessage[0] == 'userSelected':
                print(f'Fetching mask...')  
                time.sleep(4)
                print(f'Sending...')                
                conn.sendall(b"cameraMaskReady,window frame name")
                print(f'Analysis complete. Mask and Keywords sent.')
            else:
                print(f'Message type not identified')

