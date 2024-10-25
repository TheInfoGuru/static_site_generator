import unittest

from textnode import *
from node_workers import *


class TestNodeConversion(unittest.TestCase):
    # Base tests for Text Node Here ----------------
    def test_eq(self):
        node = TextNode("This is a **text** node", TextType.TEXT)
        node2 = TextNode("This **is** a text **node** with two", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], '**', TextType.BOLD)
        self.assertEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" node", TextType.TEXT),
                TextNode("This ", TextType.TEXT),
                TextNode("is", TextType.BOLD),
                TextNode(" a text ", TextType.TEXT),
                TextNode("node", TextType.BOLD),
                TextNode(" with two", TextType.TEXT)
            ],
            new_nodes
        )

    def test_error(self):
        with self.assertRaises(ValueError):
            node = TextNode("This is a **text node", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)

    def test_no_delim_foudn(self):
        node = TextNode("This is a **text** node", TextType.TEXT)
        node2 = TextNode("This **is** a text **node** with two", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], '`', TextType.CODE)
        self.assertEqual([node, node2], new_nodes)

    def test_double(self):
        node = TextNode("This is a **text** node with a `code block` added", TextType.TEXT)
        new_nodes = split_nodes_delimiter(split_nodes_delimiter([node], '**', TextType.BOLD),'`', TextType.CODE)
        self.assertEqual(
            [
                TextNode('This is a ', TextType.TEXT), 
                TextNode('text', TextType.BOLD), 
                TextNode(' node with a ', TextType.TEXT), 
                TextNode('code block', TextType.CODE), 
                TextNode(' added', TextType.TEXT)
            ],
            new_nodes
        )

    def test_multiword(self):
        node = TextNode("This is a **longer bolded text block** node.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(
            [
                TextNode('This is a ', TextType.TEXT), 
                TextNode('longer bolded text block', TextType.BOLD), 
                TextNode(' node.', TextType.TEXT)
            ],
            new_nodes
        )
    
    def test_multi_images(self):
        image_list = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(
            [
                ('rick roll', 'https://i.imgur.com/aKaOqIh.gif'),
                ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg'),
            ],
            image_list
        )
        
    def test_multi_links(self):
        link_list = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(
            [
                ('to boot dev', 'https://www.boot.dev'),
                ('to youtube', 'https://www.youtube.com/@bootdotdev'),
            ],
            link_list
        )

    def test_no_links(self):
        link_list = extract_markdown_links("This is text with a link to here and to youtube")
        self.assertEqual([], link_list)

    def test_link_node_conversion(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT, None),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT, None),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            new_nodes
        )

    def test_link_node_conversion_no_links(self):
        node = TextNode(
            "This is text with no links to find.",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is text with no links to find.", TextType.TEXT, None)
            ],
            new_nodes
        )

    def test_link_node_conversion_only_link(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes
        )

    def test_image_node_conversion_only_image(self):
        node = TextNode(
            "![to boot dev](https://www.boot.dev/pic.jpg)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev/pic.jpg"),
            ],
            new_nodes
        )

    def test_image_node_conversion_no_links(self):
        node = TextNode(
            "This is text with no images to find.",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("This is text with no images to find.", TextType.TEXT, None)
            ],
            new_nodes
        )

    def test_image_node_conversion(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev/pic.jpg) and ![to youtube](https://www.youtube.com/@bootdotdev/mypic.png5)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])
        
        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT, None),
                TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev/pic.jpg"),
                TextNode(" and ", TextType.TEXT, None),
                TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev/mypic.png5")
            ],
            new_nodes
        )


if __name__ == "__main__":
    unittest.main()