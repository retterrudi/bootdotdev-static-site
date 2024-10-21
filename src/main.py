from handle_files import move_files
from handle_files import generate_page


def main():
    move_files('static/', 'public/')
    generate_page('content/index.md', 'template.html', 'public/index.html')

main()