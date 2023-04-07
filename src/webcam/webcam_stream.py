import time
import cv2
import numpy as np
from threading import Thread

from src.webcam.webcam_set import CamSet
from src.webcam.resolution import get_resolution


class Streamer:
    def __init__(self, cfg):
        self.openCL = False

        if cv2.ocl.haveOpenCL():
            cv2.ocl.setUseOpenCL(True)
            self.openCL = True
        self.cfg = cfg

        self.cam = None

        self.current_time = time.time()
        self.preview_time = time.time()

        self.sec = 0

        self.main_thread  = None
        self.l_cam_thread = None
        # self.r_cam_thread = None

        self.l_img = None
        # self.r_img = None
        self.lr_img = None

        self.stat = self.cfg

        w, h = get_resolution(self.config["stream_resolution"])

        self.out_width = w
        self.out_height = h

        self.started = False

    def run(self):
        print("")
        print("[INFO] Web camera stream service start.")
        print(f"[INFO] OpenCL activate: {self.openCL}")
        self.stop()

        self.l_cam = CamSet(self.config, "left")
        print(f"[INFO] Left  camera initialization complete.")
        # self.r_cam = CamSet(self.config, "right")
        # print(f"[INFO] Right camera initialization complete.")

        if self.main_thread is None:
            self.l_cam_thread = Thread(target=self.l_cam_update, args=())
            self.l_cam_thread.daemon = False
            self.l_cam_thread.start()
        #
        #     self.r_cam_thread = Thread(target=self.r_cam_update, args=())
        #     self.r_cam_thread.daemon = False
        #     self.r_cam_thread.start()
        #
            self.main_thread = Thread(target=self.update, args=())
            self.main_thread.daemon = False
            self.main_thread.start()
        self.started = True

        print("[INFO] All camera connections are complete.")

    def stop(self):
        self.started = False

        if self.l_cam is not None:
        # if self.l_cam is not None or self.r_cam is not None:
            self.l_cam.release()
            # self.r_cam.release()

        print("[INFO] All camera stopped.")

    def l_cam_update(self):
        while True:
            if self.started:
                ret, frame = self.l_cam.read()

                if ret:
                    self.l_img = frame

    # def r_cam_update(self):
    #     while True:
    #         if self.started:
    #             ret, frame = self.r_cam.read()
    #
    #             if ret:
    #                 self.r_img = frame

    def update(self):
        time.sleep(0.1)
        while True:
            if self.started:
                if self.l_img is not None:
                # if self.l_img is not None and self.r_img is not None:
                    self.lr_img = self.l_img

    def bytescode(self):
        frame = self.lr_img

        frame = cv2.resize(frame, dsize=(self.out_width, self.out_height), fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

        if self.stat:
            cv2.rectangle(frame, (0, 0), (120, 30), (0, 0, 0), -1)
            fps = f"FPS : {str(self.fps())}"
            cv2.putText(frame, fps, (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1, cv2.LINE_AA)

        return cv2.imencode(".jpg", frame)[1].tobytes()

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
        # self.r_cam.release()