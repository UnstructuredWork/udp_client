import sys
import cv2

from src.webcam.webcam_prop import CamProp
from src.webcam.find_port import serial2port


class CamSet:
    def __init__(self, prop, loc):
        self.prop = prop
        self.loc = "l_serial" if loc == "left" else "r_serial"

        self.cam = CamProp()
        self.cam_set()

    def cam_set(self):

        try:
            self.cam.set_port(serial2port(self.prop["subsystem"], self.prop[self.loc]))
        except Exception as e:
            print(e)
            print("[ERROR] Retry with the right device serial.")
            print("[ERROR] Process is shutdown.")
            sys.exit()

        self.cam.set_fps(self.prop["fps"])

        try:
            self.cam.set_resolution(self.prop["camera_resolution"])
        except Exception as e:
            print(e)
            print("[WARNING] Resolution will set default value : ['1080']")

        try:
            self.cam.set_format(self.prop["format"])
        except Exception as e:
            print(e)
            print("[WARNING] Pixel format will set default value : ['NV12']")

        try:
            self.cam.set_capture(cv2.VideoCapture(self.cam.get_port()))
            self.cam.set_codec()
        except Exception as e:
            print(e)

    def get_width(self):
        return self.cam.get_width()

    def get_height(self):
        return self.cam.get_height()

    def read(self):
        _, img = self.cam.get_capture().read()
        if self.cam.get_format() == "NV12" and _:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return _, img

    def release(self):
        self.cam.get_capture().release()

    def isOpened(self):
        return self.cam.get_capture().isOpened()

