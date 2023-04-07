import os
import zlib

from .client import Client, Package
from src.load_cfg import LoadConfig
from src.kinect.kinect_stream import Kinect

current_dir = os.getcwd()
config_file = os.path.join(current_dir, "config/config.yaml")

kinect = Kinect(config_file)
kinect.run()

class KinectClient(Client):
    def __init__(self):
        super().__init__()
        self.config = LoadConfig(config_file).info
        self.pack_kinect = Package(self.config["unity_host"], self.config["kinect_port"][0:1])

    def kinect_send(self):
        self.pack_kinect.imu = kinect.imu
        self.pack_kinect.frame = kinect.frame
        self.pack_kinect.get_img_time = kinect.frame_time
        self.send_udp(self.pack_kinect)

    def run(self):
        while True:
            if kinect.imu is not None and kinect.frame is not None:
                check = zlib.crc32(kinect.depth)
                if self.duplicate_check != check:
                    self.kinect_send()
                    self.duplicate_check = check

        kinect.stop()