import cv2
import csv
import pickle

from src.parallel import thread_method

class FilePlay:
    def __init__(self, side, file_path):
        self.img = None
        self.side = side
        self.file = file_path
        self.result = {"imu": None,
                       "rgb": None,
                       "depth": None}

    @thread_method
    def run(self):
        if self.side == 'STEREO_L' or self.side == 'STEREO_R':
            self.rgb_update()
        elif self.side == 'RGBD':
            self.rgbd_update()
            self.imu_update()

    @thread_method
    def rgb_update(self):
        video = cv2.VideoCapture(self.file)

        while video.isOpened():
            ret, frame = video.read()

            if ret:
                self.img = frame

    @thread_method
    def rgbd_update(self):
        video0 = cv2.VideoCapture(self.file[0])
        video1 = cv2.VideoCapture(self.file[1])

        while True:
            ret0, frame0 = video0.read()
            ret1, frame1 = video1.read()

            if not ret0 or not ret1:
                break

            self.result["rgb"] = frame0
            self.result["depth"] = frame1[:, :, 0]

    @thread_method
    def imu_update(self):
        imu = csv.reader(open(self.file[2], "r"))

        while True:
            for row in imu:
                acc_xyz = eval(row[0])
                gyro_xyz = eval(row[1])
                self.result["imu"] = pickle.dumps([acc_xyz, gyro_xyz])

