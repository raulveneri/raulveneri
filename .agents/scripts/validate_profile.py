#!/usr/bin/env python3
"""Check profile assets, public links, structure and the Voice Kit copy floor."""
from html.parser import HTMLParser
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
SVG = "{http://www.w3.org/2000/svg}"


class ProfileHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.sources = []
        self.links = []
        self.in_picture = False
        self.responsive_images = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "picture":
            self.in_picture = True
        if tag == "img":
            self.images.append(attrs)
            if self.in_picture:
                self.responsive_images.add(attrs["src"])
        if tag == "source":
            self.sources.append(attrs)
        if tag == "a":
            self.links.append(attrs["href"])

    def handle_endtag(self, tag):
        if tag == "picture":
            self.in_picture = False


def luminance(hex_color):
    rgb = [int(hex_color[i:i+2], 16)/255 for i in (1, 3, 5)]
    linear = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in rgb]
    return sum(v*w for v, w in zip(linear, (.2126, .7152, .0722)))


def contrast(a, b):
    values = sorted((luminance(a), luminance(b)))
    return (values[1]+.05)/(values[0]+.05)


def main():
    readme = (ROOT / "README.md").read_text()
    parser = ProfileHTML()
    parser.feed(readme)
    assert len(re.findall(r"^# ", readme, re.M)) == 1, "Expected one main heading"
    levels = [len(m[1]) for m in re.finditer(r"^(#+) ", readme, re.M)]
    assert all(b <= a+1 for a, b in zip(levels, levels[1:])), "Skipped heading level"
    for img in parser.images:
        assert img.get("alt", "").strip(), "Missing alt text"
        assert int(img["width"]) > 0, "Missing image width"
        if img["src"] in parser.responsive_images:
            # GitHub leaves height fixed inside picture, even when width shrinks.
            # Use the selected SVG's intrinsic ratio for art-directed sources.
            assert "height" not in img, "Fixed height breaks GitHub art direction"
        else:
            assert int(img["height"]) > 0, "Missing fixed-card dimensions"
    sources = [img["src"] for img in parser.images] + [s["srcset"] for s in parser.sources]
    files = sorted((ROOT / "assets").glob("*.svg"))
    assert {str(p.relative_to(ROOT)) for p in files} == set(sources), "Unused or missing artwork"
    assert len(files) == 8
    for path in files:
        source = path.read_text()
        root = ET.fromstring(source)
        assert root.get("viewBox") and int(root.get("width")) > 0 and int(root.get("height")) > 0, "Missing intrinsic SVG ratio"
        assert root.get("role") == "img"
        ids = [e.get("id") for e in root.iter() if e.get("id")]
        assert len(ids) == len(set(ids)), f"Duplicate ID in {path.name}"
        assert all(value.startswith("raulveneri-") for value in ids)
        assert all(value in ids for value in root.get("aria-labelledby", "").split())
        assert root.find(SVG+"title") is not None and root.find(SVG+"desc") is not None
        assert "prefers-reduced-motion: reduce" in source and "animation: none !important" in source
        assert "infinite" not in source
        assert path.stat().st_size < 12000
        for element in root.iter():
            assert element.tag not in {SVG+"script", SVG+"foreignObject", SVG+"image"}
            assert not any(k.startswith("on") for k in element.attrib)
        assert not re.search(r"(?:href=|url\()[\"']?https?://", source), "Remote asset dependency"
    assert sum(p.stat().st_size for p in files) < 45000, "Artwork budget exceeded"
    assert not any(ch in readme for ch in ("\u2014", "\u2013")), "Voice Kit dash prohibition"
    assert not re.search(r"sin humo|sin postureo|revoluciona|increíble|asombroso|vosotros", readme, re.I)
    links = set(parser.links + re.findall(r"\]\((https?://[^)]+)\)", readme))
    for link in links:
        assert link.startswith(("https://www.raulveneri.com/", "https://www.roboticzlab.com/", "https://github.com/raulveneri")), link
        if link.startswith("https://github.com/raulveneri/"):
            assert link.split("/")[4] == "seo-kit", "Unexpected repository linked publicly"
    foregrounds = ["#f1f5f9", "#b7c8d9", "#72ede2", "#ffd28a", "#83baff", "#f8a8d3", "#f3df75", "#ffbc79"]
    backgrounds = ["#101e30", "#080f1b", "#122338", "#102034"]
    minimum = min(contrast(f, b) for f in foregrounds for b in backgrounds)
    assert minimum >= 4.5, f"Text contrast {minimum:.2f}:1"
    print(f"PASS: {len(files)} SVGs, {len(parser.images)} image embeds, {len(parser.sources)} mobile sources, {len(links)} public link targets")
    print(f"PASS: {sum(p.stat().st_size for p in files):,} artwork bytes; minimum checked text contrast {minimum:.2f}:1")
    print("PASS: SVG safety, accessible names, intrinsic ratios, finite motion, local assets, headings and Voice Kit copy floor")
    print("External link responses and browser rendering require separate verification.")


if __name__ == "__main__":
    main()
