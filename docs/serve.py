from livereload import Server
from livereload import shell


def watch(what: str) -> None:
    server.watch(f'_source/{what}', shell('make html'), delay=2)


if __name__ == '__main__':
    server = Server()
    watch('*.md')
    watch('*.py')
    watch('*.rst')
    watch('_static/*')
    watch('_templates/*')
    server.serve(root='_build/html')
