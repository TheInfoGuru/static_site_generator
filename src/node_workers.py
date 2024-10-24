import re
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
            new_text_type = text_type if index % 2 == 1 else TextType.TEXT
            new_nodes.append(TextNode(text=text, text_type=new_text_type))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([\w ]+)\]\((http[s]?:\/\/[^\s\)]+\.{1}[a-zA-Z0-9]+)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[([\w ]+)\]\((http[s]?:\/\/[^\s\)]+)\)", text)