import keras
import os
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import to_categorical
from keras.preprocessing import image

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from tqdm import tqdm
#imports
from keras.models import Sequential
from sklearn.model_selection import KFold
from keras import regularizers
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, BatchNormalization, Activation
from keras.utils import to_categorical
from keras.preprocessing import image
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt
                               

#reading labels and dataset
train = pd.read_csv('facedataset/train.csv')    # reading the csv file - Change for my new CSV
print (train.head)      # printing first five rows of the file
print (train.columns) # display the data array

#loading images and preprocessing into an array
train_image = []
for i in tqdm(range(train.shape[0])):
    img = image.load_img('facedataset/images/'+train['Id'][i]+'.jpg',target_size=(400,400,3)) #change this for my dataset
    img = image.img_to_array(img)
    img = img/255
    train_image.append(img)
X = np.array(train_image)

print (X.shape) #Showing the array

#plt.imshow(X[2]) #pull an example image
#plt.show() #use this to show any matplotlib

print(train['Labels'][2]) #show the genre of that image

# make an array just with Genre and image ID. this step may not be necessary for my work depending on how my file looks.
y = np.array(train.drop(['Id', 'Labels'],axis=1))

print(y.shape)

#define the number of folds (k)
k = 5

#Create a kfold object
kf = KFold(n_splits=k, random_state=None)

#loop through the folds
for train_index, test_index in kf.split(X):
    #print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_val = X[train_index], X[test_index]
    y_train, y_val = y[train_index], y[test_index]

# create validation set
#X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.1)

# architecture - this can be modified by changing the number of hidden layers, activation functions and other hyperparameters
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
model.add(Conv2D(filters=128, kernel_size=(5, 5), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(75, activation='sigmoid')) #change for the amount of labels


# First, we'll need to compile the model with the `AUC` metric
ACUmetric = keras.metrics.AUC()
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=[ACUmetric])

# Next, we'll need to train the model and save the training history
history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=2, batch_size=64)

# After training, we can use the `predict` method to generate
# predictions for the validation data
predictions = model.predict(X_val)

# We can then use the `roc_auc_score` function to compute the AUC
# for each class in the predictions
auc = roc_auc_score(y_val, predictions, average='macro')

# To plot the ROC curve, we can use the `roc_curve` function to
# compute the false positive rate and true positive rate for
# different threshold values
# fpr, tpr, thresholds = roc_curve(y_val, predictions)

# # Finally, we can plot the ROC curve using matplotlib
# plt.plot(fpr, tpr)
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.title('ROC Curve (AUC = %0.3f)' % auc)

#confusion matrix
from sklearn.metrics import confusion_matrix
cm=confusion_matrix(y_val,X_val)
print(cm)

#save the model
model.save('facedataset.h5')