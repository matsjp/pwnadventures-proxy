import argparse
import sys
import proxy


class InputParser:
    def __init__(self, proxy_collection):
        if not isinstance(proxy_collection, proxy.ProxyCollection):
            raise TypeError("The proxy_collection argument is of type {} while the expected type is {}".format(
                type(proxy_collection), proxy.ProxyCollection))
        self.proxy_collection = proxy_collection
        self.selected_proxy = None
        self.command = None
        self.proxy_command = ProxyCommandParser(proxy_collection)

    def run_command(self, command):
        self.command = command
        parser = argparse.ArgumentParser(description="Interacts with the proxy servers", usage='''<command> [<args>]
        The commands are:
            shutdown        Stops the proxy server
            proxy    Changes the currently selected proxy server
                ''')
        parser.add_argument('command', help='Subcommand to run')

        try:
            args = parser.parse_args(command.split()[:1])
            if not hasattr(self, args.command):
                print('Unrecognized command: {}'.format(args.command))
                parser.print_help()
                return
        except SystemExit:
            return

        getattr(self, args.command)()

    def shutdown(self):
        print('Shutting down')
        sys.exit()

    def proxy(self):
        command = " ".join(self.command.split()[1:])
        self.proxy_command.run_command(command)


class ProxyCommandParser:
    def __init__(self, proxy_collection):
        self.proxy_collection = proxy_collection
        self.command = None

    def run_command(self, command):
        self.command = command
        parser = argparse.ArgumentParser(description="Allows you to choose proxy server to interact with", usage='''<command> [<args<]
        The commands are:
            ls                      Lists all proxy servers by name
            get                     Displays the currently selected proxy server
            select <proxy name>     Select the proxy server to interact with
                ''')
        parser.add_argument('command', help='Subcommand to run')
        try:
            args = parser.parse_args(command.split()[:1])
            if not hasattr(self, args.command):
                print('Proxy: unrecognized command')
                parser.print_help()
                return
        except SystemExit:
            return
        getattr(self, args.command)()

    def ls(self):
        for proxy in self.proxy_collection.proxy_list:
            print("Proxy: {}".format(proxy.name))

    def get(self):
        if self.proxy_collection.selected_proxy is None:
            print('There is no selected proxy')
        else:
            print("Selected proxy: {}".format(self.proxy_collection.selected_proxy.name))

    def select(self):
        try:
            new_proxy_name = self.command.split()[1:2][0]
        except IndexError:
            print("You need to provide the name of a proxy to change to")
            return

        if self.proxy_collection.selected_proxy is not None:
            if self.proxy_collection.selected_proxy.name == new_proxy_name:
                print("{} is already the selected proxy".format(self.proxy_collection.selected_proxy.name))
                return

        selected = False
        for proxy in self.proxy_collection.proxy_list:
            if new_proxy_name == proxy.name:
                self.proxy_collection.selected_proxy = proxy
                selected = True

        if selected:
            print("The selected proxy is now {}".format(self.proxy_collection.selected_proxy.name))
        else:
            print("A proxy with the name {} does not exist".format(new_proxy_name))