#!/usr/bin/env python3
"""Original SVG artwork for the profile. Python standard library only."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "assets"
INK, MUTED, CYAN, AMBER = "#f1f5f9", "#b7c8d9", "#72ede2", "#ffd28a"


def text(x, y, value, size=24, color=INK, weight=400, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{escape(value)}</text>'


def document(name, width, height, title, body, inset=1):
    prefix = "raulveneri-" + name.replace("-", "_")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="{prefix}_title {prefix}_description">
<title id="{prefix}_title">{escape(title)}</title>
<desc id="{prefix}_description">{escape(title)} Ilustración original. Las animaciones terminan antes de cinco segundos.</desc>
<defs>
 <linearGradient id="{prefix}_background" x2="1" y2="1"><stop stop-color="#101e30"/><stop offset="1" stop-color="#080f1b"/></linearGradient>
 <pattern id="{prefix}_grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#23364d" stroke-opacity=".45"/></pattern>
</defs>
<style>
 text {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; }}
 .raulveneri-circuit_trace {{ stroke-dasharray: 12 16; animation: raulveneri-flow 4.6s ease-out 1; }}
 .raulveneri-panel_reveal {{ animation: raulveneri-reveal 1s ease-out 1 backwards; }}
 @keyframes raulveneri-flow {{ from {{stroke-dashoffset: 224;}} to {{stroke-dashoffset: 0;}} }}
 @keyframes raulveneri-reveal {{ from {{transform: translateY(7px);}} to {{transform: translateY(0);}} }}
 @media (prefers-reduced-motion: reduce) {{ *, *::before, *::after {{ animation: none !important; transition: none !important; }} }}
</style>
<rect x="{inset}" y="{inset}" width="{width-2*inset}" height="{height-2*inset}" rx="24" fill="url(#{prefix}_background)" stroke="#344b65"/>
<rect x="{inset+1}" y="{inset+1}" width="{width-2*inset-2}" height="{height-2*inset-2}" rx="23" fill="url(#{prefix}_grid)"/>
{body}
</svg>
'''
    (ASSETS / f"raulveneri-{name}.svg").write_text(svg, encoding="utf-8")


def circuit(cx, cy, scale=1):
    return f'''<g transform="translate({cx} {cy}) scale({scale})" fill="none" stroke="#58748f" stroke-width="2">
 <circle r="113" stroke-dasharray="3 12"/><circle r="83" stroke="#344b65"/>
 <path d="M-150-58H-88L-48-18M150 58H88L48 18M-150 58H-88L-48 18M150-58H88L48-18M0-145V-49M0 145V49"/>
 <path class="raulveneri-circuit_trace" d="M-150-58H-88L-48-18M150 58H88L48 18M0-145V-49" stroke="{CYAN}" stroke-width="3"/>
 <path d="M-48-28L0-56 48-28V28L0 56-48 28Z" fill="#102b38" stroke="{CYAN}"/>
 <path d="M-24-10L-37 0-24 10M24-10L37 0 24 10M9-21L-9 21" stroke="{CYAN}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
 <g fill="#111f30" stroke="{CYAN}"><circle cx="-150" cy="-58" r="7"/><circle cx="150" cy="58" r="7"/><circle cy="-145" r="7"/></g>
 <g fill="#111f30" stroke="{AMBER}"><circle cx="150" cy="-58" r="7"/><circle cx="-150" cy="58" r="7"/><circle cy="145" r="7"/></g>
 </g>'''


def hero(mobile=False):
    width, height = (640, 580) if mobile else (1200, 400)
    body = text(40 if mobile else 56, 82 if mobile else 112, "Marketing, código", 52 if mobile else 72, weight=700)
    body += text(40 if mobile else 56, 148 if mobile else 198, "y agentes IA.", 52 if mobile else 72, CYAN, 700)
    body += text(40 if mobile else 60, 205 if mobile else 260, "Mi laboratorio digital.", 29 if mobile else 28, MUTED)
    body += circuit(320 if mobile else 967, 387 if mobile else 192, .81 if mobile else .91)
    body += text(40 if mobile else 60, 544 if mobile else 350, "Construyo. Compruebo. Itero.", 27 if mobile else 24, AMBER, 500)
    document("digital-laboratory" + ("--mobile" if mobile else ""), width, height, "Marketing, código y agentes IA. Mi laboratorio digital.", body)


def toolkit(mobile=False):
    width, height = (640, 650) if mobile else (1200, 420)
    body = text(40 if mobile else 56, 93 if mobile else 104, "SEO Kit", 66, weight=700)
    body += text(40 if mobile else 58, 145 if mobile else 162, "Del análisis a la comprobación.", 28 if mobile else 27, MUTED)
    body += text(40 if mobile else 58, 194 if mobile else 222, "Flujos y agentes para SEO y GEO.", 28 if mobile else 26, MUTED)
    body += text(40 if mobile else 58, 240 if mobile else 286, "Claude Code · Codex · OpenCode", 25 if mobile else 22, CYAN)
    nodes = [(40, 300), (340, 300), (40, 436), (340, 436)] if mobile else [(660, 68), (922, 68), (660, 220), (922, 220)]
    path = "M170 352H470V488H170V352" if mobile else "M774 125H1036V277H774V125"
    body += f'<path d="{path}" fill="none" stroke="#58748f" stroke-width="2"/><path d="{path}" class="raulveneri-circuit_trace" fill="none" stroke="{CYAN}" stroke-width="3"/>'
    labels = [("01", "Analizar"), ("02", "Decidir"), ("04", "Verificar"), ("03", "Construir")]
    for i, ((x, y), (number, label)) in enumerate(zip(nodes, labels)):
        body += f'<g class="raulveneri-panel_reveal" style="animation-delay:{i*.2}s"><rect x="{x}" y="{y}" width="228" height="112" rx="14" fill="#122338" stroke="#58748f"/>'
        body += text(x+20, y+36, number, 20, AMBER, 600)
        body += text(x+20, y+79, label, 31, weight=600) + '</g>'
    body += text(40 if mobile else 58, 606 if mobile else 367, "Repositorio público en GitHub ↗", 26 if mobile else 23, CYAN, 500)
    document("search-optimization-toolkit" + ("--mobile" if mobile else ""), width, height, "SEO Kit: analizar, decidir, construir y verificar.", body)


def website(robotics=False):
    if robotics:
        body = '<g fill="none" stroke="#72ede2" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><path d="M550 244H720M635 244V221M635 120V88M600 156V187M670 156V187"/><rect x="568" y="120" width="134" height="100" rx="24" fill="#102b38"/><circle cx="635" cy="81" r="7" fill="#ffd28a"/><path d="M592 120L576 104M678 120L694 104M580 244V260M690 244V260" stroke="#ffd28a"/></g>'
        body += text(42, 330, "Roboticz Lab", 61, weight=700)
        body += text(44, 391, "Robótica con IA.", 32, MUTED)
        body += text(44, 438, "Noticias y proyectos para montar.", 31, MUTED)
        name, title = "robotics-publication", "Roboticz Lab. Robótica con IA, noticias y guías de montaje."
    else:
        body = '<g fill="none" stroke="#72ede2" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><rect x="535" y="80" width="205" height="165" rx="16" fill="#102b38"/><path d="M535 119H740M561 145H603M561 168H620M647 208L672 180 696 191 719 151"/><path d="M705 151H719V166" stroke="#ffd28a"/></g>'
        body += text(42, 330, "raulveneri.com", 59, weight=700)
        body += text(44, 391, "Marketing con IA.", 32, MUTED)
        body += text(44, 438, "Mi web también es mi laboratorio.", 31, MUTED)
        name, title = "personal-website", "Raúl Veneri. Marketing con IA y mi web como laboratorio."
    body += text(44, 546, "Abrir la web ↗", 30, CYAN, 500)
    document(name, 810, 600, title, body, inset=16)


def mark(kind, x, y, color, size=1):
    shapes = {
        "Python": '<path d="M-17 3V-15Q-17-24-7-24H9Q20-24 20-14V-3H-5Q-15-3-15 8V21H-22Q-32 21-32 10V3Z"/><path d="M17-3V15Q17 24 7 24H-9Q-20 24-20 14V3H5Q15 3 15-8V-21H22Q32-21 32-10V-3Z" opacity=".6"/>',
        "JavaScript": '<rect x="-28" y="-28" width="56" height="56" rx="7"/>' + text(-20, 16, "JS", 30, "#0b1422", 700),
        "TypeScript": '<rect x="-28" y="-28" width="56" height="56" rx="7"/>' + text(-22, 16, "TS", 30, "#0b1422", 700),
        "Astro": '<path d="M-27 21L-9-26H9L27 21 12 15 0-13-12 15Z"/><path d="M-10 25Q0 40 10 25Q0 28-10 25" fill="#ffd28a"/>',
        "Tailwind CSS": '<path d="M-32-1Q-22-25-3-12T32-13Q22 12 3-1T-32-1M-32 17Q-22-7-3 6T32 5Q22 30 3 17T-32 17"/>',
        "Cloudflare": '<path d="M-31 16H32Q41 5 29-4Q29-24 9-24-9-24-12-8-31-14-34 3-45 7-37 16Z"/>',
    }
    return f'<g transform="translate({x} {y}) scale({size})" fill="{color}">{shapes[kind]}</g>'


def stack(mobile=False):
    width, height = (640, 480) if mobile else (1200, 264)
    cols = 2 if mobile else 3
    cardw, cardh = (282, 128) if mobile else (368, 100)
    margin, gap = (26, 24) if mobile else (24, 24)
    names = ["Python", "JavaScript", "TypeScript", "Astro", "Tailwind CSS", "Cloudflare"]
    colors = [AMBER, "#f3df75", "#83baff", "#f8a8d3", CYAN, "#ffbc79"]
    body = ""
    for i, (name, color) in enumerate(zip(names, colors)):
        x, y = margin+(i % cols)*(cardw+gap), 26+(i//cols)*(cardh+22)
        body += f'<g class="raulveneri-panel_reveal" style="animation-delay:{i*.12}s"><rect x="{x}" y="{y}" width="{cardw}" height="{cardh}" rx="16" fill="#102034" stroke="#58748f"/>'
        body += mark(name, x+cardw/2 if mobile else x+54, y+40 if mobile else y+50, color, .7 if mobile else .85)
        body += text(x+cardw/2 if mobile else x+105, y+98 if mobile else y+60, name, 30 if mobile else 28, weight=600, extra='text-anchor="middle"' if mobile else "")
        body += f'<path class="raulveneri-circuit_trace" d="M{x+18} {y+cardh}H{x+cardw-18}" fill="none" stroke="{color}" stroke-width="2"/></g>'
    document("development-stack" + ("--mobile" if mobile else ""), width, height, "Python, JavaScript, TypeScript, Astro, Tailwind CSS y Cloudflare.", body)


def main():
    ASSETS.mkdir(exist_ok=True)
    for mobile in (False, True):
        hero(mobile)
        toolkit(mobile)
        stack(mobile)
    website()
    website(True)
    print(f"Generated 8 original SVG assets in {ASSETS}")


if __name__ == "__main__":
    main()
