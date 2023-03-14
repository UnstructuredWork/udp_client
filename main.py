from src.client import Client

HOST = ["10.252.101.139"]

PORT = [5001]

client = Client(HOST, PORT)

if __name__ == '__main__':
    client.run()