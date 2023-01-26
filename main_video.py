import os
import cv2
import logging
import argparse
import replicate
import urllib
import numpy as np
import base64
import json
import queue

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
        import time
            # create a queue to hold the frames
        frames_queue = queue.Queue()
        time_to_close = 10
        start_time = time.time()
        while self.video.isOpened():
            if cv2.waitKey(1) & 0xFF == ord('q') or time.time() - start_time > time_to_close:
                break

            _, dst_img = self.video.read()
            dst_points, dst_shape, dst_face = select_face(dst_img, choose=False)
            if dst_points is not None:
                dst_img = face_swap(self.src_face, dst_face, self.src_points, dst_points, dst_shape, dst_img, self.args, 68)
            self.writer.write(dst_img)
            #if self.args.show:
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
    parser.add_argument('--negative_prompt', type=str, required=False, default='nsfw, profile, cropped, partial, incomplete, abstract',help='Prompt for generation')
    args = parser.parse_args()

    dir_path = os.path.dirname(args.save_path)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    #StableDiffusion code for replicate. requires a replicate account and a export code
    def stable_diffusion(prompt, init_image, src_img, prompt_strength):
        model = replicate.models.get("stability-ai/stable-diffusion")
        version = model.versions.get("27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478")

        # https://replicate.com/stability-ai/stable-diffusion/versions/27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478#input
        inputs = {
            # Input prompt
            'prompt': "a full head and shoulders portrait of a person",

            # The prompt NOT to guide the image generation. Ignored when not using
            # guidance
            'negative_prompt': "not profile, cropped, partial, profile, NSFW"

            # # Width of output image. Maximum size is 1024x768 or 768x1024 because
            # # of memory limits
            # 'width': 512,

            # # Height of output image. Maximum size is 1024x768 or 768x1024 because
            # # of memory limits
            # 'height': 512,

            # Inital image to generate variations of. Will be resized to the
            # specified width and height
            # 'init_image': open("path/to/file", "rb"),

            # Black and white image to use as mask for inpainting over init_image.
            # Black pixels are inpainted and white pixels are preserved. Tends to
            # work better with prompt strength of 0.5-0.7. Consider using
            # https://replicate.com/andreasjansson/stable-diffusion-inpainting
            # instead.
            # 'mask': open("path/to/file", "rb"),

            # Prompt strength when using init image. 1.0 corresponds to full
            # destruction of information in init image
            #'prompt_strength': 0.3,

            # Number of images to output. If the NSFW filter is triggered, you may
            # get fewer outputs than this.
            # Range: 1 to 10
            # 'num_outputs': 1,

            # # Number of denoising steps
            # # Range: 1 to 500
            # 'num_inference_steps': 50,

            # # Scale for classifier-free guidance
            # # Range: 1 to 20
            # 'guidance_scale': 7.5,

            # # Choose a scheduler. If you use an init image, PNDM will be used
            # 'scheduler': "K-LMS",

            # Random seed. Leave blank to randomize the seed
            # 'seed': ...,
            }
        output = version.predict(**inputs)
        print(output)
        #remove square brackets from output
        output = str(output)
        output = output.replace('[', '')
        output = output.replace(']', '')
        #convert %s' to :
        output = output.replace('%s', ':')
        print(output)
        # download the image, convert it to a NumPy array, and then read
        # it into OpenCV format
        request_site = Request(output, headers={"User-Agent": "Mozilla/5.0"})
        req = urlopen(request_site)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1) # 'Load it as it is'
        img = np.array(img)
        dream = cv2.imwrite('dream.jpg', img)
        return dream
    
    stable_diffusion(prompt=args.prompt, init_image=filename, src_img='dream.jpg', prompt_strength=0.3)

    VideoHandler(args.video_path, args.src_img, args.prompt, args).start()