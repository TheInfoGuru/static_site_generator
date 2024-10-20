import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag='<a>', value='Google', children=None, props={'href': 'https://www.google.com/'})
        self.assertEqual(' href="https://www.google.com/"', node.props_to_html())

    def test_repr(self):
        node = HTMLNode(tag='<a>', value='Google', children=None, props={'href': 'https://www.google.com/'})
        self.assertEqual("HTMLNode(tag=<a>, value=Google, children=None, props={'href': 'https://www.google.com/'})", repr(node))

    def test_children_length(self):
        node_child1 = HTMLNode(tag='<a>', value='Google', children=None, props={'href': 'https://www.google.com/'})
        node_child2 = HTMLNode(tag='<i>', value='This is my sentence', children=None, props=None)
        node_parent = HTMLNode(tag='<b>', value=None, children=[node_child1, node_child2], props=None)
        self.assertEqual(len(node_parent.children), 2)

    def test_children_type(self):
        node_child1 = HTMLNode(tag='<a>', value='Google', children=None, props={'href': 'https://www.google.com/'})
        node_child2 = HTMLNode(tag='<i>', value='This is my sentence', children=None, props=None)
        node_parent = HTMLNode(tag='<b>', value=None, children=[node_child1, node_child2], props=None)
        self.assertIsInstance(node_parent.children, list) 

    def test_default_types(self):
        node1 = HTMLNode()
        self.assertIsInstance(node1, HTMLNode) 

    def test_repr_none(self):
        node1 = HTMLNode()
        self.assertEqual("HTMLNode(tag=None, value=None, children=None, props=None)", repr(node1))

    def test_partial_args(self):
        node1 = HTMLNode('<p>', 'my text')
        self.assertEqual(len(vars(node1)), 4)

    def test_props_to_html_none(self):
        node = HTMLNode(tag='<a>', value='Google', children=None)
        self.assertEqual('', node.props_to_html())

if __name__ == "__main__":
    unittest.main()