import command_parsers
from proxy import *

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

proxy_collection = ProxyCollection(proxies)
input_parser = command_parsers.InputParser(proxy_collection)

while True:
    cmd = input("$ ")
    input_parser.run_command(cmd)