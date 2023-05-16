import cv2
import csv
import time
import h5py
import pickle

from .file_play import FilePlay
from src.parallel import thread_method

class MultipleData(FilePlay):
    def __init__(self, file_path):
        super().__init__(file_path)

        self.result = {"imu": None,
                       "rgb": None,
                       "depth": None}

    @thread_method
    def run(self):
        self.update1()
        self.update2()

    @thread_method
    def update1(self):
        video = cv2.VideoCapture(self.file[0])
        frame_duration = 1 / video.get(cv2.CAP_PROP_FPS)

        hdf5 = h5py.File(self.file[1], 'r')
        index = 0

        self.curr_time = time.perf_counter()

        while True:
            elapsed_time = self.curr_time - self.prev_time
            if elapsed_time > frame_duration:
                ret, frame0 = video.read()
                frame1 = hdf5[str(index)][:]

                if not ret:
                    break

                self.result["rgb"] = frame0
                self.result["depth"] = frame1
                self.prev_time = time.perf_counter()
                index += 1
            else:
                self.curr_time = time.perf_counter()

            if video.get(cv2.CAP_PROP_POS_FRAMES) == video.get(cv2.CAP_PROP_FRAME_COUNT):
                video.open(self.file[0])

                hdf5 = h5py.File(self.file[1], 'r')
                index = 0

        video.release()
        cv2.destroyAllWindows()

    @thread_method
    def update2(self):
        imu = csv.reader(open(self.file[2], "r"))

        while True:
            for row in imu:
                acc_xyz = eval(row[0])
                gyro_xyz = eval(row[1])
                self.result["imu"] = pickle.dumps([acc_xyz, gyro_xyz])

            imu = csv.reader(open(self.file[2], "r"))