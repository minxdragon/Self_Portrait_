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
                            

# #import the cascade for face detection
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# def TakeSnapshotAndSave():
#     # access the webcam (every webcam has a number, the default is 0)
#     cap = cv2.VideoCapture(0)

#     num = 0 
#     while num<1:
#         # Capture frame-by-frame
#         ret, frame = cap.read()
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#         # to detect faces in video
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#         for (x,y,w,h) in faces:
#             cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
#             roi_gray = gray[y:y+h, x:x+w]
#             roi_color = frame[y:y+h, x:x+w]

#         x = 0
#         y = 20
#         text_color = (0,255,0)

#         cv2.imwrite('opencv'+str(num)+'.jpg',frame)
#         num = num+1
        
#     # When everything done, release the capture

#     cap.release()
#     cv2.destroyAllWindows()


# if __name__ == "__main__":
#     TakeSnapshotAndSave()
    
# prediction metrics
# Load the image

# Load the image
#filelist = ['static/thumbnails/752a9c4dbc0d4e0aa30c183035da7b26.jpg']
filelist = ['test1.jpg','test2.jpg','test3.jpg','test4.jpg','test5.jpg','test6.jpg','test7.jpg','test8.jpg','test9.jpg','test10.jpg','test11.jpg','test12.jpg',]
for imagefile in filelist:
    img = image.load_img(imagefile,target_size=(400,400,3))
    img = image.img_to_array(img)
    img = img/255
# save the image file to dataset
    img_save = image.img_to_array(img)
    unique_filename = str(uuid.uuid4())
    #Saved_img = image.save_img('/Users/j.rosenbaum/Development/DCGAN-tensorflow/data/gender-tapestry/' + unique_filename + '.jpg', img_save, file_format='jpeg', target_size=(400,400,3))

    # get the model
    train = pd.read_csv('Top6_Dataset/train.csv') # don't forget to update this to the dataset
    model = keras.models.load_model('Top6Dataset20') # don't forget to update this to the dataset
    classes = np.array(train.columns[2:])
    proba = model.predict(img.reshape(1,400,400,3))
    top_6 = np.argsort(proba[0])[:-9:-1]

    print (proba)
    print (top_6)
    print ('classes ' + classes)

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

    #separate Hex values and strip .
    hexCode1 = prediction_0[:prediction_0.find('.')]
    hexCode2 = prediction_1[:prediction_1.find('.')]
    hexCode3 = prediction_2[:prediction_2.find('.')]
    hexCode4 = prediction_3[:prediction_3.find('.')]
    hexCode5 = prediction_4[:prediction_4.find('.')]
    hexCode6 = prediction_5[:prediction_5.find('.')]
    #format variables for CSV
    print(hexCode1 + hexCode2 + hexCode3 + hexCode4 + hexCode5 + hexCode6)
    #print (hexCode1 + ", " + hexCode2 + ", " + hexCode3)
  

    hexCSV = {'#'+hexCode1+hexCode2+hexCode3+hexCode4 + hexCode5 + hexCode6}
    hexCode = (hexCode1 + hexCode2 + hexCode3 + hexCode4 + hexCode5 + hexCode6)

 #format the hexcode
 #      #shorten each to its first number
    hc1 = hexCode1[:1]
    hc2 = hexCode2[:1]
    hc3 = hexCode3[:1]
    hc4 = hexCode4[:1]
    hc5 = hexCode5[:1]
    hc6 = hexCode6[:1]

    hexCode = (hc1 + hc2 + hc3 + hc4 + hc5 + hc6)

    print ('hexcode = ' + hexCode)

#formatting the RGB code
    #Shorten each number to the first two for the three primary results and one digit for the three secondary results
    rg1 = hexCode1[:2]
    rg2 = hexCode2[:2]
    rg3 = hexCode3[:2]
    rg4 = hexCode4[:1]
    rg5 = hexCode5[:1]
    rg6 = hexCode6[:1]

    #add the first and fourth results together and divide the remainders by 255 to ensure the results are RGB compatible
    RGBc1 = int(rg1+rg4) % 255
    RGBc2 = int(rg2+rg5) % 255
    RGBc3 = int(rg3+rg6) % 255

    #print the formatted string for testing
    print ('RGB = '+ str(RGBc1)+','+str(RGBc2)+','+str(RGBc3))

# #Hex Code image generation
#     # make sure all hex numbers are 6 long
#     global h_pad
#     global h_number
#     h_pad = hexCode.ljust(6, '0')  
#     print('h_pad = ' + h_pad)

#     # remove the +
#     global h_clean
#     if '+' in h_pad:
#         h_clean = h_pad.replace('+', '5')
#         print('h_clean = '+ h_clean)
    
#     if 'e' in h_pad:
#         h_number= h_clean.replace('e', '3')
#         print('h_number = '+ h_number)

#     else:
#         h_number = h_pad

#     Hex_result = int(h_number)
#     hexCSV = {'#'+ h_number}

#     print ("cleaned hex is ", Hex_result)

#     #add HexColors to CSV
#     def append_list_as_row(file_name, listElem):
#         # Open file in append mode
#         file_name = ("Predictions.csv") 
#         with open(file_name, 'a+', newline='') as write_obj:
#             # Create a writer object from csv module
#             csv_writer = writer(write_obj)
#             # Add contents of list as last row in the csv file
#             csv_writer.writerow(listElem)

#     append_list_as_row("Predictions.csv", hexCSV)

#     hex_colors.append(hexCSV)

#     #generate the Hexcolor tile
#     webhexcolor = Hex_result
#     im = Image.new(mode="RGB", size=(100,100), color='#'+h_number)
#     #save the color as an image
#     unique_filename = str(uuid.uuid4())
#     im.save("colors/" + unique_filename + ".png")

#create a two color image from the photo and the color
    RGBimage = img_save

    #convert image to grayscale
    grayscale = rgb2gray(RGBimage)

    # Threshold image to binary
    thresh = threshold_otsu(grayscale)
    binary = grayscale > thresh

    # Make 3 channel RGB image same dimensions
    RGB = np.zeros((binary.shape[0],binary.shape[1],3), dtype=np.uint8)

#light Binary image
    # Make True pixels white
    RGB[binary]  = [255,255,255]
    # Make False pixels generated color
    RGB[~binary] = [RGBc1, RGBc2, RGBc3]

    # Display result
    imB = Image.fromarray(RGB)
    unique_filename = str(uuid.uuid4())
    imB.save("binary/" + unique_filename + ".png")

# dark binary image
    # Make 3 channel RGB image same dimensions
    RGB = np.zeros((binary.shape[0],binary.shape[1],3), dtype=np.uint8)

    # Make True pixels new color
    RGB[binary]  = [RGBc1, RGBc2, RGBc3]
    # Make False pixels blue
    RGB[~binary] = [0,0,0]

    # Display result
    imB = Image.fromarray(RGB)
    unique_filename = str(uuid.uuid4())
    imB.save("binary/" + unique_filename + ".png")