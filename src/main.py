from textnode import TextNode,TextType

def main():
    test_textnode = TextNode('This is my text.', TextType.BOLD, 'https://myurl.com/')
    print(test_textnode)


main()