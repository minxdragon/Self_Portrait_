#! /usr/bin/env python
import os
import cv2
import numpy
import argparse
import streamlit as st
import replicate
import numpy as np
from  PIL import Image, ImageEnhance
import requests
from io import BytesIO

from urllib.request import urlopen, Request
from face_detection import select_face, select_all_faces
from face_swap import face_swap

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FaceSwapApp')
    parser.add_argument('--correct_color', default=True, action='store_true', help='Correct color')
    parser.add_argument('--warp_2d', default=False, action='store_true', help='2d or 3d warp')
    #parser.add_argument('--prompt', default=False, action='store_true', help='prompt')
    args = parser.parse_args()
    
    uploaded_target_file = st.camera_input("Take a picture")
    genderoptions = st.multiselect(
    'a portrait of a', ['person', 'man', 'woman']) 
    meduimoptions = st.multiselect('in', ['oils', 'watercolor', 'acrylic', 'pastel', 'charcoal', 'pencil', 'ink', 'marker', 'digital', 'mixed media'])
    styleoptions = st.multiselect('in the style of', ['realism', 'impressionism', 'abstract', 'expressionism', 'pop art', 'surrealism',])

    prompt = print('a portrait of a', genderoptions, 'in', meduimoptions, 'in the style of', styleoptions)
    st.write('a portrait of a', genderoptions, 'in', meduimoptions, 'in the style of', styleoptions)
    

    # stable diffusion script
    model = replicate.models.get("stability-ai/stable-diffusion")
    init_image = uploaded_target_file
    print (init_image)
    output_url = model.predict(prompt=(prompt), init_image=(init_image))[0]
    print(output_url)
    # download the image, convert it to a NumPy array, and then read
    response = requests.get(output_url)
    img = Image.open(BytesIO(response.content))
    st.image(img, caption='Stable Diffusion Image')

    target_image = Image.open(uploaded_target_file)
    source_image = Image.open(img)
    
    #uploaded_source_file = st.file_uploader("Upload a source image", type=["png", "jpg", "jpeg"])

    if uploaded_target_file is not None and img is not None and prompt is not None:
    
       # Convert images from PIL to CV2
        src_img = cv2.cvtColor(numpy.array(source_image), cv2.IMREAD_COLOR)
        dst_img = cv2.cvtColor(numpy.array(target_image), cv2.IMREAD_COLOR)
    

       # Select src face
        src_points, src_shape, src_face = select_face(src_img)
       # Select dst face
        dst_faceBoxes = select_all_faces(dst_img)

        if dst_faceBoxes is None:
          print('Detect 0 Face !!!')
          exit(-1)

        output = dst_img
        for k, dst_face in dst_faceBoxes.items():
           output = face_swap(src_face, dst_face["face"], src_points,
                           dst_face["points"], dst_face["shape"],
                           output, args)

           st.markdown('<p style="text-align: left;">Result</p>',unsafe_allow_html=True)
           st.image(output,width=500)       