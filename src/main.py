from handle_files import move_files
from handle_files import generate_page_recursive


def main():
    move_files('static/', 'public/')
    generate_page_recursive('content/', 'template.html', 'public/')

main()