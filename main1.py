from threading import Thread
from src.client.sony_client import LeftClient, RightClient

left = LeftClient()
right = RightClient()

l_thr = Thread(target=left.run, args=())
r_thr = Thread(target=right.run, args=())

if __name__ == "__main__":
    l_thr.start()
    r_thr.start()
