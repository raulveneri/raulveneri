// Imagenes dadas por la usuaria (assets/img/*.png, PNG animado con transparencia), incrustadas en los SVG como data URI.
import fs from 'node:fs';
import path from 'node:path';

const dir = path.resolve(import.meta.dirname, '..', 'assets', 'img');

export function dims(id) {
  const b = fs.readFileSync(path.join(dir, `${id}.png`));
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
}

// escala: 1 = tamano de archivo. pix: mantiene el pixel art nitido al ampliar
export function sprite(id, x, y, escala = 1, { pix = false, hijos = '' } = {}) {
  const b = fs.readFileSync(path.join(dir, `${id}.png`));
  const w = Math.round(b.readUInt32BE(16) * escala), h = Math.round(b.readUInt32BE(20) * escala);
  const abre = `<image x='${x}' y='${y}' width='${w}' height='${h}'${pix ? " style='image-rendering:pixelated'" : ''} href='data:image/png;base64,${b.toString('base64')}'`;
  return hijos ? `${abre}>${hijos}</image>` : `${abre}/>`;
}
