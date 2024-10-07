from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, text_type_text

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
    all_blocks = markdown.split("\n\n")
    real_blocks = []
    for block in all_blocks:
        if block != "":
            real_blocks.append(block.strip("\n "))
    return real_blocks

def block_to_block_type(block):
    heading = len(block)-len(block.lstrip("#"))
    if 0 < heading <= 6 and block.lstrip("#")[0] == " ":
        return (block_type_heading, heading)
    if "".join(block[:3]) == "```" and "".join(block[-3:]) == "```":
        return (block_type_code,None)
    lines = block.split("\n")
    flag = 1
    for line in lines:
        if line[0] != ">":
            flag = 0
    if flag:
        return (block_type_quote,None)
    flag = 1
    for line in lines:
        if (line[0] != "-" and line[0] != "*") or line[1] != " ":
            flag = 0
    if flag:
        return (block_type_unordered_list,None)
    flag = 1
    for i in range(len(lines)):
        if "".join(lines[i][0:3]) != f"{str(i+1)}. ":
            flag = 0
    if flag:
        return (block_type_ordered_list,None)
    return (block_type_paragraph,None)

def text_to_children(text):
    return list(map(text_node_to_html_node,text_to_textnodes(text)))

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type, heading = block_to_block_type(block)
        if block_type == block_type_heading:
            nodes.append(ParentNode(f"h{heading}",text_to_children("".join(block[heading+1:]))))
        elif block_type == block_type_code:
            nodes.append(ParentNode("code",text_to_children("".join(block[3:-3]))))
        elif block_type == block_type_quote:
            nodes.append(ParentNode("blockquote",text_to_children("".join(list(map(lambda line:"".join(line[1:]),block.split("\n")))))))
        elif block_type == block_type_unordered_list:
            nodes.append(ParentNode("ul",list(map(lambda line:ParentNode("li",text_to_children("".join(line[2:]))),block.split("\n")))))
        elif block_type == block_type_ordered_list:
            nodes.append(ParentNode("ol",list(map(lambda line:ParentNode("li",text_to_children("".join(line[2:]))),block.split("\n")))))
        else:
            nodes.append(ParentNode("p",list(map(text_node_to_html_node,text_to_textnodes(block)))))
    return ParentNode("div",nodes)