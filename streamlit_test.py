
#! /usr/bin/env python
import os
import cv2
import numpy as np
import argparse
import streamlit as st
import replicate
from  PIL import Image, ImageEnhance

from urllib.request import urlopen, Request
from face_detection import select_face
from face_swap import face_swap

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FaceSwapApp')
    parser.add_argument('--correct_color', default=True, action='store_true', help='Correct color')
    parser.add_argument('--warp_2d', default=False, action='store_true', help='2d or 3d warp')
    parser.add_argument('--prompt', default=True, action='store_true', help='prompt for generation')
    args = parser.parse_args()
    
    uploaded_source_file = st.file_uploader("Source File", type=['jpg','png','jpeg'])
    # uploaded_target_file = st.file_uploader("Target File", type=['jpg','png','jpeg'])

    entered_prompt = st.text_input("Your name", key="name")
    
    if entered_prompt is not None:
        source_image = Image.open(uploaded_source_file)
       # target_image = Image.open(uploaded_target_file)
        model = replicate.models.get("stability-ai/stable-diffusion")
        init_image = ("dream.jpg")
        output_url = model.predict(prompt=(args.prompt))[0]
        print(output_url)

            # download the image, convert it to a NumPy array, and then read
            # it into OpenCV format
        request_site = Request(output_url, headers={"User-Agent": "Mozilla/5.0"})
        req = urlopen(request_site)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1) # 'Load it as it is'
        img = np.array(img)
        dream = cv2.imwrite('dream.jpg', img)
    
       # Convert images from PIL to CV2
        src_img = cv2.cvtColor(np.array(source_image), cv2.IMREAD_COLOR)
        dst_img = cv2.cvtColor(np.array(dream), cv2.IMREAD_COLOR)

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