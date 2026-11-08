import fs from 'node:fs';
import { T } from './textos.mjs';
import { tarjetaLenguajes } from './secciones/lenguajes.mjs';
import { actividad } from './secciones/actividad.mjs';
for (const t of Object.values(T)) {
 for (const [file,render] of [['lenguajes.svg',tarjetaLenguajes],['actividad.svg',actividad]]) {
  const content=await render(t);
  fs.writeFileSync(`assets/${t.lang}/${file}`,content);
  const label=content.match(/aria-label='([^']*)'/)[1].replace(/&apos;/g,"'").replace(/&quot;/g,'&quot;');
  const readme=t.lang==='en'?'README.md':'README.es.md';
  const text=fs.readFileSync(readme,'utf8');
  const pattern=new RegExp(`(<img src="assets/${t.lang}/${file.replace('.','\\.')}" alt=")[^"]*(" width="100%">)`);
  if (!pattern.test(text)) throw new Error(`Missing chart in ${readme}: ${file}`);
  fs.writeFileSync(readme,text.replace(pattern,(_,a,b)=>a+label+b));
 }
}
