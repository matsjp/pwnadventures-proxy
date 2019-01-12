import socket
from threading import Thread
import data_parsers
import importlib


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
                    importlib.reload(data_parsers)
                    data_parsers.parse("client", self.port, data)
                #TODO: better exception handling, handle more specific exceptions
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
        print("Proxy has connected to server on port {}".format(port))

    def run(self):
        while True:
            data = self.server_connection.recv(4096)
            if data:
                try:
                    importlib.reload(data_parsers)
                    data_parsers.parse("server", self.port, data)
                #TODO: better exception handling, handle more specific exceptions
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


class ProxyCollection:
    def __init__(self, proxy_list):
        if not isinstance(proxy_list, list):
            raise TypeError("The proxy_list argument is of type {} while expected type is {}".format(
                type(proxy_list), list))
        for proxy in proxy_list:
            if not isinstance(proxy, Proxy):
                raise TypeError("The proxy_list contains some element which is not a {} object".format(Proxy))
        self.proxy_list = proxy_list
        self.selected_proxy = None
