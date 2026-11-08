import fs from 'node:fs';
import path from 'node:path';
export const datos = JSON.parse(fs.readFileSync(path.join(import.meta.dirname,'datos.json'),'utf8'));
export const fechaTxt = (iso, locale, opts) => new Intl.DateTimeFormat(locale,{timeZone:'UTC',...opts}).format(new Date(`${iso}T00:00:00Z`));
export function lenguajes() {
  const bytes = {};
  for (const r of Object.values(datos.repos)) for (const [l,b] of Object.entries(r.languages)) bytes[l]=(bytes[l]||0)+b;
  const total=Object.values(bytes).reduce((a,b)=>a+b,0);
  if (!total) throw new Error('No language data available');
  const all=Object.entries(bytes).sort((a,b)=>b[1]-a[1]);
  const top=all.slice(0,2).map(([nombre,b])=>({nombre,bytes:b}));
  const other=all.slice(2).reduce((a,[,b])=>a+b,0);
  if (other) top.push({nombre:'Other / Otros',bytes:other});
  const fractions=top.map(l=>({...l,raw:l.bytes/total*100,pct:Math.floor(l.bytes/total*100)}));
  let remaining=100-fractions.reduce((a,l)=>a+l.pct,0);
  for (const l of [...fractions].sort((a,b)=>(b.raw%1)-(a.raw%1))) if (remaining-->0) l.pct++;
  return {total,kb:Math.round(total/1024),lista:fractions};
}
export function commits() {
  const names=Object.keys(datos.repos);
  const end=new Date(`${datos.fecha}T00:00:00Z`);
  const dias=Array.from({length:30},(_,i)=>{ const d=new Date(end); d.setUTCDate(d.getUTCDate()-29+i); const fecha=d.toISOString().slice(0,10); return {fecha,total:names.reduce((a,r)=>a+(datos.repos[r].commits[fecha]||0),0)}; });
  const all=names.map(nombre=>({nombre,total:Object.values(datos.repos[nombre].commits).reduce((a,b)=>a+b,0)})).sort((a,b)=>b.total-a.total);
  const porRepo=all.slice(0,3); if (all.length>3) porRepo.push({nombre:'Other / Otros',total:all.slice(3).reduce((a,r)=>a+r.total,0)});
  return {dias,porRepo,total:dias.reduce((a,d)=>a+d.total,0),repoCount:names.length};
}
