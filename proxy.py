import socket
from threading import Thread
import dataParser
import importlib
import inputParser


class ClientToProxy(Thread):
    def __init__(self, host, port):
        super(ClientToProxy, self).__init__()
        self.host = host
        self.port = port
        self.server_connection = None
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(1)
        self.client_connection, addr = sock.accept()
        print("Client has connectet to proxy on port {}".format(port))

    def run(self):
        while True:
            data = self.client_connection.recv(4096)
            if data:
                try:
                    importlib.reload(dataParser)
                    dataParser.parse("client", self.port, data)
                except Exception as e:
                    print(e)
                    continue
                self.server_connection.sendall(data)


class ProxyToServer(Thread):
    def __init__(self, host, port):
        super(ProxyToServer, self).__init__()
        self.host = host
        self.port = port
        self.client_connection = None
        self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_connection.connect((self.host, self.port))
        print("Proxy has connectet to server on port {}".format(port))

    def run(self):
        while True:
            data = self.server_connection.recv(4096)
            if data:
                #print("{} <- {}".format(self.port, data.hex()))
                try:
                    importlib.reload(dataParser)
                    dataParser.parse("server", self.port, data)
                except Exception as e:
                    print(e)
                    continue
                self.client_connection.sendall(data)


class Proxy(Thread):
    def __init__(self, client_host, client_port, server_host, server_port, name):
        super(Proxy, self).__init__()
        self.client_host = client_host
        self.client_port = client_port
        self.server_host = server_host
        self.server_port = server_port
        self.name = name

    def run(self):
        print("Setting up proxy on port {}".format(self.client_port))
        client_to_proxy = ClientToProxy(self.client_host, self.client_port)
        proxy_to_server = ProxyToServer(self.server_host, self.server_port)

        client_to_proxy.server_connection = proxy_to_server.server_connection
        proxy_to_server.client_connection = client_to_proxy.client_connection

        client_to_proxy.start()
        proxy_to_server.start()
        print("Proxy on port {} established".format(self.client_port))

host = '127.0.0.1'
client_port_master = 3333
server_port_master = 5555

client_port_game0 = 3000
server_port_game0 = 5000

client_port_game1 = 3001
server_port_game1 = 5001

client_port_game2 = 3002
server_port_game2 = 5002

client_port_game3 = 3003
server_port_game3 = 5003

client_port_game4 = 3004
server_port_game4 = 5004

client_port_game5 = 3005
server_port_game5 = 5005

master_proxy = Proxy(host, client_port_master, host, server_port_master, 'master_proxy')

master_proxy.start()
game_proxy0 = Proxy(host, client_port_game0, host, server_port_game0, 'game_proxy0')
game_proxy1 = Proxy(host, client_port_game1, host, server_port_game1, 'game_proxy1')
game_proxy2 = Proxy(host, client_port_game2, host, server_port_game2, 'game_proxy2')
game_proxy3 = Proxy(host, client_port_game3, host, server_port_game3, 'game_proxy3')
game_proxy4 = Proxy(host, client_port_game4, host, server_port_game4, 'game_proxy4')
game_proxy5 = Proxy(host, client_port_game5, host, server_port_game5, 'game_proxy5')

proxies = [master_proxy, game_proxy0, game_proxy1, game_proxy2, game_proxy3, game_proxy4, game_proxy5]

game_proxy0.start()
game_proxy1.start()
game_proxy2.start()
game_proxy3.start()
game_proxy4.start()
game_proxy5.start()
input_parser = inputParser.InputParser(proxies)

while True:
    cmd = input("$ ")
    input_parser.run_command(cmd)