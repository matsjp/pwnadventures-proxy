import argparse
import sys


class InputParser:

    def __init__(self, proxy_list):
        self.proxy_list = proxy_list
        self.selected_proxy = None
        self.command = None
        self.proxy_command = ProxyCommand(self)

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

        if args.command == 'proxy':
            getattr(self, args.command)()
        else:
            getattr(self, args.command)()

    def shutdown(self):
        print('Shutting down')
        sys.exit()

    def proxy(self):
        command = " ".join(self.command.split()[1:])
        print(command)
        self.proxy_command.run_command(command)


class ProxyCommand:
    def __init__(self, input_parser):
        self.input_parser = input_parser
        self.command = None

    def run_command(self, command):
        self.command = command
        parser = argparse.ArgumentParser(description="Allows you to choose proxy server to interact with", usage='''<command> [<args<]
        The commands are:
            ls        Lists all proxy servers by name
            get         Displays the currently selected proxy server
            change         Changes the proxy server
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
        print("Command: {}".format(args.command))
        getattr(self, args.command)()

    def ls(self):
        print(1)
        print(self.input_parser.proxy_list)
        for proxy in self.input_parser.proxy_list:
            print("Proxy: {}".format(proxy.name))

    def get(self):
        if self.input_parser.selected_proxy is None:
            print('There is no selected proxy')
        else:
            print("Selected proxy: {}".format(self.input_parser.selected_proxy.name))

    def change(self):
        try:
            new_proxy_name = self.command.split()[1:2][0]
        except IndexError:
            print("You need to provide the name of a proxy to change to")
            return

        if self.input_parser.selected_proxy is not None:
            if self.input_parser.selected_proxy.name == new_proxy_name:
                print("{} is already the selected proxy".format(self.input_parser.selected_proxy.name))
                return

        changed = False
        for proxy in self.input_parser.proxy_list:
            if new_proxy_name == proxy.name:
                self.input_parser.selected_proxy = proxy
                changed = True

        if changed:
            print("The selected proxy is now {}".format(self.input_parser.selected_proxy.name))
        else:
            print("A proxy with the name {} does not exist".format(new_proxy_name))