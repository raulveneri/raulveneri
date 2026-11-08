import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.dirname(fileURLToPath(import.meta.url));
const user = 'raulveneri';
const token = process.env.GH_TOKEN || execFileSync('gh', ['auth', 'token'], {encoding:'utf8'}).trim();
async function get(url) {
  let all = [];
  while (url) {
    const res = await fetch(url, {headers:{Authorization:`Bearer ${token}`, Accept:'application/vnd.github+json', 'User-Agent':'profile-charts', 'X-GitHub-Api-Version':'2022-11-28'}});
    if (!res.ok) throw new Error(`GitHub API ${res.status}: ${url}`);
    const value = await res.json();
    if (!Array.isArray(value)) return value;
    all.push(...value);
    url = res.headers.get('link')?.match(/<([^>]+)>; rel="next"/)?.[1];
  }
  return all;
}
const now = new Date();
const date = now.toISOString().slice(0,10);
const start = new Date(`${date}T00:00:00Z`); start.setUTCDate(start.getUTCDate()-29);
const repoList = await get(`https://api.github.com/users/${user}/repos?per_page=100&type=owner`);
const repos = {};
for (const repo of repoList.filter(r => !r.private && !r.fork && r.owner.login.toLowerCase() === user)) {
  const base = `https://api.github.com/repos/${user}/${encodeURIComponent(repo.name)}`;
  const languages = await get(`${base}/languages`);
  let items = [];
  if (repo.size > 0) items = await get(`${base}/commits?author=${user}&since=${start.toISOString()}&per_page=100`);
  const commits = {};
  for (const item of items) {
    const day = item.commit.author.date.slice(0,10);
    if (day >= start.toISOString().slice(0,10) && day <= date) commits[day] = (commits[day] || 0) + 1;
  }
  repos[repo.name] = {languages, commits};
}
if (!Object.keys(repos).length) throw new Error('No public owned repositories returned');
fs.writeFileSync(path.join(root,'datos.json'), JSON.stringify({fecha:date, repos}, null, 2)+'\n');
console.log(`Fetched ${Object.keys(repos).length} public non-fork repositories, last 30 UTC days through ${date}`);
