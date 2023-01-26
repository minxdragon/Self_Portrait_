import cv2
import Syphon
import glfw
import os
import cv2
import logging
import argparse
from quickvideo import VideoHandler
from face_detection import select_face
from face_swap import face_swap
import threading
import queue

def main():
    # argument parser
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

    dir_path = os.path.dirname(args.save_path)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    
    # window details
    size = (640, 400)

    # window setup
    #server1 = Syphon.Server("Server RGB", size, show=False) # Syphon.Server("window and syphon server name", frame size, show)
    server2 = Syphon.Server("python", size, show=True)


    cap = cv2.VideoCapture(0)
    if cap.isOpened() is False:
        raise("IO Error")
        
    # create a queue to hold the frames
    frames_queue = queue.Queue()

    # pass the queue to the VideoHandler
    VideoHandler(args.video_path, args.src_img, args, frames_queue).start()

    # loop
    while not server2.should_close():
        try:
            # try to get a frame from the queue
            frame = frames_queue.get(timeout=1)
            server2.draw_and_send(frame)
        except queue.Empty:
            # if the queue is empty, do nothing
            pass
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    glfw.terminate()
    cv2.destroyAllWindows()
    exit()


if __name__ == "__main__":
    main()