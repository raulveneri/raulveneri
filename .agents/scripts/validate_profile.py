#!/usr/bin/env python3
"""Check profile content, public boundaries and self-contained artwork."""
from base64 import b64decode
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
SVG = '{http://www.w3.org/2000/svg}'
NAMES = ('profile-heading', 'search-optimization-toolkit', 'personal-website', 'development-stack')


class ProfileHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images, self.sources, self.links, self.pictures = [], [], [], []
        self.disclosures = []
        self.details = []
        self.picture = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'details':
            self.details.append('open' in attrs)
            self.disclosures.append('open' in attrs)
        if tag == 'picture':
            self.picture = []
        if tag == 'img':
            assert self.picture is not None, 'Every image needs responsive picture sources'
            assert self.details, 'Readers need a disclosure to hide artwork'
            self.images.append(attrs)
        if tag == 'source':
            self.sources.append(attrs)
            self.picture.append(attrs)
        if tag == 'a':
            self.links.append(attrs['href'])

    def handle_endtag(self, tag):
        if tag == 'details':
            self.details.pop()
        if tag == 'picture':
            self.pictures.append(self.picture)
            self.picture = None


def luminance(value):
    channels = [int(value[i:i+2], 16)/255 for i in (1, 3, 5)]
    linear = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in channels]
    return sum(v*w for v, w in zip(linear, (.2126, .7152, .0722)))


def contrast(a, b):
    lo, hi = sorted((luminance(a), luminance(b)))
    return (hi+.05)/(lo+.05)


def main():
    readme = (ROOT / 'README.md').read_text()
    parser = ProfileHTML()
    parser.feed(readme)
    assert not parser.details, 'Unclosed details'
    assert len(re.findall(r'^# ', readme, re.M)) == 1
    levels = [len(m[1]) for m in re.finditer(r'^(#+) ', readme, re.M)]
    assert all(b <= a+1 for a, b in zip(levels, levels[1:]))
    assert parser.disclosures == [True]*4+[False], 'Four collapsible animations and one closed static gallery'
    assert len(parser.images) == 8 and len(parser.pictures) == 8
    for index, (img, sources) in enumerate(zip(parser.images, parser.pictures)):
        assert img.get('alt', '').strip() and int(img['width']) > 0
        assert 'height' not in img, 'GitHub fixed HTML heights break picture art direction'
        if index < 4:
            assert [s['media'] for s in sources] == ['(prefers-reduced-motion: reduce) and (max-width: 1023px)', '(prefers-reduced-motion: reduce)', '(max-width: 1023px)']
            assert all('--static.svg' in s['srcset'] for s in sources[:2])
        else:
            assert '--static.svg' in img['src']
    paths = {img['src'] for img in parser.images} | {s['srcset'] for s in parser.sources}
    expected = {f'assets/raulveneri-{name}{mobile}{static}.svg' for name in NAMES for mobile in ('', '--mobile') for static in ('', '--static')}
    assert paths == expected == {str(p.relative_to(ROOT)) for p in (ROOT/'assets').glob('*.svg')}
    for relative in sorted(paths):
        path = ROOT / relative
        source = path.read_text()
        root = ET.fromstring(source)
        static = relative.endswith('--static.svg')
        assert root.get('viewBox') and int(root.get('width')) > 0 and int(root.get('height')) > 0
        assert root.get('role') == 'img'
        ids = [e.get('id') for e in root.iter() if e.get('id')]
        assert len(ids) == len(set(ids)) and all(i.startswith('raulveneri-') for i in ids)
        assert all(i in ids for i in root.get('aria-labelledby', '').split())
        assert root.find(SVG+'title') is not None and root.find(SVG+'desc') is not None
        assert 'prefers-reduced-motion: reduce' in source and 'animation: none !important' in source
        assert ('infinite' not in source) if static else ('prefers-reduced-motion: no-preference' in source)
        assert not re.search(r'(?:href=|url\()[\"\']?https?://', source)
        assert not any(word in source for word in ('linearGradient', '<pattern', 'circuit_trace'))
        assert path.stat().st_size < (500_000 if 'personal-website' in relative else 15_000)
        for element in root.iter():
            assert element.tag not in {SVG+'script', SVG+'foreignObject'}
            assert not any(k.startswith('on') for k in element.attrib)
            if element.tag == SVG+'image':
                assert 'personal-website' in relative
                value = element.get('href', '')
                assert value.startswith('data:image/png;base64,')
                data = b64decode(value.split(',', 1)[1], validate=True)
                assert data.startswith(b'\x89PNG\r\n\x1a\n')
                capture = 'mobile' if '--mobile' in relative else 'desktop'
                assert data == (ROOT/f'assets/sources/raulveneri-guide-{capture}.png').read_bytes()
    assert not any(ch in readme for ch in ('\u2014', '\u2013'))
    assert not re.search(r'sin humo|sin postureo|revoluciona|increíble|asombroso|vosotros|laboratorio|arreglaba móviles', readme, re.I)
    assert 'Mi herramienta de SEO. La uso en mi día a día y la voy actualizando.' in readme
    links = set(parser.links + re.findall(r'\]\((https?://[^)]+)\)', readme))
    for link in links:
        assert link.startswith(('https://www.raulveneri.com/', 'https://github.com/raulveneri')), link
        if link.startswith('https://github.com/raulveneri/'):
            assert link.split('/')[4].split('#')[0] == 'seo-kit', 'Unexpected public repository'
    pairs = [('#242321', '#f5f2ec'), ('#615c55', '#f5f2ec'), ('#ad3d28', '#f5f2ec'), ('#f1f5f9', '#1d2838')]
    minimum = min(contrast(f, b) for f, b in pairs)
    assert minimum >= 4.5
    captures = json.loads((ROOT/'assets/sources/capture.json').read_text())
    assert len(captures) == 2 and all(c['url'] == 'https://www.raulveneri.com/guias/google-analytics-mcp/' for c in captures)
    total = sum((ROOT/p).stat().st_size for p in paths)
    assert total < 2_500_000
    print(f'PASS: 16 SVGs, 8 image embeds, responsive reduced-motion sources, 4 closable animations and static gallery')
    print(f'PASS: {total:,} SVG bytes, embedded public captures, no remote dependencies, minimum checked text contrast {minimum:.2f}:1')
    print(f'PASS: public links, accessible names, intrinsic ratios, headings and Voice Kit copy floor')
    print('Browser motion, rendering and link responses require separate verification.')


if __name__ == '__main__':
    main()
