import os

from .block_markdown import extract_title, markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    template = ""
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html_page = template.replace(r"{{ Title }}", title).replace(
        r"{{ Content }}", html_string
    )

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(html_page)


def generate_pages_recursive(
    content_dir_path: str, template_path: str, dest_dir_path: str
):
    content_list = os.listdir(content_dir_path)
    for item in content_list:
        item_path = os.path.join(content_dir_path, item)
        if os.path.isfile(item_path) and item.endswith(".md"):
            dest_file_name = item[:-3] + ".html"
            generate_page(
                item_path, template_path, os.path.join(dest_dir_path, dest_file_name)
            )
        elif os.path.isdir(item_path):
            generate_pages_recursive(
                item_path, template_path, os.path.join(dest_dir_path, item)
            )
