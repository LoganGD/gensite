import os
import shutil
from block import markdown_to_html_node

def get():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    os.mkdir("./public")
    os.mkdir("./public/images")
    shutil.copy("./static/index.css","./public")
    shutil.copy("./static/images/rivendell.png","./public/images")

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line[0] == "#" and line[1] == " ":
            return "".join(line[2:])
    raise Exception("No title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    with open(dest_path, "w") as f:
        f.write(template.replace("{{ Title }}", extract_title(markdown)).replace("{{ Content }}", markdown_to_html_node(markdown).to_html()))

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(os.listdir(dir_path_content))
    for element in os.listdir(dir_path_content):
        if "".join(element[-3:])!=".md":
            os.mkdir(dest_dir_path+'/'+element)
            generate_pages_recursive(dir_path_content+'/'+element,template_path,dest_dir_path+'/'+element)
        else: 
            generate_page(dir_path_content+'/'+element,template_path,dest_dir_path+'/'+"".join(element[:-3])+".html")

def main():
    get()
    generate_pages_recursive("content","template.html","public")
    

if __name__ == "__main__":
    main()