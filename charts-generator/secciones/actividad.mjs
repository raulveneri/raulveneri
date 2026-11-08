import { C } from '../tokens.mjs';
import { texto, tarjeta, anim, svg } from '../helpers.mjs';
import { sprite, dims } from '../imagenes.mjs';
import { commits, fechaTxt, datos } from '../datos.mjs';

const D = 10;

// curva suave que pasa por los puntos (Catmull-Rom convertida a bezier)
function suave(pts) {
  let d = `M${pts[0][0]} ${pts[0][1]}`;
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
    const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
    const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
    d += ` C${c1[0].toFixed(1)} ${c1[1].toFixed(1)} ${c2[0].toFixed(1)} ${c2[1].toFixed(1)} ${p2[0]} ${p2[1]}`;
  }
  return d;
}

// curva de commits por dia con actividad y panel "por proyecto"; datos reales de GitHub
export async function actividad(t) {
  const W = 1000, H = 320;
  const { dias, porRepo, total, repoCount } = commits();
  const maxV = Math.max(10, Math.ceil(Math.max(...dias.map((d) => d.total)) / 5) * 5);
  const yb = 250, alto = 150, n = dias.length;
  const xs = dias.map((_, i) => (n === 1 ? 345 : 130 + i * (430 / (n - 1))));
  const pts = dias.map((d, i) => [Math.round(xs[i]), Math.round(yb - (d.total / maxV) * alto)]);
  const curva = suave(pts);
  const area = `${curva} L${pts[n - 1][0]} ${yb} L${pts[0][0]} ${yb} Z`;
  const grid = [0, maxV / 2, maxV].map((v) => {
    const y = Math.round(yb - (v / maxV) * alto);
    return `<line x1='70' x2='640' y1='${y}' y2='${y}' stroke='${C.ink}' stroke-opacity='0.12'/>${texto(58, y + 4, String(v), 12, C.ink, { anchor: 'end' })}`;
  }).join('\n');
  const puntos = pts.map(([x, y], i) => {
    const a = (0.02 + 0.4 * (n > 1 ? i / (n - 1) : 0)).toFixed(3), b = (+a + 0.03).toFixed(3);
    return `<circle cx='${x}' cy='${y}' r='7' fill='${C.white}' stroke='${C.teal}' stroke-width='3'>${anim('opacity', '0;0;1;1', `0;${a};${b};1`, D)}</circle>

${(i === 0 || i === 7 || i === 14 || i === 21 || i === n - 1) ? texto(x, yb + 24, fechaTxt(dias[i].fecha, t.locale, { month: 'short', day: 'numeric' }), 12, C.ink, { anchor: 'middle' }) : ''}`;
  }).join('\n');
  const maxRepo = Math.max(1, ...porRepo.map((r) => r.total));
  const colores = [C.teal, C.ink];
  const filas = porRepo.map((r, i) => {
    const y = 142 + i * 40, w = Math.round((r.total / maxRepo) * 260);
    const a = (0.1 + i * 0.1).toFixed(2), b = (+a + 0.3).toFixed(2);
    return `${texto(700, y, r.nombre === 'raulveneri' ? t.repoProfile : r.nombre, 15, C.ink)}
${texto(960, y, String(r.total), 15, C.ink, { peso: 600, anchor: 'end' })}
<rect x='700' y='${y + 10}' width='260' height='8' rx='4' fill='${C.ink}' fill-opacity='0.1'/>
<rect x='700' y='${y + 10}' width='${w}' height='8' rx='4' fill='${colores[i % 2]}'>${anim('width', `0;0;${w};${w};0`, `0;${a};${b};0.9;1`, D)}</rect>`;
  }).join('\n');
  const sub = t.actCardSub.replace('{n}', total).replace('{r}', repoCount).replace('{date}', fechaTxt(datos.fecha, t.locale, { year: 'numeric', month: 'short', day: 'numeric' }));
  const cb = dims('cubone');
  const cuerpo = `
${tarjeta(W, H, C.paper)}
${texto(40, 52, t.actCardTitle, 20, C.ink, { peso: 600 })}
${texto(40, 74, sub, 13, C.ink)}
${grid}
<path d='${area}' fill='${C.teal}' fill-opacity='0.2'>${anim('opacity', '0;0;1;1;0', '0;0.1;0.45;0.9;1', D)}</path>
<path d='${curva}' pathLength='1' stroke-dasharray='1' stroke-dashoffset='0' fill='none' stroke='${C.teal}' stroke-width='4' stroke-linecap='round'>
  ${anim('stroke-dashoffset', '1;1;0;0', '0;0.02;0.42;1', D)}
</path>
${puntos}
${texto(700, 110, t.byProject.toUpperCase(), 12, C.ink, { peso: 600, extra: "letter-spacing='1.5'" })}
${filas}
${sprite('cubone', W - 24 - cb.w, 18)}`;
  return svg(W, H, cuerpo, `${t.actCardTitle}: ${sub}. ${dias.map((d) => `${fechaTxt(d.fecha, t.locale, { month: 'short', day: 'numeric' })}, ${d.total}`).join('; ')}.`);
}
