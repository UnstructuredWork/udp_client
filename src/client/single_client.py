import cv2
import zlib
import pickle

from .client import Client
from datetime import datetime
from src.parallel import thread_method

class SingleDataClient(Client):
    def __init__(self, cfg, side):
        super().__init__(cfg, side)
        self.data = None

    def bytescode(self, package):
        data = self.data
        package.get_img_time = datetime.now().time().isoformat().encode('utf-8')
        if self.side == 'STEREO_L' or self.side == 'STEREO_R':
            package.frame = self.comp.encode(self.resize(data, package), 40)
        elif self.side == 'DETECTION':
            package.frame = zlib.compress(pickle.dumps(data))
        elif self.side == 'MONO_DEPTH':
            package.frame = cv2.imencode('.png', self.resize(data, package), [cv2.IMWRITE_PNG_COMPRESSION, 4])[1].tobytes()

        self.send_udp(package)

    @thread_method
    def run(self, data):
        if self.side == 'DETECTION':
            check = zlib.crc32(data[0])
        else:
            check = zlib.crc32(data)

        if self.duplicate_check != check:
            self.duplicate_check = check
            self.data = data
            if self.pack_cloud is not None:
                self.bytescode(self.pack_cloud)

            if self.pack_unity is not None:
                self.bytescode(self.pack_unity)