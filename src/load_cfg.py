import yaml

class LoadConfig():
    def __init__(self, path):
        self.path = path
        self.info = None

        self.load_config()

    def load_config(self):
        try:
            with open(self.path, 'r') as f:
                self.info = yaml.load(f, Loader=yaml.FullLoader)
        except:
            print(f"[Error] Config file open fail.")
            print(f"[Error] Your path is [{self.path}]")


