# import modules
import socket
import threading


class Client(threading.Thread):
    def __init__(self, host, port, editor):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.editor = editor
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.start()

    def run(self):
        print("attempting to connect to server")
        while True:
            data = self.socket.recv(1024)
            if not data:
                self.disconnect()
            data = data.decode().split("|")
            if data[0] == "new":
                print(data)
                self.editor.insert(data[1], data[2])

    def send(self, packet):
        self.socket.send(bytes(packet, 'utf-8'))

    def disconnect(self):
        print("disconnected")
        self.socket.close()
        exit()
