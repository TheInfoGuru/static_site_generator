import unittest

from htmlnode import *


class TestLeafNode(unittest.TestCase):
    def test_no_value(self):
        with self.assertRaises(ValueError, msg='All leaf nodes must have a value'):
            node = LeafNode(tag='a', value=None, props={'href': 'https://www.google.com/'})

    def test_no_tag(self):
        node = LeafNode(tag=None, value='This is my value.', props={'href': 'https://www.google.com/'})
        self.assertEqual("This is my value.", node.to_html())

    def test_value(self):
        node = LeafNode(tag='a', value='My value goes here.', props={'href': 'https://www.google.com/'})
        self.assertEqual('a', node.tag)
        self.assertEqual('My value goes here.', node.value)
        self.assertEqual(None, node.children)
        self.assertEqual({'href': 'https://www.google.com/'}, node.props)

    def test_to_html_w_prop(self):
        node = LeafNode(tag='a', value='My value goes here.', props={'href': 'https://www.google.com/'})
        self.assertEqual(f'<a href="https://www.google.com/">My value goes here.</a>', node.to_html())

    def test_to_html_no_prop(self):
        node = LeafNode(tag='p', value='My other value goes here.')
        self.assertEqual(f"<p>My other value goes here.</p>", node.to_html())

if __name__ == "__main__":
    unittest.main()