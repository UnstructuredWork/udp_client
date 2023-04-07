import cv2
import time

from nvjpeg import NvJpeg
from threading import Thread
from turbojpeg import TurboJPEG

from src.load_cfg import LoadConfig
from src.webcam.webcam_set import CamSet
from src.webcam.resolution import get_resolution

from datetime import datetime

class Streamer:
    def __init__(self, config_path):
        self.openCL = False

        if cv2.ocl.haveOpenCL():
            cv2.ocl.setUseOpenCL(True)
            self.openCL = True

        self.l_cam = None
        self.r_cam = None

        self.current_time = time.time()
        self.preview_time = time.time()

        self.sec = 0

        self.l_cam_thread = None
        self.r_cam_thread = None

        self.l_img = None
        self.r_img = None

        self.config = LoadConfig(config_path).info
        self.stat = self.config["show_fps"]

        if self.config["gpu_compression"]:
            self.comp = NvJpeg()
        else:
            self.comp = TurboJPEG()

        w, h = get_resolution(self.config["stream_resolution"])

        self.out_width = w
        self.out_height = h

        self.l_frame_time_cloud = None
        self.r_frame_time_cloud = None
        self.l_frame_time_unity = None
        self.r_frame_time_unity = None

        self.started = False

    def run(self):
        print("")
        print("[INFO] Web camera stream service start.")
        print(f"[INFO] OpenCL activate: {self.openCL}")
        self.stop()

        self.l_cam = CamSet(self.config, "left")
        print(f"[INFO] Left  camera initialization complete.")
        self.r_cam = CamSet(self.config, "right")
        print(f"[INFO] Right camera initialization complete.")

        self.l_cam_thread = Thread(target=self.l_cam_update, args=())
        self.l_cam_thread.daemon = False
        self.l_cam_thread.start()

        self.r_cam_thread = Thread(target=self.r_cam_update, args=())
        self.r_cam_thread.daemon = False
        self.r_cam_thread.start()

        self.started = True

        print("[INFO] All camera connections are complete.")

    def stop(self):
        self.started = False

        if self.l_cam is not None or self.r_cam is not None:
            self.l_cam.release()
            self.r_cam.release()

        print("[INFO] All camera stopped.")

    def l_cam_update(self):
        while True:
            if self.started:
                ret, frame = self.l_cam.read()

                if ret:
                    self.l_img = frame

    def r_cam_update(self):
        while True:
            if self.started:
                ret, frame = self.r_cam.read()

                if ret:
                    self.r_img = frame

    def l_frame_bytescode_cloud(self):
        frame = self.l_img
        frame = cv2.resize(frame, dsize=(960, 540), fx=0.5, fy=0.5,
                                 interpolation=cv2.INTER_AREA)

        self.l_frame_time_cloud = datetime.now().time().isoformat().encode('utf-8')

        return self.comp.encode(frame, 40)

    def l_frame_bytescode_unity(self):
        frame = self.l_img
        frame = cv2.resize(frame, dsize=(self.out_width * 1, self.out_height), fx=0.5, fy=0.5,
                           interpolation=cv2.INTER_AREA)

        self.l_frame_time_unity = datetime.now().time().isoformat().encode('utf-8')

        return self.comp.encode(frame, 40)

    def r_frame_bytescode_cloud(self):
        frame = self.r_img
        frame = cv2.resize(frame, dsize=(960, 540), fx=0.5, fy=0.5,
                                 interpolation=cv2.INTER_AREA)

        self.r_frame_time_cloud = datetime.now().time().isoformat().encode('utf-8')

        return self.comp.encode(frame, 40)

    def r_frame_bytescode_unity(self):
        frame = self.r_img
        frame = cv2.resize(frame, dsize=(self.out_width * 1, self.out_height), fx=0.5, fy=0.5,
                             interpolation=cv2.INTER_AREA)

        self.r_frame_time_unity = datetime.now().time().isoformat().encode('utf-8')

        return self.comp.encode(frame, 40)

    def fps(self):
        self.current_time = time.time()
        self.sec = self.current_time - self.preview_time
        self.preview_time = self.current_time

        if self.sec > 0:
            fps = round((1/self.sec), 1)

        else:
            fps = 1

        return fps

    def __exit__(self):
        print("[INFO] Streamer class exit")
        self.l_cam.release()
        self.r_cam.release()
