import os
import cv2
import logging
import argparse

from face_detection import select_face
from face_swap import face_swap
import threading
import queue

class VideoHandler(object):
    def __init__(self, frames_queue, video_path=0, img_path=None, args=None):
        self.frames_queue = frames_queue
        self.video_path = video_path
        self.img_path = img_path
        self.args = args
        try:
            self.src_points, self.src_shape, self.src_face = select_face(cv2.imread(img_path))
            if self.src_points is None:
                raise Exception('No face detected in the source image')
        except Exception as e:
            print(e)
            img_path = 'interactive/data/dream2.jpg'
            print('Using default image')
            self.src_points, self.src_shape, self.src_face = select_face(cv2.imread(img_path))
                
            self.args = args
            self.video = cv2.VideoCapture(video_path)
            self.stopped = False
            self.dst_queue = queue.Queue()
                # create a queue to hold the frames

    def start(self):
        t = threading.Thread(target=self.process_video)
        t.daemon = True
        t.start()
        print("starting VideoHandler.start")
        while not self.stopped:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stopped = True
                break
            if self.video.isOpened():
                dst_img = self.dst_queue.get()
                resized = cv2.resize(dst_img, (640, 400))
                cv2.imshow("python", resized,)


    def process_video(self):
        print("starting VideoHandler.process_video")
        while not self.stopped:
            _, dst_img = self.video.read()
            dst_points, dst_shape, dst_face = select_face(dst_img, choose=False)
            if dst_points is not None:
                self.dst_img = face_swap(self.src_face, dst_face, self.src_points, dst_points, dst_shape, dst_img, self.args, 68)
                self.dst_queue.put(self.dst_img)
            else:
                self.dst_img = dst_img
                self.dst_queue.put(self.dst_img)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s:%(lineno)d:%(message)s")

    parser = argparse.ArgumentParser(description='FaceSwap Video')
    parser.add_argument('--src_img', required=False, default='interactive/data/dream.jpg',
                        help='Path for source image')
    parser.add_argument('--video_path', default=0,
                        help='Path for video')
    parser.add_argument('--warp_2d', default=False, action='store_true', help='2d or 3d warp')
    parser.add_argument('--correct_color', default=False, action='store_true', help='Correct color')
    parser.add_argument('--show', default=False, action='store_true', help='Show')
    parser.add_argument('--save_path', required=False, default="test/test.avi", help='Path for storing output video')
    args = parser.parse_args()
        # create a queue to hold the frames
    frames_queue = queue.Queue()

    dir_path = os.path.dirname(args.save_path)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    VideoHandler(frames_queue, video_path=0, img_path='interactive/data/dream.jpg', args=args.parse_args()).start()