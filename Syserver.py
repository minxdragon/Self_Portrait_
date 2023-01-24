
import cv2
import Syphon
import glfw
import os
import argparse
from urllib.request import urlopen, Request
from face_detection import select_face
from face_swap import face_swap

src_img='interactive/data/dream.jpg'
parser = argparse.ArgumentParser(description='FaceSwap Video')
parser.add_argument('--src_img', required=False, default=src_img, help='Path for source image')
parser.add_argument('--video_path', default=0,help='Path for video')
parser.add_argument('--warp_2d', default=False, action='store_true', help='2d or 3d warp')
parser.add_argument('--correct_color', default=False, action='store_true', help='Correct color')
parser.add_argument('--show', default=False, action='store_true', help='Show')
parser.add_argument('--save_path', required=False, default= "test/test.avi", help='Path for storing output video')
args = parser.parse_args()

dir_path = os.path.dirname(args.save_path)
if not os.path.isdir(dir_path):
    os.makedirs(dir_path)

class VideoHandler(object):

    def __init__(self, video_path=0, img_path=None, prompt=None, args=None):
        self.src_points, self.src_shape, self.src_face = select_face(cv2.imread(img_path))
        self.args = args
        self.video = cv2.VideoCapture(video_path)
        #self.writer = cv2.VideoWriter(args.save_path, cv2.VideoWriter_fourcc(*'MJPG'), self.video.get(cv2.CAP_PROP_FPS),
                                    #(int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    def start(self):
        src_img='interactive/data/dream.jpg'
        # window details
        size = (640, 400)
        server2 = Syphon.Server("python", size, show=False)
        import time
        time_to_close = 5
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
            server2.draw_and_send(dst_img)

        self.video.release()
        self.writer.release()
        cv2.destroyAllWindows()

def main():

    # window details
    size = (640, 400)

    # window setup
    # server1 = Syphon.Server("Server RGB", size, show=False) # Syphon.Server("window and syphon server name", frame size, show)
    server2 = Syphon.Server("python", size, show=False)


    cap = cv2.VideoCapture(0)
    if cap.isOpened() is False:
        raise("IO Error")
        
    # loop
    # while not server1.should_close() and not server2.should_close():
    while not server2.should_close():
        ret, frame = cap.read() #read camera image
        frame = cv2.resize(frame, size)
        # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #BGR --> RGB
        # frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #BGR --> GRAY
        # frame_gray = cv2.cvtColor(frame_gray, cv2.COLOR_GRAY2RGB) # GRAY (3 channels)
        VideoHandler(video_path="test/test.avi", img_path="interactive/data/dream.jpg", args=None)
        
        #cv2.imshow("rgb", frame)
        #server1.draw_and_send(frame_rgb) # Syphon.Server.draw_and_send(frame) draw frame using opengl and send it to syphon
        
        # cv2.imshow("python", dst_img)
        # server2.draw_and_send(dst_img)
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    glfw.terminate()
    cv2.destroyAllWindows()
    exit()


if __name__ == "__main__":
    main()
