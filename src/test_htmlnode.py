import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    #HTMLNode Tests Below Here ---------------------
    def test_props_to_html(self):
        node = HTMLNode(tag='a', value='Google', children=None, props={'href': 'https://www.google.com/'})
        self.assertEqual(' href="https://www.google.com/"', node.props_to_html())

    def test_multiple_props_to_html(self):
        node = HTMLNode(tag='a', value='Google', children=None, props={'href': 'https://www.google.com/', 'index': 0})
        self.assertEqual(' href="https://www.google.com/" index="0"', node.props_to_html())

    def test_repr(self):
        node = HTMLNode(tag='a', value='Google', children=None, props={'href': 'https://www.google.com/'})
        self.assertEqual("HTMLNode(tag=a, value=Google, children=None, props={'href': 'https://www.google.com/'})", repr(node))

    def test_children_length(self):
        node_child1 = HTMLNode(tag='a', value='Google', children=None, props={'href': 'https://www.google.com/'})
        node_child2 = HTMLNode(tag='i', value='This is my sentence', children=None, props=None)
        node_parent = HTMLNode(tag='b', value=None, children=[node_child1, node_child2], props=None)
        self.assertEqual(len(node_parent.children), 2)

    def test_children_type(self):
        node_child1 = HTMLNode(tag='a', value='Google', children=None, props={'href': 'https://www.google.com/'})
        node_child2 = HTMLNode(tag='i', value='This is my sentence', children=None, props=None)
        node_parent = HTMLNode(tag='b', value=None, children=[node_child1, node_child2], props=None)
        self.assertIsInstance(node_parent.children, list) 

    def test_default_types(self):
        node1 = HTMLNode()
        self.assertIsInstance(node1, HTMLNode) 

    def test_repr_none(self):
        node1 = HTMLNode()
        self.assertEqual("HTMLNode(tag=None, value=None, children=None, props=None)", repr(node1))

    def test_partial_args(self):
        node1 = HTMLNode('p', 'my text')
        self.assertEqual(len(vars(node1)), 4)

    def test_props_to_html_none(self):
        node = HTMLNode(tag='a', value='Google', children=None)
        self.assertEqual('', node.props_to_html())

    #LeafNode Tests Below Here ---------------------

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

    #ParentNode Tests Below Here ---------------------

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