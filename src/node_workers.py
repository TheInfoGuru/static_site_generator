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
    return re.findall(r"\!\[([^\]]+)\]\((https?:\/\/[^\s\)]+)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[([^\]]+)\]\((https?:\/\/[^\s\)]+)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        image_nodes = []
        if not node.text:
            continue

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        image_tuples = extract_markdown_images(node.text)
    
        if not image_tuples:
            new_nodes.append(node)
            continue

        for alt_txt, image_url in image_tuples:
            image_nodes.append(TextNode(text=alt_txt, text_type=TextType.IMAGE, url=image_url))

        text_to_split = node.text
        
        for image_node in image_nodes:
            split_text = re.split(r"\!\[[^\)]+\)", text_to_split, 1)
            new_nodes.extend([TextNode(split_text[0], TextType.TEXT), image_node] if split_text[0] else [image_node])
            text_to_split = split_text[1]

        if text_to_split:
            new_nodes.append(TextNode(text_to_split, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        link_nodes = []

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        if not node.text:
            continue
        
        link_tuples = extract_markdown_links(node.text)
    
        if not link_tuples:
            new_nodes.append(node)
            continue

        for link_txt, link_url in link_tuples:
            link_nodes.append(TextNode(text=link_txt, text_type=TextType.LINK, url=link_url))

        text_to_split = node.text
        for link_node in link_nodes:
            split_text = re.split(r"(?<!\!)\[[^\)]+\)", text_to_split, 1)
            new_nodes.extend([TextNode(split_text[0], TextType.TEXT), link_node] if split_text[0] else [link_node])                
            text_to_split = split_text[1]
        
        if text_to_split:
            new_nodes.append(TextNode(text_to_split, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    markdown_delim_options = [
        ('**', TextType.BOLD), 
        ('*', TextType.ITALIC), 
        ('`', TextType.CODE)
    ]

    text_nodes = [TextNode(text=text, text_type=TextType.TEXT)]
    
    for delim, type in markdown_delim_options:
        text_nodes = split_nodes_delimiter(text_nodes, delim, type)
    
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    
    return text_nodes

