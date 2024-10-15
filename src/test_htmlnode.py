import unittest

from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_HTMLNode_propsToHTML(self):
        node = HTMLNode(props={'href': 'https://www.google.com', 'target': '_blank'})
        string = node.props_to_html()
        self.assertEqual(' href="https://www.google.com" target="_blank"', string)

    def test_HTMLNode_repr(self):
        node = HTMLNode('p', 'test text')
        self.assertEqual('HTMLNode(p, test text, None, None)', str(node))

    def test_HTMLNode_emptyState(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)


if __name__ == '__main__':
    unittest.main()
