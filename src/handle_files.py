import os
import shutil

from parse_markdown import markdown_to_html_node, extract_title


def move_files(source: str, destination: str) -> None:
    if not os.path.isdir(source):
        raise ValueError(f'source has to be a directory: {source}')
    # if not os.path.isdir(destination):
    #     raise ValueError(f'destination has to be a directory: {destination}')

    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.mkdir(destination)

    source_list = os.listdir(source)
    for item in source_list:
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        print(source_path)
        if os.path.isdir(source_path):
            move_files(source_path, destination_path)
        else:
            shutil.copy(source_path, destination_path)

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f'Generating page from "{from_path}" to "{dest_path}" using "{template_path}"')

    # markdown = ''
    with open(from_path) as file:
        markdown = file.read()

    # template_text = ''
    with open(template_path) as file:
        template_text = file.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    site = template_text.replace('{{ Title }}', title).replace('{{ Content }}', content)

    if not os.path.exists(dest_path):
        dir_path = os.path.dirname(dest_path)
        os.makedirs(dir_path, exist_ok=True)

    with open(dest_path, 'w+') as file:
        file.write(site)
