import time
import keras_cv
from tensorflow import keras
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Creates a photomosaic from input images')
parser.add_argument('--prompt', required=True, default="create an image", help="create an image with a prompt")
parser.add_argument('--strength', required=False, default=0.5, help="prompt strength")
parser.add_argument('--init', required=False, default="dream.jpg", help="initial image")
parser.add_argument('--size', required=False, default=512, help="image size")

args = parser.parse_args()

model = keras_cv.models.StableDiffusion(img_width=args.size, img_height=args.size)

images = model.text_to_image(args.prompt, batch_size=3)

def plot_images(images):
    plt.figure(figsize=(20, 20))
    for i in range(len(images)):
        ax = plt.subplot(1, len(images), i + 1)
        plt.imshow(images[i])
        plt.axis("off")

plot_images(images)
