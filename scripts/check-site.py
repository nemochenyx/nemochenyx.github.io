"""Check the four public pages, PDF, canonical URLs, and internal links."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re

root = Path(__file__).resolve().parents[1]
public = root / 'public'
expected = ['index.html', 'cv/index.html', 'publication/index.html', 'working-paper/index.html', '404.html']
errors = []

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.canonical = None
        self.h1 = 0
        self.active = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'h1': self.h1 += 1
        if tag == 'a' and a.get('aria-current') == 'page': self.active += 1
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical = a.get('href')
        for key in ('href', 'src', 'data'):
            if a.get(key): self.links.append(a[key])

for name in expected:
    path = public / name
    if not path.is_file():
        errors.append(f'Missing page: {name}')
        continue
    p = Page()
    p.feed(path.read_text())
    if p.h1 != 1: errors.append(f'{name}: expected one main heading')
    if name != '404.html' and p.active != 1: errors.append(f'{name}: expected one active navigation link')
    if not p.canonical or not p.canonical.startswith('https://'): errors.append(f'{name}: canonical URL must use HTTPS')
    for link in p.links:
        u = urlsplit(link)
        if u.scheme or u.netloc or not u.path or u.path.startswith('data:'): continue
        target = public / unquote(u.path.lstrip('/')) if u.path.startswith('/') else path.parent / unquote(u.path)
        if target.is_dir(): target = target / 'index.html'
        if not target.is_file(): errors.append(f'{name}: broken local link {link}')

pdf = public / 'files/cv/YC_CV.pdf'
if not pdf.is_file() or not pdf.read_bytes().startswith(b'%PDF-'): errors.append('CV is missing or is not a PDF')
for name in ('sitemap.xml', 'robots.txt', 'llms.txt'):
    if not (public / name).is_file(): errors.append(f'Missing {name}')
if errors:
    raise SystemExit('\n'.join(errors))
print('Verified: four pages, navigation, HTTPS canonical URLs, local links, CV PDF, and crawler files.')

