import os
import zlib

from threading import Thread
from .client import Client, Package
from src.load_cfg import LoadConfig
from src.webcam.webcam_dual_stream import Streamer

current_dir = os.getcwd()
config_file = os.path.join(current_dir, "config/config.yaml")

streamer = Streamer(config_file)
streamer.run()

class LeftClient(Client):
    def __init__(self):
        super().__init__()
        self.config = LoadConfig(config_file).info
        self.pack_unity = Package(self.config["unity_host"], self.config["l_cam_port"][0:1])
        self.pack_cloud = Package(self.config["cloud_host"], self.config["l_cam_port"][1:])

    def thread_order(self, func1, func2):
        img_cloud = Thread(target=func1, args=())
        img_cloud.start()

        img_unity = Thread(target=func2, args=())
        img_unity.start()

        send_cloud = Thread(target=self.multi_thread_send, args=(self.pack_cloud,))
        send_cloud.start()

        send_unity = Thread(target=self.single_thread_send, args=(self.pack_unity,))
        send_unity.start()

    def get_image_cloud(self):
        self.pack_cloud.frame = streamer.l_frame_bytescode_cloud()
        self.pack_cloud.get_img_time = streamer.l_frame_time_cloud

    def get_image_unity(self):
        self.pack_unity.frame = streamer.l_frame_bytescode_unity()
        self.pack_unity.get_img_time = streamer.l_frame_time_unity

    def run(self):
        while True:
            if streamer.l_img is not None:
                check = zlib.crc32(streamer.l_img)
                if self.duplicate_check != check:
                    self.thread_order(self.get_image_cloud(), self.get_image_unity())
                    self.duplicate_check = check

class RightClient(Client):
    def __init__(self):
        super().__init__()
        self.config = LoadConfig(config_file).info
        self.pack_unity = Package(self.config["unity_host"], self.config["r_cam_port"][0:1])
        self.pack_cloud = Package(self.config["cloud_host"], self.config["r_cam_port"][1:])

    def thread_order(self, func1, func2):
        img_cloud = Thread(target=func1, args=())
        img_cloud.start()

        img_unity = Thread(target=func2, args=())
        img_unity.start()

        send_cloud = Thread(target=self.multi_thread_send, args=(self.pack_cloud,))
        send_cloud.start()

        send_unity = Thread(target=self.single_thread_send, args=(self.pack_unity,))
        send_unity.start()

    def get_image_cloud(self):
        self.pack_cloud.frame = streamer.r_frame_bytescode_cloud()
        self.pack_cloud.get_img_time = streamer.r_frame_time_cloud

    def get_image_unity(self):
        self.pack_unity.frame = streamer.r_frame_bytescode_unity()
        self.pack_unity.get_img_time = streamer.r_frame_time_unity

    def run(self):
        while True:
            if streamer.r_img is not None:
                check = zlib.crc32(streamer.r_img)
                if self.duplicate_check != check:
                    self.thread_order(self.get_image_cloud(), self.get_image_unity())
                    self.duplicate_check = check