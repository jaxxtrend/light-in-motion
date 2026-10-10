"""Build the Claude artifact page from the standalone page.

index.html is the working page (opens on its own over http://localhost).
light-in-motion.html is what gets published as an artifact: the artifact
viewer wraps the file in its own <html>/<head>/<body>, so the document
wrapper, charset/viewport metas and the old og:url are removed, and the title
becomes a plain name.

Usage: python build.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'index.html'
TARGET = HERE / 'light-in-motion.html'

STRIP = [
    '<meta charset="utf-8">\n',
    '<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover">\n',
    '    <meta property="og:url" content="https://artifact.ardor.build/artifact-api/published/fffe22b2-31c79ed9/index.html" />\n',
    '  </head>\n<body>\n',
    '</body>\n</html>',
]


def build() -> None:
    lines = SOURCE.read_text(encoding='utf-8').split('\n')
    if not (lines[0].lower().startswith('<!doctype') and lines[1].startswith('<html') and lines[2] == '<head>'):
        raise SystemExit('index.html does not start with the expected <!doctype>/<html>/<head> lines')
    page = '\n'.join(lines[3:])
    for fragment in STRIP:
        if page.count(fragment) != 1:
            raise SystemExit(f'expected exactly one {fragment!r} in index.html')
        page = page.replace(fragment, '', 1)
    page = page.replace('<title>Film — Light in Motion</title>', '<title>Light in Motion</title>', 1)
    TARGET.write_text(page, encoding='utf-8')
    print(f'{TARGET.name}: {len(page):,} characters')


if __name__ == '__main__':
    build()
