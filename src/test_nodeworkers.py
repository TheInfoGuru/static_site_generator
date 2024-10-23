import unittest

from textnode import *
from node_workers import *


class TestNodeConversion(unittest.TestCase):
    # Base tests for Text Node Here ----------------
    def test_eq(self):
        node = TextNode("This is a **text** node", TextType.TEXT)
        node2 = TextNode("This **is** a text **node** with two", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], '**', TextType.BOLD)
        self.assertEqual(len(new_nodes), node2)


if __name__ == "__main__":
    unittest.main()