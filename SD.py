import time
import keras_cv
from tensorflow import keras
import matplotlib.pyplot as plt
import argparse
import cv2
import numpy as np

parser = argparse.ArgumentParser(description='Creates a photomosaic from input images')
parser.add_argument('--prompt', required=True, default="create an image", help="create an image with a prompt")
#parser.add_argument('--strength', required=False, default=0.5, help="prompt strength")
#parser.add_argument('--init', required=False, default="dream.jpg", help="initial image")
parser.add_argument('--size', required=False, type=int, default=126, help="image size")
#parser.add_argument('--steps', required=False, default=100, help="number of steps")
parser.add_argument('--batch', type=int, default=3, help='Batch size')

args = parser.parse_args()

model = keras_cv.models.StableDiffusion(img_width=args.size, img_height=args.size)

images = model.text_to_image(args.prompt, batch_size=args.batch)

def plot_images(images):
    plt.figure(figsize=(20, 20))
    for i in range(len(images)):
        ax = plt.subplot(1, len(images), i + 1)
        plt.imshow(images[i])
        plt.axis("off")
        plt.savefig('foo.png', bbox_inches='tight') #saves all images in batch as one, need to change the path too

plot_images(images)

plt.show()
