import unittest

from src.htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_LeafNode_valueCanNotBeNone(self):
        node = LeafNode()
        with self.assertRaises(ValueError):
            _ = node.to_html()

    def test_LeafNode_toHTML(self):
        node = LeafNode('a', 'Click me!', {'href': 'https://www.google.com'})
        self.assertEqual('<a href="https://www.google.com">Click me!</a>', node.to_html())



if __name__ == '__main__':
    unittest.main()
