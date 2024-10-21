import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    # Base tests for Text Node Here ----------------
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, None)
        node2 = TextNode("This is a text node", TextType.ITALIC, None)
        self.assertEqual(node, node2)

    def test_kw_args_eq(self):
        node = TextNode(text="This is a text node", text_type=TextType.BOLD, url='https://url.com/')
        node2 = TextNode(text="This is a text node", text_type=TextType.BOLD, url='https://url.com/')
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.BOLD, 'https://thisurl.com/')
        self.assertNotEqual(node, node2)

    # Base tests for Text Node types to html Here ----------------
    def test_single_text_node(self):
        node1 = TextNode("This is a text node", TextType.TEXT).to_html_node()
        self.assertEqual("LeafNode(tag=None, value=This is a text node, props=None)", repr(node1))

    def test_is_leafnode(self):
        node1 = TextNode("This is a text node", TextType.BOLD).to_html_node()
        self.assertIsInstance(node1, LeafNode)

    def test_convert_textnode_to_full_html(self):
        node1 = TextNode("This is a text node", TextType.ITALIC).to_html_node().to_html()
        self.assertIsInstance(node1, str)
        self.assertEqual('<i>This is a text node</i>', node1)

    def test_values(self):
        node_text = TextNode("This is a text node", TextType.TEXT).to_html_node()
        node_bold = TextNode("This is a bold node", TextType.BOLD).to_html_node()
        node_italic = TextNode("This is an italic node", TextType.ITALIC).to_html_node()
        node_code = TextNode("This is a code node", TextType.CODE).to_html_node()
        node_link = TextNode("This is a link node", TextType.LINK, url='https://www.google.com/').to_html_node()
        node_image = TextNode("This is an image node", TextType.IMAGE, url='https://myimage.com/').to_html_node()
        self.assertTrue(node_text.tag in (None, ''))
        self.assertEqual('b', node_bold.tag)
        self.assertEqual('i', node_italic.tag)
        self.assertEqual('code', node_code.tag)
        self.assertEqual('a', node_link.tag)
        self.assertEqual('img', node_image.tag)


if __name__ == "__main__":
    unittest.main()