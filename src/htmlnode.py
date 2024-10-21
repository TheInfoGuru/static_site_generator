class HTMLNode():
    def __init__(self, tag: str=None, value: str=None, children: list=None, props: dict=None):
        self.tag = tag # <p>, <a>, <h1>, etc
        self.value = value #text in between tags
        self.children = children #list of children nodes as HTMLNode objects
        self.props = props #dict of key/value pairs of attributes of the tag, {"href": "https://www.google.com"}

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ''
        return ''.join([f' {key}="{value}"' for key,value in self.props.items()])
    
    def __repr__(self):
        return f'HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})'
    

class LeafNode(HTMLNode):
    def __init__(self, tag: str=None, value: str=None, props: dict=None):
        super().__init__(tag=tag, value=value, props=props)
        if not self.value:
            raise ValueError('All leaf nodes must have a value')
        
    def to_html(self):
        if not self.tag:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>' 
    

class ParentNode(HTMLNode):
    def __init__(self, tag: str=None, children: list=None, props: dict=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError('Parent node must have tag')
        
        if not self.children:
            raise ValueError('Parent node must have children')
        
        children_html = ''.join(child.to_html() for child in self.children)
        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'