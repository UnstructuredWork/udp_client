from __future__ import division
import time
import math
import zlib
import socket
import struct

from threading import Thread

class Package:
    def __init__(self, HOST, PORT):
        self.host = HOST
        self.port = PORT
        self.index = len(PORT)

        self.imu   = None
        self.frame = None

        self.get_img_time = None

class Client:
    def __init__(self):
        self.sock = None
        self.sock_udp()

        self.img_num = 1

        self.duplicate_check = None

        self.prev_time = 0
        self.curr_time = 0

        self.frame_duration = 1 / 60

        self.MAX_IMAGE_DGRAM = 2 ** 16 - 256

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
                if package.imu is None:
                    self.sock.sendto(struct.pack("B", count) + b'end' +
                                     udp_header + b'end' +
                                     packet_num + b'end' +
                                     package.get_img_time + b'end' +
                                     str(len(package.frame)).encode('utf-8') + b'end' +
                                     str(array_pos_start).encode('utf-8') + b'end' +
                                     package.frame[array_pos_start:array_pos_end], (package.host, package.port[index]))
                else:
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

    def single_thread_send(self, package):
        thr = Thread(target=self.send_udp, args=(package,))
        thr.start()

    def multi_thread_send(self, package):
        self.curr_time = time.perf_counter()
        elapsed_time = self.curr_time - self.prev_time
        if elapsed_time > self.frame_duration:
            for index in range(package.index):
                thr = Thread(target=self.send_udp, args=(package, index))
                thr.start()

            self.prev_time = time.perf_counter()