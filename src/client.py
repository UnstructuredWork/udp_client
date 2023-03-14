import os
import math
import zlib
import socket
import struct

from src.kinect.kinect_stream import Kinect

current_dir = os.getcwd()
config_file = os.path.join(current_dir, "config/config.yaml")

kinect = Kinect(config_file)
kinect.run()

class Package:
    def __init__(self, HOST, PORT):
        self.host = HOST
        self.port = PORT
        self.index = len(PORT)

        self.imu   = None
        self.frame = None

        self.get_img_time = None

class Client:
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT

        self.sock = None
        self.sock_udp()

        self.img_num = 1

        self.duplicate_check = None

        self.prev_time = 0
        self.curr_time = 0

        self.frame_duration = 1 / 60

        self.MAX_IMAGE_DGRAM = 2 ** 16 - 256

        self.pack_unity = Package(self.HOST[0], self.PORT[0:1])

    def __del__(self):
        self.sock.close()

    def sock_udp(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def udp_header(self, frame):
        checksum = zlib.crc32(frame)
        header = struct.pack("!I", checksum)

        return header

    def send_udp(self, package, index=0):
        udp_header = self.udp_header(package.frame)
        size = len(package.frame)
        count = math.ceil(size / (self.MAX_IMAGE_DGRAM))
        total_count = count
        array_pos_start = 0
        if self.img_num > 99:
            self.img_num = 1

        while count:
            array_pos_end = min(size, array_pos_start + self.MAX_IMAGE_DGRAM)
            packet_num = (str(self.img_num).zfill(3) + '-' +
                          str(total_count) + '-' +
                          str(total_count - count + 1)).encode('utf-8')
            try:
                self.sock.sendto(struct.pack("B", count) + b'end' +
                                 udp_header + b'end' +
                                 packet_num + b'end' +
                                 package.get_img_time + b'end' +
                                 str(len(package.frame)).encode('utf-8') + b'end' +
                                 str(array_pos_start).encode('utf-8') + b'end' +
                                 package.imu + b'end' +
                                 package.frame[array_pos_start:array_pos_end], (package.host, package.port[index]))
            except OSError:
                pass

            array_pos_start = array_pos_end
            count -= 1

        self.img_num += 1

    def run(self):
        while True:
            if kinect.imu is not None and kinect.frame is not None:
                check = zlib.crc32(kinect.depth)
                if self.duplicate_check != check:
                    self.duplicate_check = check
                    self.pack_unity.imu = kinect.imu
                    self.pack_unity.frame = kinect.frame
                    self.pack_unity.get_img_time = kinect.frame_time
                    self.send_udp(self.pack_unity)

        kinect.stop()