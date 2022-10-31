from turtle import shape
import gradio as gr
import numpy as np

def flip(im):
    return np.flipud(im)

demo = gr.Interface(
    flip, 
    gr.Image(source="webcam", streaming=True, shape=[768,1024]), 
    "image",
    live=True
)
demo.launch()