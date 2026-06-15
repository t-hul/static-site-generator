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
