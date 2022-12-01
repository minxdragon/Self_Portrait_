import keras
import os
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import to_categorical
from keras.preprocessing import image

#os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

import numpy as np
import pandas as pd
import matplotlib  
#matplotlib.use('Qt5Agg')    
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from tqdm import tqdm
#imports
import sys
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QApplication, QTableWidget,
                               QTableWidgetItem)
# %matplotlib inline

#reading labels and dataset
train = pd.read_csv('SP_Dataset/train.csv')    # reading the csv file - Change for my new CSV
print (train.head)      # printing first five rows of the file
print (train.columns) # display the data array

#loading images and preprocessing into an array
train_image = []
for i in tqdm(range(train.shape[0])):
    img = keras.preprocessing.image_dataset.image_dataset_from_directory('SP_Dataset/Images/'+train['Id'][i]+'.jpg',target_size=(400,400,3)) #change this for my dataset
    img = tf.keras.utils.img_to_array(img)
    img = img/255
    train_image.append(img)
X = np.array(train_image)

print (X.shape) #Showing the array

#plt.imshow(X[2]) #pull an example image
#plt.show() #use this to show any matplotlib

#print(train['Pronouns'][2]) #show the genre of that image

# make an array just with Genre and image ID. this step may not be necessary for my work depending on how my file looks.
y = np.array(train.drop(['Id', 'Labels'],axis=1))

print(y.shape)

# create validation set
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.1)

# architecture - this can be modified by changing the number of hidden layers, activation functions and other hyperparameters
model = Sequential()
model.add(Conv2D(filters=16, kernel_size=(5, 5), activation="relu", input_shape=(400,400,3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(filters=32, kernel_size=(5, 5), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(filters=64, kernel_size=(5, 5), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(filters=64, kernel_size=(5, 5), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(52, activation='sigmoid')) #change for the amount of labels

model.summary()

# compile with ADAM
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

#training
model.fit(X_train, y_train, epochs=20, validation_data=(X_test, y_test), batch_size=64) #change the epochs here, no need to update the architecture.

from sklearn.metrics import confusion_matrix
cm=confusion_matrix(y_test,X_test)
print(cm)

#save the model
model.save('SPDataset')