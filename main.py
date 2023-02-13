from src.client import LeftClient, RightClient
from threading import Thread

UNITY_HOST = "10.252.101.174"  # UNITY PC IP
CLOUD_HOST = "10.252.101.191"  # CLOUD PC IP

HOST = [UNITY_HOST, CLOUD_HOST]

LEFT_PORT = [5001, 5003, 5005, 5007]
RIGHT_PORT = [5002, 5004, 5006]

left = LeftClient(HOST, LEFT_PORT)
right = RightClient(HOST, RIGHT_PORT)

l_thr = Thread(target=left.run, args=())
r_thr = Thread(target=right.run, args=())

if __name__ == "__main__":
    l_thr.start()
    r_thr.start()