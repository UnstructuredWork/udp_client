import cv2
import time
import pyk4a
import pickle

from nvjpeg import NvJpeg
from threading import Thread
from datetime import datetime
from pyk4a import Config, PyK4A
from turbojpeg import TurboJPEG
from src.load_cfg import LoadConfig

class Kinect:
    def __init__(self, config_path):
        self.k4a = PyK4A(
            Config(
                color_resolution=pyk4a.ColorResolution.RES_720P,
                depth_mode=pyk4a.DepthMode.WFOV_2X2BINNED,
                camera_fps=pyk4a.FPS.FPS_30
            )
        )

        self.openCL = False

        if cv2.ocl.haveOpenCL():
            cv2.ocl.setUseOpenCL(True)
            self.openCL = True

        self.imu   = None
        self.rgb   = None
        self.depth = None
        self.frame = None

        self.frame_time = None

        self.current_time = time.time()
        self.preview_time = time.time()

        self.sec = 0

        self.set()

        self.imu_thread   = None
        self.frame_thread = None

        self.config = LoadConfig(config_path).info

        if self.config["gpu_compression"]:
            self.comp = NvJpeg()
        else:
            self.comp = TurboJPEG()

        self.started  = False

    def set(self):
        self.k4a.start()
        self.k4a.whitebalance = 4500
        assert self.k4a.whitebalance == 4500
        self.k4a.whitebalance = 4510
        assert self.k4a.whitebalance == 4510

    def run(self):
        self.imu_thread = Thread(target=self.imu_update, args=())
        self.imu_thread.start()

        self.frame_thread = Thread(target=self.frame_update, args=())
        self.frame_thread.start()

        self.started = True

    def stop(self):
        self.started = False

        self.k4a._stop_imu()
        self.k4a.stop()

    def imu_update(self):
        while True:
            if self.started:
                acc_xyz = self.k4a.get_imu_sample().pop("acc_sample")
                gyro_xyz = self.k4a.get_imu_sample().pop("gyro_sample")
                self.imu = pickle.dumps([acc_xyz, gyro_xyz])

    def frame_update(self):
        while True:
            if self.started:
                self.rgb = self.k4a.get_capture().color[:, :, :3]
                self.depth = self.k4a.get_capture().transformed_depth
                self.frame_time = datetime.now().time().isoformat().encode('utf-8')

                self.frame = self.comp.encode(self.rgb, 40) + b'frame' + \
                             cv2.imencode('.png', self.depth, [cv2.IMWRITE_PNG_COMPRESSION, 4])[1].tobytes()

    def fps(self):
        self.current_time = time.time()
        self.sec = self.current_time - self.preview_time
        self.preview_time = self.current_time
        if self.sec > 0:
            fps = round((1/self.sec), 1)
        else:
            fps = 1

        return fps