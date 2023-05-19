import time
import h5py

from .file_play import FilePlay
from src.parallel import thread_method

class H5Player(FilePlay):
    def __init__(self, file_path, side):
        super().__init__(file_path)

        self.side = side

    @thread_method
    def run(self):
        if self.side == 'DETECTION':
            self.update1()
        elif self.side == 'MONO_DEPTH':
            self.update2()

    def update1(self):
        hdf5 = h5py.File(self.file, 'r')
        total_index = len(hdf5['classes'])
        index = 0

        frame_duration = 1 / 10         # FPS : 10

        self.curr_time = time.perf_counter()

        while True:
            elapsed_time = self.curr_time - self.prev_time
            if elapsed_time > frame_duration:
                classes = hdf5['classes'][str(index)][:]
                bboxes = hdf5['bboxes'][str(index)][:]
                mask = hdf5['mask'][str(index)][:]

                self.result = classes, bboxes, mask
                self.prev_time = time.perf_counter()

                index += 1
            else:
                self.curr_time = time.perf_counter()

            if index == total_index:
                hdf5 = h5py.File(self.file, 'r')
                index = 0

    def update2(self):
        hdf5 = h5py.File(self.file, 'r')
        total_index = len(hdf5)
        index = 0

        frame_duration = 1 / 10         # FPS : 10

        self.curr_time = time.perf_counter()

        while True:
            elapsed_time = self.curr_time - self.prev_time
            if elapsed_time > frame_duration:
                frame = hdf5[str(index)][:]

                self.result = frame
                self.prev_time = time.perf_counter()

                index += 1
            else:
                self.curr_time = time.perf_counter()

            if index == total_index:
                hdf5 = h5py.File(self.file, 'r')
                index = 0