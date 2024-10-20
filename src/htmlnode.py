class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag # <p>, <a>, <h1>, etc
        self.value = value #text in between tags
        self.children = children #list of children nodes as HTMLNode objects
        self.props = props #dict of key/value pairs of attributes of the tag, {"href": "https://www.google.com"}

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ''
        return ' '.join([f' {key}="{value}"' for key,value in self.props.items()])
    
    def __repr__(self):
        return f'HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})'
    

        