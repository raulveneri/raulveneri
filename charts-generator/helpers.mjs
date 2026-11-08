import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import subsetFont from 'subset-font';
import { C, FUENTE, FORMA } from './tokens.mjs';

const aqui = path.dirname(fileURLToPath(import.meta.url));
const ruta = (peso) => path.join(aqui, 'node_modules/@fontsource/manrope/files', `manrope-latin-${peso}-normal.woff2`);

export const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/'/g, '&apos;').replace(/"/g, '&quot;');
const unesc = (s) => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&apos;/g, "'").replace(/&quot;/g, '"').replace(/&amp;/g, '&');

// ancho aproximado de Manrope; se confirma mirando el resultado
export const ancho = (t, size, f = 0.6) => t.length * size * f;
export function envolver(texto, size, maxAncho, f = 0.6) {
  const max = Math.floor(maxAncho / (size * f));
  const out = []; let linea = '';
  for (const p of texto.split(' ')) {
    if ((linea + ' ' + p).trim().length > max) { out.push(linea); linea = p; } else linea = (linea + ' ' + p).trim();
  }
  if (linea) out.push(linea);
  return out;
}
export const texto = (x, y, t, size, fill, { peso = 400, anchor = 'start', extra = '' } = {}) =>
  `<text x='${x}' y='${y}' font-size='${size}' font-weight='${peso}' fill='${fill}' text-anchor='${anchor}' ${extra}>${esc(t)}</text>`;
export const lineas = (x, y, arr, size, alto, fill, opts = {}) => arr.map((l, i) => texto(x, y + i * alto, l, size, fill, opts)).join('\n');
export const tarjeta = (w, h, fill) =>
  `<rect x='0.5' y='0.5' width='${w - 1}' height='${h - 1}' rx='${FORMA.radio}' fill='${fill}' stroke='${C.ink}' stroke-opacity='${FORMA.borde}'/>`;

// animacion de bucle: valores y tiempos clave; el valor base del atributo es el estado final
export const anim = (attr, values, keyTimes, dur, extra = '') =>
  `<animate attributeName='${attr}' values='${values}' keyTimes='${keyTimes}' dur='${dur}s' repeatCount='indefinite' ${extra}/>`;

// envuelve el cuerpo en un SVG con la fuente recortada e incrustada
export async function svg(w, h, cuerpo, etiqueta) {
  const chars = new Set();
  for (const m of cuerpo.matchAll(/<text[^>]*>([^<]*)<\/text>/g)) for (const ch of unesc(m[1])) chars.add(ch);
  const juego = [...chars].join('');
  let css = '';
  for (const peso of FUENTE.pesos) {
    const sub = await subsetFont(fs.readFileSync(ruta(peso)), juego, { targetFormat: 'woff2' });
    css += `@font-face{font-family:'${FUENTE.familia}';font-weight:${peso};src:url(data:font/woff2;base64,${Buffer.from(sub).toString('base64')}) format('woff2');}`;
  }
  return `<svg xmlns='http://www.w3.org/2000/svg' width='${w}' height='${h}' viewBox='0 0 ${w} ${h}' role='img' aria-label='${esc(etiqueta)}' font-family="${FUENTE.familia}, ${FUENTE.respaldo}">
<style>${css}</style>
${cuerpo}
</svg>
`;
}
