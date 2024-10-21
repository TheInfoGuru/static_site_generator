import unittest

from htmlnode import *

class TestLeafNode(unittest.TestCase):
    def test_default_one_parent_level(self):
        leaf_node_1 = LeafNode(tag='', value='This is the start.')
        parent_node_1 = ParentNode(tag='p', children=[leaf_node_1])
        self.assertEqual('<p>This is the start.</p>', parent_node_1.to_html())

    def test_default_one_parent_no_child(self):
        with self.assertRaises(ValueError):
            parent_node_1 = ParentNode(tag='p') # No child parent
            parent_node_1.to_html()

    def test_default_one_parent_no_tag(self):
        with self.assertRaises(ValueError):
            leaf_node_1 = LeafNode(tag='', value='This is the start.')
            parent_node_1 = ParentNode(children=[leaf_node_1]) # Parent with no tag
            parent_node_1.to_html()

    def test_default_one_parent_child_no_value(self):
        with self.assertRaises(ValueError):
            leaf_node_1 = LeafNode(tag='') # Child with no value
            parent_node_1 = ParentNode(children=[leaf_node_1])
            parent_node_1.to_html()

    def test_default_three_parent_level(self):
        leaf_node_1_parent_1 = LeafNode(tag='', value='This is the start.')
        leaf_node_2_parent_1 = LeafNode(tag='b', value='This is the important next line!')
        leaf_node_1_parent_2 = LeafNode(tag='i', value='This is a wonderful website to go to.')
        leaf_node_2_parent_2 = LeafNode(tag='a', value='This is the start.', props={'href': 'https://google.com/', 'index': 0})
        parent_node_1 = ParentNode(tag='p', children=[leaf_node_1_parent_1, leaf_node_2_parent_1])
        parent_node_2 = ParentNode(tag='p', children=[leaf_node_1_parent_2, leaf_node_2_parent_2])
        parent_node_3 = ParentNode(tag='body', children=[parent_node_1, parent_node_2])
        parent_node_4 = ParentNode(tag='html', children=[parent_node_3], props={'header': 'False'})
        self.maxDiff = None
        self.assertEqual('<html header="False"><body><p>This is the start.<b>This is the important next line!</b></p><p><i>This is a wonderful website to go to.</i><a href="https://google.com/" index="0">This is the start.</a></p></body></html>', parent_node_4.to_html())

    def test_default_multi_level(self):
        leaf_node_1_parent_1 = LeafNode(tag='', value='This is the start.')
        leaf_node_2_parent_3 = LeafNode(tag='b', value='This is the important next line!')
        leaf_node_1_parent_2 = LeafNode(tag='i', value='This is a wonderful website to go to.')
        leaf_node_2_parent_2 = LeafNode(tag='a', value='This is the url.', props={'href': 'https://google.com/', 'index': 0})
        leaf_node_1_parent_5 = LeafNode(tag='', value='This is the last.')
        parent_node_1 = ParentNode(tag='p', children=[leaf_node_1_parent_1])
        parent_node_2 = ParentNode(tag='p', children=[leaf_node_1_parent_2, leaf_node_2_parent_2])
        parent_node_3 = ParentNode(tag='p', children=[leaf_node_2_parent_3])
        parent_node_4 = ParentNode(tag='body', children=[parent_node_1, parent_node_2, parent_node_3])
        parent_node_5 = ParentNode(tag='html', children=[parent_node_4, leaf_node_1_parent_5], props={'header': 'False'})
        self.maxDiff = None
        self.assertEqual('<html header="False"><body><p>This is the start.</p><p><i>This is a wonderful website to go to.</i><a href="https://google.com/" index="0">This is the url.</a></p><p><b>This is the important next line!</b></p></body>This is the last.</html>', parent_node_5.to_html())

    def test_default_multiple_level_missing_tag(self):
        with self.assertRaises(ValueError):
            leaf_node_1_parent_1 = LeafNode(tag='', value='This is the start.')
            leaf_node_2_parent_1 = LeafNode(tag='b', value='This is the important next line!')
            leaf_node_1_parent_2 = LeafNode(tag='i', value='This is a wonderful website to go to.')
            leaf_node_2_parent_2 = LeafNode(tag='a', value='This is the start.', props={'href': 'https://google.com/', 'index': 0})
            parent_node_1 = ParentNode(tag='p', children=[leaf_node_1_parent_1, leaf_node_2_parent_1])
            parent_node_2 = ParentNode(tag='p', children=[leaf_node_1_parent_2, leaf_node_2_parent_2])
            parent_node_3 = ParentNode(tag='body') # Parent without children multiple levels
            parent_node_4 = ParentNode(tag='html', children=[parent_node_3], props={'header': 'False'})
            self.maxDiff = None
            parent_node_4.to_html()


if __name__ == "__main__":
    unittest.main()