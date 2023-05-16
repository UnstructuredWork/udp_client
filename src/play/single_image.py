import cv2
import time

from .file_play import FilePlay

class SingleImage(FilePlay):
    def __init__(self, file_path):
        super().__init__(file_path)

    def update(self):
        video = cv2.VideoCapture(self.file)
        frame_duration = 1 / video.get(cv2.CAP_PROP_FPS)

        self.curr_time = time.perf_counter()

        while video.isOpened():
            elapsed_time = self.curr_time - self.prev_time
            if elapsed_time > frame_duration:
                ret, frame = video.read()

                if ret:
                    self.result = frame

                self.prev_time = time.perf_counter()
            else:
                self.curr_time = time.perf_counter()

            if video.get(cv2.CAP_PROP_POS_FRAMES) == video.get(cv2.CAP_PROP_FRAME_COUNT):
                video.open(self.file)

        video.release()
        cv2.destroyAllWindows()