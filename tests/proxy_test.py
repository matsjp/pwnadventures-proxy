import unittest
from proxy import *


class ProxyCollectionTest(unittest.TestCase):
    def setUp(self):
        host = '0.0.0.0'
        port = 3333
        proxy = Proxy(host, port, host, port, "name")
        self.proxy_list = [proxy]

    def test_initialize_with_incorrect_list_content(self):
        lst = ["This is a string, not a Proxy object"]
        self.assertRaises(TypeError, ProxyCollection, lst)

    def test_initialize_with_wrong_argument_type(self):
        arg = "This is a string, not a list"
        self.assertRaises(TypeError, ProxyCollection, arg)

    def test_initialize_with_correct_argument(self):
        proxy_collection = ProxyCollection(self.proxy_list)
        self.assertEqual(self.proxy_list, proxy_collection.proxy_list)


if __name__ == 'main':
    unittest.main()
