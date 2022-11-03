import keras
import os
import cv2
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import to_categorical
from keras.preprocessing import image

#os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

import numpy as np
import pandas as pd

#matplotlib.use('Qt5Agg')    
from matplotlib import pyplot as plt
import matplotlib as mpl
from sklearn.model_selection import train_test_split
from tqdm import tqdm
#imports

from csv import writer
from PIL import Image
from skimage import data
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray
import uuid
                            

#import the cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def TakeSnapshotAndSave():
    # access the webcam (every webcam has a number, the default is 0)
    cap = cv2.VideoCapture(0)

    num = 0 
    while num<1:
        # Capture frame-by-frame
        ret, img = cap.read()
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

            #cv2.imshow("face",faces)
            cv2.imwrite('opencv'+str(num)+'.jpg',faces)
            
        # Display the output
        #cv2.imwrite('face.jpg', faces)
        #cv2.imshow('img', img)
        #cv2.waitKey()

        #older code after
        x = 100
        y = 100
        text_color = (0,255,0)

        cv2.imwrite('opencv'+str(num)+'.jpg',faces)
        cv2.namedWindow("output", cv2.WINDOW_AUTOSIZE)    # Create window with freedom of dimensions
        im = cv2.imread('opencv0.jpg')                    # Read image
        #imS = cv2.resize(im, (940, 540))                # Resize image
        cv2.imshow("output", im)                       # Show image
        cv2.waitKey(0)                                  # Display the image infinitely until any keypress
        num = num+1
        
    # When everything done, release the capture

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    TakeSnapshotAndSave()
    
    # prediction metrics
    # Load the image

#filelist = ['static/thumbnails/752a9c4dbc0d4e0aa30c183035da7b26.jpg']
#filelist = ['test1.jpg','test2.jpg','test3.jpg','test4.jpg','test5.jpg','test6.jpg','test7.jpg','test8.jpg','test9.jpg','test10.jpg','test11.jpg','test12.jpg',]
filelist = ['opencv0.jpg']
for imagefile in filelist:
    img = image.load_img(imagefile,target_size=(400,400,3))
    img = image.img_to_array(img)
    img = img/255
# save the image file to dataset
    img_save = image.img_to_array(img)
    unique_filename = str(uuid.uuid4())
    Saved_img = image.save_img(unique_filename + '.jpg', img_save, file_format='jpeg',)

    # get the model
    train = pd.read_csv('SP_Dataset/train.csv') # don't forget to update this to the dataset
    model = keras.models.load_model('SPDataset') # don't forget to update this to the dataset
    classes = np.array(train.columns[2:])
    proba = model.predict(img.reshape(1,400,400,3))
    top_6 = np.argsort(proba[0])[:-9:-1]

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