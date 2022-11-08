import os
import cv2
import logging
import argparse
import replicate
import urllib
import numpy as np
import base64
import json

from urllib.request import urlopen, Request
from face_detection import select_face
from face_swap import face_swap

# face swap video from webcam class
class VideoHandler(object):
    def __init__(self, video_path=0, img_path=None, prompt=None, args=None):
        self.src_points, self.src_shape, self.src_face = select_face(cv2.imread(img_path))
        self.args = args
        self.video = cv2.VideoCapture(video_path)
        self.writer = cv2.VideoWriter(args.save_path, cv2.VideoWriter_fourcc(*'MJPG'), self.video.get(cv2.CAP_PROP_FPS),
                                      (int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    def start(self):
        while self.video.isOpened():
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            _, dst_img = self.video.read()
            dst_points, dst_shape, dst_face = select_face(dst_img, choose=False)
            if dst_points is not None:
                dst_img = face_swap(self.src_face, dst_face, self.src_points, dst_points, dst_shape, dst_img, self.args, 68)
            self.writer.write(dst_img)
            if self.args.show:
                cv2.imshow("Video", dst_img)

        self.video.release()
        self.writer.release()
        cv2.destroyAllWindows()

#load the initial image. currently static, will make dynamic later
filename = 'https://res.cloudinary.com/dj1ptpbol/image/upload/v1667791534/opencv0_o7mtqy.jpg' #Init image URL currently fixed, will make dynamic later

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s:%(lineno)d:%(message)s")

# argument parser for terminal input
    parser = argparse.ArgumentParser(description='FaceSwap Video')
    parser.add_argument('--src_img', required=False, default='dream.jpg', help='Path for source image')
    parser.add_argument('--video_path', default=0,help='Path for video')
    parser.add_argument('--warp_2d', default=False, action='store_true', help='2d or 3d warp')
    parser.add_argument('--correct_color', default=False, action='store_true', help='Correct color')
    parser.add_argument('--show', default=False, action='store_true', help='Show')
    parser.add_argument('--save_path', required=True, help='Path for storing output video')
    parser.add_argument('--prompt', type=str, required=True, help='Prompt for generation')
    parser.add_argument('--strength', type=str, required=False, help='Prompt for generation')
    parser.add_argument('--init', type=str, default=filename, required=False, help='Prompt for generation')
    args = parser.parse_args()

    dir_path = os.path.dirname(args.save_path)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    #StableDiffusion code for replicate. requires a replicate account and a export code
    def stable_diffusion(prompt, init_image, src_img, prompt_strength):
        prompt = args.prompt
        model = replicate.models.get("stability-ai/stable-diffusion")
        init_image = args.init
        prompt_strength = args.strength
        output_url = model.predict(prompt=(args.prompt), init_image=filename)[0]
        print(output_url)
        # download the image, convert it to a NumPy array, and then read
        # it into OpenCV format
        request_site = Request(output_url, headers={"User-Agent": "Mozilla/5.0"})
        req = urlopen(request_site)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1) # 'Load it as it is'
        img = np.array(img)
        dream = cv2.imwrite('dream.jpg', img)
        return dream
    
    stable_diffusion(prompt = args.prompt, init_image=filename, src_img='dream.jpg', prompt_strength=0.3)

    VideoHandler(args.video_path, args.src_img, args.prompt, args).start()