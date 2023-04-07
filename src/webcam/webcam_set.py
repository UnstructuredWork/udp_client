import sys
import cv2

from src.webcam.webcam_prop import CamProp
from src.webcam.find_port import serial2port


class CamSet(CamProp):
    def __init__(self, prop, loc):
        super().__init__()

        self.prop = prop
        self.loc = "l_serial" if loc == "left" else "r_serial"

        self.cam_set()

    def cam_set(self):

        try:
            self.set_port(serial2port(self.prop["subsystem"], self.prop[self.loc]))
        except Exception as e:
            print(e)
            print("[ERROR] Retry with the right device serial.")
            print("[ERROR] Process is shutdown.")
            sys.exit()

        self.set_fps(self.prop["fps"])

        try:
            self.set_resolution(self.prop["camera_resolution"])
        except Exception as e:
            print(e)
            print("[WARNING] Resolution will set default value : ['1080']")

        try:
            self.set_format(self.prop["format"])
        except Exception as e:
            print(e)
            print("[WARNING] Pixel format will set default value : ['NV12']")

        try:
            self.set_capture(cv2.VideoCapture(self.get_port()))
            self.set_codec()
        except Exception as e:
            print(e)

    def get_width(self):
        return self.get_width()

    def get_height(self):
        return self.get_height()

    def read(self):
        _, img = self.get_capture().read()
        if self.get_format() == "NV12" and _:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return _, img

    def release(self):
        self.get_capture().release()

    def isOpened(self):
        return self.get_capture().isOpened()

