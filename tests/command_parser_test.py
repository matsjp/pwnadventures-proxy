import unittest
from command_parsers import *
from proxy import *
import sys
from io import StringIO


def check_if_help_message(message):
    """Help message strings printed by the input parsers are supposed to contain
    "The commands are"
    somewhere in them"""
    return "The commands are" in message


def get_printed_output_from_command(parser, command):
    old_stdout = sys.stdout
    io = StringIO()
    sys.stdout = io

    parser.run_command(command)
    sys.stdout = old_stdout
    return io


class InputParserTest(unittest.TestCase):
    def setUp(self):
        host = '0.0.0.0'
        port = 3333
        proxy = Proxy(host, port, host, port, "name")
        proxy_list = [proxy]
        proxy_collection = ProxyCollection(proxy_list)
        self.input_parser = InputParser(proxy_collection)

    def test_shutdown_command(self):
        command = "shutdown"
        self.assertRaises(SystemExit, self.input_parser.run_command, command)

    def test_invalid_command(self):
        command = "randomnonsense"

        io = get_printed_output_from_command(self.input_parser, command)

        help_command_bool = check_if_help_message(io.getvalue())

        self.assertTrue(help_command_bool)

    def test_help_short_flag(self):
        command = "-h"

        io = get_printed_output_from_command(self.input_parser, command)

        help_command_bool = check_if_help_message(io.getvalue())

        self.assertTrue(help_command_bool)

    def test_help_long_flag(self):
        command = "--help"

        old_stdout = sys.stdout
        io = StringIO()
        sys.stdout = io

        self.input_parser.run_command(command)
        sys.stdout = old_stdout

        help_command_bool = check_if_help_message(io.getvalue())

        self.assertTrue(help_command_bool)

    #TODO: figure out how to implement a test for the proxy command
    #see python mock lib, might help

class ProxyCommandParserTest(unittest.TestCase):
    def setUp(self):
        host = '0.0.0.0'
        port = 3333
        proxy = Proxy(host, port, host, port, "name")
        proxy_list = [proxy]
        self.proxy_collection = ProxyCollection(proxy_list)
        self.proxy_command_parser = ProxyCommandParser(self.proxy_collection)

    def test_invalid_command(self):
        command = "randomnonsense"

        io = get_printed_output_from_command(self.proxy_command_parser, command)

        help_command_bool = check_if_help_message(io.getvalue())

        self.assertTrue(help_command_bool)

    def test_help_short_flag(self):
        command = "-h"

        io = get_printed_output_from_command(self.proxy_command_parser, command)

        help_command_bool = check_if_help_message(io.getvalue())

        self.assertTrue(help_command_bool)

    def test_help_long_flag(self):
        command = "--help"

        io = get_printed_output_from_command(self.proxy_command_parser, command)

        help_command_bool = check_if_help_message(io.getvalue())

        self.assertTrue(help_command_bool)

    def test_ls_command(self):
        command = "ls"

        io = get_printed_output_from_command(self.proxy_command_parser, command)

        #name is the name of the proxy
        #if name is in io.getvalue then the name of the proxy was printed
        self.assertTrue("name" in io.getvalue())

    def test_get_command_when_no_selected_proxy(self):
        self.proxy_collection.selected_proxy = None
        command = "get"

        io = get_printed_output_from_command(self.proxy_command_parser, command)

        self.assertTrue("There is no selected proxy" in io.getvalue())

    def test_get_command_when_selected_proxy(self):
        self.proxy_command_parser.run_command("select name")
        command = "get"

        io = get_printed_output_from_command(self.proxy_command_parser, command)

        self.assertTrue("Selected proxy:" in io.getvalue())

    def test_select_no_name_provided(self):
        command = "select"

        io = get_printed_output_from_command(self.proxy_command_parser, command)

        self.assertTrue("You need to provide the name of a proxy to change to" in io.getvalue())

    def test_select_when_target_already_selected(self):
        self.proxy_command_parser.run_command("select name")
        command = "select name"

        io = get_printed_output_from_command(self.proxy_command_parser, command)

        self.assertTrue("name is already the selected proxy" in io.getvalue())

    def test_select_invalid_proxy(self):
        invalid_proxy_name = "invalid_proxy_name"
        command = "select {}".format(invalid_proxy_name)

        io = get_printed_output_from_command(self.proxy_command_parser, command)

        self.assertTrue("A proxy with the name {} does not exist".format(invalid_proxy_name) in io.getvalue())

    def test_select_unselected_valid_proxy(self):
        self.proxy_collection.selected_proxy = None

        valid_proxy_name = "name"
        command = "select {}".format(valid_proxy_name)

        io = get_printed_output_from_command(self.proxy_command_parser, command)

        self.assertTrue("The selected proxy is now {}".format(valid_proxy_name) in io.getvalue())





if __name__ == 'main':
    unittest.main()
