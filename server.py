import socket
import sys
import time
import threading

class Server:

        connections = []
        peers = []

        def __init__(self):
                try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                except socket.error:
                        print("ERROR: Failed while trying to create socket")
                server_ip = sys.argv[1]
                server_port = sys.argv[2]
                sock.bind((server_ip, int(server_port)))
                sock.listen(5)

                while True:
                        c, a = sock.accept()
                        cThread = threading.Thread(target = self.handler, args = (c,a))
                        cThread.daemon = True
                        cThread.start()
                        self.connections.append(c)
                        self.peers.append(a[0])
                        print(str(a[0]) + ":" + str(a[1]), "connected")
                        self.sendPeers()


        def sendPeers(self):
                p = ""
                for peer is self.peers:
                        p = p + peer + ","

                for connection in self.connections:
                        connection.send(b'\x11' + bytes(p, 'utf-8'))

        def handler(self, c, a):
                while True:
                        data = c.recv(1024)
                        for connection in self.connections:
                                connection.send(bytes(data))
                        if not data:
                                print(str(a[0]) + ":" + str(a[1]), "disconnected")
                                self.connections.remove(c)
                                self.peers.remove(a[0])
                                c.close()
                                self.sendPeers()
                                break
                        
                
class Client:

        def sendMsg(self, sock):
                while True:
                        sock.send(bytes(input(), 'utf-8'))
                
        def __init__(self, address, port):
                try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                except socket.error:
                        print("ERROR: Failed while trying to create socket")
                sock.connect((address, port))

                iThread = threading.Thread(target = self.sendMsg, args = (sock,))
                iThread.daemon = True
                iThread.start()

                while True:
                        data = sock.recv(1024)
                        if not data:
                                break
                        if data[0:1] == b'\x11':
                                print("got peers")
                        else:
                                print(str(data, 'utf-8'))

if sys.argv[3] == "client":
        client = Client('127.0.0.1', 8080)
else:
        server = Server()
        server.run()
