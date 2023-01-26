
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
        
    # loop
    # while not server1.should_close() and not server2.should_close():
    while not server2.should_close():
        ret, frame = cap.read() #read camera image
        frame = cv2.resize(frame, size)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #BGR --> RGB
        #frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #BGR --> GRAY
        #frame_gray = cv2.cvtColor(frame_gray, cv2.COLOR_GRAY2RGB) # GRAY (3 channels)
        #VideoHandler(args.video_path, args.src_img, args).start()
        
        #cv2.imshow("rgb", frame)
        #server1.draw_and_send(frame_rgb) # Syphon.Server.draw_and_send(frame) draw frame using opengl and send it to syphon
        #cv2.imshow("python", frame_gray)
        #server2.draw_and_send(frame_gray)
        #cv2.imshow("python", resized)
        server2.draw_and_send(VideoHandler(args.video_path, args.src_img, args).start())
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    glfw.terminate()
    cv2.destroyAllWindows()
    exit()


if __name__ == "__main__":
    main()