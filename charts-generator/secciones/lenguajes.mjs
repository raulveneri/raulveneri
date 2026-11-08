import { C } from '../tokens.mjs';
import { texto, anim, svg } from '../helpers.mjs';
import { lenguajes } from '../datos.mjs';

const D = 10;

// donut y barras con datos reales; el donut se dibuja y las barras crecen en bucle
export async function tarjetaLenguajes(t) {
  const W = 1000, H = 340;
  const { kb, lista } = lenguajes();
  const colores = [C.lime, C.mint, C.teal];
  const cx = 170, cy = 168, r = 70, sw = 28;
  let acc = 0;
  const segmentos = lista.map((l, i) => {
    const a = 0.02 + i * 0.18, b = a + 0.18;
    const base = `${l.pct} ${100 - l.pct}`;
    const s = `<circle cx='${cx}' cy='${cy}' r='${r}' pathLength='100' fill='none' stroke='${colores[i]}' stroke-width='${sw}' stroke-dasharray='${base}' stroke-dashoffset='${-acc}' transform='rotate(-90 ${cx} ${cy})'>
  ${anim('stroke-dasharray', `0 100;0 100;${base};${base};0 100`, `0;${a};${b};0.9;1`, D)}
</circle>`;
    acc += l.pct;
    return s;
  }).join('\n');
  const barras = lista.map((l, i) => {
    const y = 138 + i * 70, ancho = Math.round((l.pct / 100) * 600);
    const a = (0.1 + i * 0.1).toFixed(2), b = (+a + 0.3).toFixed(2);
    return `
<rect x='340' y='${y - 14}' width='14' height='14' rx='3' fill='${colores[i]}'/>
${texto(364, y, l.nombre, 18, C.white, { peso: 600 })}
${texto(940, y, `${l.pct}%`, 18, C.white, { peso: 600, anchor: 'end' })}
<rect x='340' y='${y + 14}' width='600' height='10' rx='5' fill='${C.paper}' fill-opacity='0.15'/>
<rect x='340' y='${y + 14}' width='${ancho}' height='10' rx='5' fill='${colores[i]}'>
  ${anim('width', `0;0;${ancho};${ancho};0`, `0;${a};${b};0.9;1`, D)}
</rect>`;
  }).join('\n');
  const cuerpo = `
<rect width='${W}' height='${H}' rx='16' fill='${C.ink}'/>
${texto(40, 52, t.langCardTitle, 20, C.white, { peso: 600 })}
${texto(40, 74, t.langCardSub, 13, C.mint)}
<circle cx='${cx}' cy='${cy}' r='${r}' fill='none' stroke='${C.paper}' stroke-opacity='0.12' stroke-width='${sw}'/>
${segmentos}
${texto(cx, cy - 2, `${kb} KB`, 26, C.white, { peso: 600, anchor: 'middle' })}
${texto(cx, cy + 20, t.langCenter, 13, C.mint, { anchor: 'middle' })}
${barras}`;
  return svg(W, H, cuerpo, `${t.langCardTitle}: ${lista.map((l) => `${l.nombre} ${l.pct}%`).join(', ')}.`);
}
