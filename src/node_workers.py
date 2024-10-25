import re
import itertools
from htmlnode import *
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_node_text = node.text.split(delimiter)

        if len(split_node_text) % 2 == 0:
            raise ValueError('Invalid Markdown syntax detected. Please ensure all markdown has beginning and ending marks.')
        
        for index, text in enumerate(split_node_text):
            if not text:
                continue
            new_text_type = text_type if index % 2 == 1 else TextType.TEXT
            new_nodes.append(TextNode(text=text, text_type=new_text_type))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\]]+)\]\((https?:\/\/[^\s]+\.[a-zA-Z0-9]+)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[([^\]]+)\]\((https?:\/\/[^\s\)]+)\)", text)

def split_nodes_image(old_nodes):
    new_image_nodes = []
    old_image_nodes = []
    old_text_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_image_nodes.append(node)
            continue
        
        if not node.text:
            continue
        
        image_tuples = extract_markdown_images(node.text)
    
        if not image_tuples:
            new_image_nodes.append(node)
            continue

        for alt_txt, image_url in image_tuples:
            old_image_nodes.append(TextNode(text=alt_txt, text_type=TextType.IMAGE, url=image_url))

        split_node_text = re.split(r"![^\)]+\)", node.text)

        for text in split_node_text:
            if not text:
                continue
            old_text_nodes.append(TextNode(text=text, text_type=TextType.TEXT))

        new_image_nodes = list(
            filter(
                None, 
                itertools.chain.from_iterable(
                    itertools.zip_longest(
                        old_text_nodes, old_image_nodes, fillvalue=None
                        )
                    )
                )
            )
    
    return new_image_nodes

def split_nodes_link(old_nodes):
    new_link_nodes = []
    old_link_nodes = []
    old_text_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_link_nodes.append(node)
            continue
        
        if not node.text:
            continue
        
        link_tuples = extract_markdown_links(node.text)
    
        if not link_tuples:
            new_link_nodes.append(node)
            continue

        for link_txt, link_url in link_tuples:
            old_link_nodes.append(TextNode(text=link_txt, text_type=TextType.LINK, url=link_url))

        split_node_text = re.split(r"\[[^\)]+\)", node.text)

        for text in split_node_text:
            if not text:
                continue
            old_text_nodes.append(TextNode(text=text, text_type=TextType.TEXT))

        new_link_nodes = list(
            filter(
                None, 
                itertools.chain.from_iterable(
                    itertools.zip_longest(
                        old_text_nodes, old_link_nodes, fillvalue=None
                        )
                    )
                )
            )
    
    return new_link_nodes

# print(split_nodes_link([TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)]))