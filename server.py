import socket
import threading


class Client(threading.Thread):
    def __init__(self, address, connection, client_id):
        threading.Thread.__init__(self)
        self.id = client_id
        self.address = address
        self.conn = connection
        self.isRunning = True

        self.start()

    def send(self, packet):
        packet = bytes(packet, 'utf-8')
        self.conn.sendall(packet)

    def run(self):
        while self.isRunning:
            data = self.conn.recv(1024)
            if not data:
                server.clients.pop(server.clients.index(self))
                self.isRunning = False
                break
            data = data.decode().split("|")
            print(data)
            if data[0] == "new":
                server.send_all_but(self.id, "new|" + data[1] + "|" + data[2])


class Receiver(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        print("starting the receiver, waiting for sockets")
        self.host = host
        self.port = port
        self.clients = 0
        self.start()

    def run(self):
        local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        local_socket.bind((self.host, self.port))
        while True:
            local_socket.listen()
            conn, address = local_socket.accept()
            client = Client(address, conn, self.clients)
            server.clients.append(client)
            self.clients += 1


class Server:
    def __init__(self, contents):
        self.clients = []
        self.contents = contents

    def send_all(self, packet):
        for client in self.clients:
            client.send(packet)

    def send_all_but(self, id, packet):
        for client in self.clients:
            if client.id != id:
                client.send(packet)


server = Server("hello world")
network = Receiver("127.0.0.1", 12345)
