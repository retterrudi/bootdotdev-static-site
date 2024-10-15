from typing import List, Optional


class HTMLNode:
    def __init__(
            self,
            tag: Optional[str] = None,
            value: Optional[str] = None,
            children: Optional[List['HTMLNode']] = None,
            props: Optional[dict] = None
    ):
       self.tag = tag
       self.value = value
       self.children = children
       self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        string = ''
        if self.props is not None:
            for key, value in self.props.items():
                string += f' {key}="{value}"'
        return string

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'


class LeafNode(HTMLNode):
    def __init__(
            self,
            tag: Optional[str] = None,
            value: Optional[str] = None,
            props: Optional[dict] = None
    ):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError('LeafNodes must have a value')
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(
            self,
            tag: Optional[str] = None,
            children: Optional[List['HTMLNode']] = None,
            props: Optional[dict] = None
    ):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.children is None:
            raise ValueError('A ParentNode must have children.')
        if self.tag is None:
            raise ValueError('A ParentNode must have a tag.')

        string = f'<{self.tag}>'
        for child in self.children:
            string += child.to_html()

        string += f'</{self.tag}>'

        return string
