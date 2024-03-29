from fvcore.common.config import CfgNode as CN


_C = CN()

_C.VERSION = 0.1
_C.CUDA = False
_C.OCL = False


_C.SYSTEM = CN()

_C.SYSTEM.LOG = CN()
_C.SYSTEM.LOG.SAVE = False
_C.SYSTEM.LOG.SHOW = True
_C.SYSTEM.LOG.PRINT_PERIOD = 10

_C.SYSTEM.SYNC = CN()
_C.SYSTEM.SYNC.SERVER = ""
_C.SYSTEM.SYNC.RESTART = True
_C.SYSTEM.SYNC.TOLERANCE = 10


_C.SERVER = CN()

_C.SERVER.CLOUD = CN()
_C.SERVER.CLOUD.HOST = []
_C.SERVER.CLOUD.PORT = CN()
_C.SERVER.CLOUD.PORT.STEREO_L = 0
_C.SERVER.CLOUD.PORT.STEREO_R = 0
_C.SERVER.CLOUD.PORT.RGBD = 0
_C.SERVER.CLOUD.SIZE = CN()
_C.SERVER.CLOUD.SIZE.STEREO_L = [1920, 1080]
_C.SERVER.CLOUD.SIZE.STEREO_R = [1920, 1080]
_C.SERVER.CLOUD.SIZE.RGBD = [540, 360]
_C.SERVER.CLOUD.SEND = False

_C.SERVER.UNITY = CN()
_C.SERVER.UNITY.HOST = []
_C.SERVER.UNITY.PORT = CN()
_C.SERVER.UNITY.PORT.STEREO_L = 0
_C.SERVER.UNITY.PORT.STEREO_R = 0
_C.SERVER.UNITY.PORT.RGBD = 0
_C.SERVER.UNITY.SIZE = CN()
_C.SERVER.UNITY.SIZE.STEREO_L = [1920, 1080]
_C.SERVER.UNITY.SIZE.STEREO_R = [1920, 1080]
_C.SERVER.UNITY.SIZE.RGBD = [540, 360]
_C.SERVER.UNITY.SEND = False


_C.HW_INFO = CN()

_C.HW_INFO.STEREO_L = CN()
_C.HW_INFO.STEREO_L.TYPE = 'sony'
_C.HW_INFO.STEREO_L.SIZE = [1920, 1080]
_C.HW_INFO.STEREO_L.USE = True
_C.HW_INFO.STEREO_L.FPS = 60
_C.HW_INFO.STEREO_L.SERIAL = 0
_C.HW_INFO.STEREO_L.FORMAT = "YUYV"

_C.HW_INFO.STEREO_R = CN()
_C.HW_INFO.STEREO_R.TYPE = 'sony'
_C.HW_INFO.STEREO_R.SIZE = [1920, 1080]
_C.HW_INFO.STEREO_R.USE = True
_C.HW_INFO.STEREO_R.FPS = 60
_C.HW_INFO.STEREO_R.SERIAL = 0
_C.HW_INFO.STEREO_R.FORMAT = "YUYV"

_C.HW_INFO.RGBD = CN()
_C.HW_INFO.RGBD.TYPE = 'kinect'
_C.HW_INFO.RGBD.SIZE = [1920, 1080]
_C.HW_INFO.RGBD.USE = True
_C.HW_INFO.RGBD.FPS = 30
_C.HW_INFO.RGBD.SERIAL = ""
_C.HW_INFO.RGBD.FORMAT = ""
