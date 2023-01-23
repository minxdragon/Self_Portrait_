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
        cap.set(10,150)

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
            cv2.rectangle(img, (x, y), (x + 100 + w + 100, y + 100 + h + 100), (0, 0, 255), 2)
            faces = img[y:y + 100 + h, x:x + 100 + w]

            cv2.imshow("face",faces)
            cv2.imwrite('opencv'+str(num)+'.jpg',faces)
            
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
        promptString = "a head and shoulders portrait of a person, full face, with a neutral expression of a person who is " + analysisComplete + " painted by a portrait artist"

        print (promptString)

    ### Face swap
    #will come from imagebb
    facefile = ()

    userSelected = None #convert array to string

    promptString = "a head and shoulders portrait of a person, full face, with a neutral expression of a person who is " + analysisComplete + " painted by a portrait artist"

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
        parser.add_argument('--src_img', required=False, default='dream.jpg', help='Path for source image')
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
        def stable_diffusion(prompt, init_image, src_img, prompt_strength):
            prompt = args.prompt
            model = replicate.models.get("stability-ai/stable-diffusion")
            init_image = args.init
            prompt_strength = args.strength
            output_url = model.predict(prompt=(args.prompt), init_image=filename)[0]
            print(output_url)
            # download the image, convert it to a NumPy array, and then read
            # it into OpenCV format
            request_site = Request(output_url, headers={"User-Agent": "Mozilla/5.0"})
            req = urlopen(request_site)
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            img = cv2.imdecode(arr, -1) # 'Load it as it is'
            img = np.array(img)
            dream = cv2.imwrite('dream.jpg', img)
            return dream
        
        stable_diffusion(prompt = args.prompt, init_image=filename, src_img='dream.jpg', prompt_strength=0.3)

        VideoHandler(args.video_path, args.src_img, args.prompt, args).start()

if __name__ == "__main__":
    TakeSnapshotAndSave()
    selfPortrait()
    
    # prediction metrics
    # Load the image