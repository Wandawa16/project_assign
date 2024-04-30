import os
import shutil
import markdown
from jinja2 import Environment, FileSystemLoader

# Configuration
MARKDOWN_DIR = "content"
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "output"

# Load Jinja2 environment
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# Function to create output directory if not exists
def create_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

# Function to convert Markdown to HTML
def convert_markdown_to_html(content):
    return markdown.markdown(content)

# Function to generate HTML from template
def generate_html(template, **kwargs):
    template = env.get_template(template)
    return template.render(**kwargs)

# Function to read Markdown file
def read_markdown_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# Function to write HTML file
def write_html_file(filename, content):
    with open(os.path.join(OUTPUT_DIR, filename), 'w') as file:
        file.write(content)

# Function to generate website
def generate_website():
    create_output_dir()

    # Load content pages
    pages = {}
    for file in os.listdir(MARKDOWN_DIR):
        if file.endswith(".md"):
            name = os.path.splitext(file)[0]
            content = read_markdown_file(os.path.join(MARKDOWN_DIR, file))
            html_content = convert_markdown_to_html(content)
            pages[name] = html_content

    # Generate homepage with all pages
    homepage = generate_html("homepage.html", pages=pages)
    write_html_file("index.html", homepage)

    # Generate articles and supporting pages
    for name, content in pages.items():
        page = generate_html("article.html", title=name, content=content, pages=pages)
        write_html_file(f"{name}.html", page)

    # Copy styles.css to the output directory
    shutil.copyfile(os.path.join(TEMPLATE_DIR, "styles.css"), os.path.join(OUTPUT_DIR, "styles.css"))

# Generate the website
generate_website()
