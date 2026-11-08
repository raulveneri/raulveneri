#!/usr/bin/env python3
"""Generate the owner's editorial profile artwork, without third-party packages."""
from base64 import b64encode
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'assets'
INK, MUTED, ACCENT, PAPER = '#242321', '#615c55', '#ad3d28', '#f5f2ec'
CYAN, AMBER = '#72ede2', '#ffd28a'


def text(x, y, value, size=24, color=INK, weight=400, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{escape(value)}</text>'


BASE = '''
text { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; }
.raulveneri-serif { font-family: Georgia, 'Times New Roman', serif; font-style: italic; }
.raulveneri-monospace { font-family: 'DejaVu Sans Mono', Consolas, monospace; }
.raulveneri-demo_stage { opacity: 0; }
.raulveneri-demo_stage--decision { opacity: 1; }
'''
MOTION = '''
@media (prefers-reduced-motion: no-preference) {
 .raulveneri-heading_underline { animation: raulveneri-underline 12s ease-in-out infinite; transform-origin: 52px 0; }
 .raulveneri-demo_stage--request { animation: raulveneri-request 12s linear infinite; }
 .raulveneri-demo_stage--finding { animation: raulveneri-finding 12s linear infinite; }
 .raulveneri-demo_stage--decision { animation: raulveneri-decision 12s linear infinite; }
 .raulveneri-guide_scroll { animation: raulveneri-scroll 14s ease-in-out infinite; }
 .raulveneri-stack_gesture { transform-box: fill-box; transform-origin: center; }
 .raulveneri-stack_gesture--python { animation: raulveneri-orbit 12s ease-in-out infinite; }
 .raulveneri-stack_gesture--javascript { animation: raulveneri-code 12s ease-in-out 2s infinite; }
 .raulveneri-stack_gesture--typescript { animation: raulveneri-code 12s ease-in-out 4s infinite; }
 .raulveneri-stack_gesture--astro { animation: raulveneri-lift 12s ease-in-out 6s infinite; }
 .raulveneri-stack_gesture--tailwind { animation: raulveneri-wave 12s ease-in-out 8s infinite; }
 .raulveneri-stack_gesture--cloudflare { animation: raulveneri-arrive 12s ease-in-out 10s infinite; }
}
@keyframes raulveneri-underline { 0%, 8%, 100% { transform: scaleX(.3); } 24%, 82% { transform: scaleX(1); } }
@keyframes raulveneri-request { 0%, 30% { opacity: 1; } 33%, 96% { opacity: 0; } 100% { opacity: 1; } }
@keyframes raulveneri-finding { 0%, 30%, 66%, 100% { opacity: 0; } 33%, 63% { opacity: 1; } }
@keyframes raulveneri-decision { 0%, 63%, 100% { opacity: 0; } 66%, 96% { opacity: 1; } }
@keyframes raulveneri-scroll { 0%, 18%, 100% { transform: translateY(0); } 55%, 82% { transform: translateY(-280px); } }
@keyframes raulveneri-orbit { 0%, 3%, 20%, 100% { transform: rotate(0); } 9% { transform: rotate(-12deg); } 14% { transform: rotate(8deg); } }
@keyframes raulveneri-code { 0%, 3%, 20%, 100% { transform: translateX(0); } 9% { transform: translateX(-5px); } 14% { transform: translateX(5px); } }
@keyframes raulveneri-lift { 0%, 3%, 20%, 100% { transform: translateY(0); } 10%, 14% { transform: translateY(-9px); } }
@keyframes raulveneri-wave { 0%, 3%, 20%, 100% { transform: skewX(0); } 9% { transform: skewX(-12deg); } 14% { transform: skewX(9deg); } }
@keyframes raulveneri-arrive { 0%, 3%, 20%, 100% { transform: translateX(0); } 9% { transform: translateX(-7px); } 14% { transform: translateX(3px); } }
'''
REDUCED = '''
@media (prefers-reduced-motion: reduce) {
 *, *::before, *::after { animation: none !important; transition: none !important; }
}
'''


def document(name, width, height, title, body, mobile=False, static=False, dark=False, defs=''):
    suffix = ('--mobile' if mobile else '') + ('--static' if static else '')
    prefix = 'raulveneri-' + name.replace('-', '_') + suffix.replace('-', '_')
    bg = '#151b24' if dark else PAPER
    description = 'Versión estática.' if static else 'Animación con pausas de lectura. Respeta la preferencia de movimiento reducido.'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="{prefix}_title {prefix}_description">
<title id="{prefix}_title">{escape(title)}</title>
<desc id="{prefix}_description">{escape(title)} {description}</desc>
<defs>{defs}</defs>
<style>{BASE}{'' if static else MOTION}{REDUCED}</style>
<rect width="{width}" height="{height}" rx="{16 if dark else 0}" fill="{bg}"/>
{body}
</svg>
'''
    (ASSETS / f'raulveneri-{name}{suffix}.svg').write_text(svg, encoding='utf-8')


def hero(mobile=False, static=False):
    w, h = (640, 350) if mobile else (1200, 360)
    x = 36 if mobile else 52
    body = text(x, 100 if mobile else 127, 'Marketing, código', 58 if mobile else 91, weight=700, extra='letter-spacing="-2"')
    body += text(x, 180 if mobile else 237, 'y agentes de IA.', 66 if mobile else 100, extra='class="raulveneri-serif"')
    body += f'<path class="raulveneri-heading_underline" d="M52 {214 if mobile else 271}H{595 if mobile else 1098}" stroke="{ACCENT}" stroke-width="4"/>'
    body += text(x, 296 if mobile else 328, 'SEO / GOOGLE ADS / AUTOMATIZACIÓN', 23 if mobile else 22, MUTED, extra='letter-spacing="1"')
    document('profile-heading', w, h, 'Marketing, código y agentes de IA.', body, mobile, static)


def toolkit(mobile=False, static=False):
    w, h = (640, 810) if mobile else (1200, 560)
    x = 36 if mobile else 52
    body = text(x, 96 if mobile else 120, 'SEO Kit', 74 if mobile else 94, weight=700, extra='letter-spacing="-3"')
    body += text(x, 157 if mobile else 213, 'Analiza tu web.', 37 if mobile else 40)
    body += text(x, 206 if mobile else 271, 'Entiende qué falla.', 37 if mobile else 40)
    body += text(x, 255 if mobile else 329, 'Decide qué cambiar.', 37 if mobile else 40, ACCENT, 600)
    if mobile:
        body += '<path d="M36 298H604" stroke="#c9c2b8"/>'
        px, py = 36, 354
    else:
        body += '<path d="M604 52V444" stroke="#c9c2b8"/>'
        px, py = 650, 90
    body += text(px, py, 'EJEMPLO DOCUMENTADO · WEB LOCAL', 21 if mobile else 17, MUTED)
    stages = [
        ('request', '01 / LA PETICIÓN', ['Auditar dos páginas.', 'Revisar técnica y contenido.'], ['Análisis de HTML compilado.', 'Sin modificar la web.']),
        ('finding', '02 / EL HALLAZGO', ['Un enlace está roto.', '/about/ → /missing/'], ['La página de destino no existe.', 'El informe indica dónde ocurre.']),
        ('decision', '03 / QUÉ HACER', ['Corregir el enlace', 'o recuperar la página.'], ['La opción depende del proyecto.', 'Tú decides qué tiene sentido.']),
    ]
    for kind, label, lines, detail in stages:
        body += f'<g class="raulveneri-demo_stage raulveneri-demo_stage--{kind}">'
        body += text(px, py+64, label, 22 if mobile else 19, ACCENT, 600)
        for i, line in enumerate(lines):
            body += text(px, py+128+i*47, line, 32 if mobile else 30, weight=600)
        for i, line in enumerate(detail):
            body += text(px, py+240+i*37, line, 27 if mobile else 24, MUTED)
        body += '</g>'
    body += text(x, h-77, 'Claude Code · Codex · OpenCode', 25 if mobile else 24, MUTED)
    body += text(x, h-32, 'Quiero ver SEO Kit ↗', 28 if mobile else 26, ACCENT, 600)
    document('seo-kit-demonstration', w, h, 'SEO Kit: analiza tu web, entiende qué falla y decide qué cambiar. Demostración adaptada del ejemplo documentado.', body, mobile, static)


def website(mobile=False, static=False):
    w, h = (640, 920) if mobile else (1200, 620)
    x = 36 if mobile else 52
    body = text(x, 78 if mobile else 106, 'Lo que aprendo,', 47 if mobile else 45, weight=600)
    body += text(x, 137 if mobile else 168, 'lo explico aquí.', 51 if mobile else 50, extra='class="raulveneri-serif"')
    body += text(x, 196 if mobile else 238, 'raulveneri.com', 27, ACCENT, 600)
    if not mobile:
        body += text(x, 350, 'Guías sobre agentes,', 27, MUTED)
        body += text(x, 389, 'SEO y herramientas', 27, MUTED)
        body += text(x, 428, 'que uso en mi trabajo.', 27, MUTED)
    sx, sy, sw, sh = (24, 246, 592, 580) if mobile else (466, 38, 700, 516)
    clip = 'raulveneri-guide_viewport' + ('_mobile' if mobile else '')
    defs = f'<clipPath id="{clip}"><rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="4"/></clipPath>'
    source = ASSETS / 'sources' / ('raulveneri-guide-mobile.png' if mobile else 'raulveneri-guide-desktop.png')
    data = b64encode(source.read_bytes()).decode('ascii')
    image_height = sw*1440/(600 if mobile else 1100)
    body += f'<g clip-path="url(#{clip})"><g class="raulveneri-guide_scroll"><image x="{sx}" y="{sy}" width="{sw}" height="{image_height}" href="data:image/png;base64,{data}"/></g></g>'
    body += f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="4" fill="none" stroke="#b8afa2"/>'
    body += text(x, h-35, 'Quiero leer las guías ↗', 28 if mobile else 26, ACCENT, 600)
    document('website-guides', w, h, 'Mi web: captura real de la guía Google Analytics en Claude Code. Quiero leer las guías.', body, mobile, static, defs=defs)


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



def stack(mobile=False, static=False):
    width, height = (640, 480) if mobile else (1200, 264)
    cols = 2 if mobile else 3
    cardw, cardh = (282, 128) if mobile else (368, 100)
    margin, gap = (26, 24) if mobile else (24, 24)
    names = ['Python', 'JavaScript', 'TypeScript', 'Astro', 'Tailwind CSS', 'Cloudflare']
    colors = [AMBER, '#f3df75', '#83baff', '#f8a8d3', CYAN, '#ffbc79']
    gestures = ['python', 'javascript', 'typescript', 'astro', 'tailwind', 'cloudflare']
    body = ''
    for i, (name, color, gesture) in enumerate(zip(names, colors, gestures)):
        x, y = margin+(i % cols)*(cardw+gap), 26+(i//cols)*(cardh+22)
        body += f'<rect x="{x}" y="{y}" width="{cardw}" height="{cardh}" rx="12" fill="#1d2838" stroke="#496078"/>'
        body += f'<g class="raulveneri-stack_gesture raulveneri-stack_gesture--{gesture}">'
        body += mark(name, x+cardw/2 if mobile else x+54, y+40 if mobile else y+50, color, .7 if mobile else .85) + '</g>'
        body += text(x+cardw/2 if mobile else x+105, y+98 if mobile else y+60, name, 30 if mobile else 28, '#f1f5f9', 600, extra='text-anchor="middle"' if mobile else '')
    document('development-tools', width, height, 'Python, JavaScript, TypeScript, Astro, Tailwind CSS y Cloudflare. Cada símbolo tiene un movimiento propio.', body, mobile, static, dark=True)


def main():
    ASSETS.mkdir(exist_ok=True)
    for mobile in (False, True):
        for static in (False, True):
            for build in (hero, toolkit, website, stack):
                build(mobile, static)
    print(f'Generated 16 SVG assets in {ASSETS}')


if __name__ == '__main__':
    main()
