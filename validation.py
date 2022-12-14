import pandas as pd

#load dataset into a dataframe
df = pd.read_csv('facedataset/train.csv')

#display all of the labels
labels = (df['Labels'].unique())

#use the value counts to get the number of examples for every single label in your dataset
label_counts = str(df['Labels'].value_counts())

#display the label counts for every label
#print(labels + label_counts)

#visualize the label counts for every label in a bar chart
df['Labels'].value_counts().plot(kind='bar')

#define plt
import matplotlib.pyplot as plt

#view the bar chart
plt.show()