import unittest

from src.textnode import TextNode, TextType, text_node_to_html


class TextTextNode(unittest.TestCase):
    def test_TextNode_eq(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.BOLD)
        self.assertEqual(node, node2)

    def test_TextNode_eqWithGivenUrl_areEqual(self):
        node = TextNode('This is a text node', TextType.BOLD, 'https://boot.dev')
        node2 = TextNode('This is a text node', TextType.BOLD, 'https://boot.dev')
        self.assertEqual(node, node2)

    def test_TextNode_eqWithDifferingProperties_areNotEqual(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.ITALIC)
        self.assertNotEqual(node, node2)


class TestTextNodeToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode('This is a text node', TextType.TEXT)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, 'This is a text node')

    def test_image(self):
        node = TextNode('This is an image', TextType.IMAGE, 'https://www.boot.dev')
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props, {'src': 'https://www.boot.dev', 'alt': 'This is an image'})

    def test_bold(self):
        node = TextNode('This is bold', TextType.BOLD)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, 'This is bold')

if __name__ == '__main__':
    unittest.main()
