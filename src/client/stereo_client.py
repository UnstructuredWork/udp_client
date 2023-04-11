import zlib

from .client import Client
from datetime import datetime
from src.parallel import thread_method

class StereoClient(Client):
    def __init__(self, cfg, meta, side):
        super().__init__(cfg, meta, side)
        self.rgb = None

    def bytescode(self, package):
        rgb = self.rgb
        package.get_img_time = datetime.now().time().isoformat().encode('utf-8')
        package.frame = self.comp.encode(self.resize(rgb, package), 40)

        self.send_udp(package)

    @thread_method
    def run(self, data):
        check = zlib.crc32(data)
        if self.duplicate_check != check:
            self.duplicate_check = check
            self.rgb = data
            if self.pack_cloud is not None:
                self.bytescode(self.pack_cloud)

            if self.pack_unity is not None:
                self.bytescode(self.pack_unity)