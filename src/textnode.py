from enum import Enum
from htmlnode import *

class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if isinstance(other, TextNode):
            return vars(self) == vars(other)
        return False
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'
    
    def to_html_node(self):
        match self.text_type:
            case TextType.TEXT:
                return LeafNode(value=self.text)
            case TextType.BOLD:
                return LeafNode(tag='b', value=self.text)
            case TextType.ITALIC:
                return LeafNode(tag='i', value=self.text)
            case TextType.CODE:
                return LeafNode(tag='code', value=self.text)
            case TextType.LINK:
                return LeafNode(tag='a', value=self.text, props={'href': self.url})
            case TextType.IMAGE:
                return LeafNode(tag='img', value='', props={'src': self.url, 'alt': self.text})
            case _:
                raise ValueError('Text node must be predefined type.')