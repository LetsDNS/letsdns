from livereload import Server
from livereload import shell


def watch(s: Server, what: str) -> None:
    s.watch(f'_source/{what}', shell('make html'), delay=2)


def serve() -> None:
    s = Server()
    watch(s, '*.rst')
    watch(s, '_static/*')
    watch(s, '_templates/*')
    s.serve(root='_build/html')


if __name__ == '__main__':
    serve()
