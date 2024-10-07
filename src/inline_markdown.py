import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)",text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)",text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            current_text = node.text
            for image in images:
                next_text = current_text.split(f"![{image[0]}]({image[1]})")
                if next_text[0] != "":
                    new_nodes.append(TextNode(next_text[0],text_type_text))
                current_text = next_text[1]
                new_nodes.append(TextNode(image[0],text_type_image,image[1]))
            if current_text != "":
                new_nodes.append(TextNode(current_text,text_type_text))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            current_text = node.text
            for link in links:
                next_text = current_text.split(f"[{link[0]}]({link[1]})")
                if next_text[0] != "":
                    new_nodes.append(TextNode(next_text[0],text_type_text))
                current_text = next_text[1]
                new_nodes.append(TextNode(link[0],text_type_link,link[1]))
            if current_text != "":
                new_nodes.append(TextNode(current_text,text_type_text))
    return new_nodes

def text_to_textnodes(text):
    nodes = split_nodes_delimiter([TextNode(text, text_type_text)], '`', text_type_code)
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes