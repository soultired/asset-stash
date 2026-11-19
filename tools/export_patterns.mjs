// Usage: node export_patterns.mjs <hero-patterns es.js absolute path> <out dir> <names json out>
import fs from 'node:fs';
import { pathToFileURL } from 'node:url';

const [modPath, outDir, namesOut] = process.argv.slice(2);
const hp = await import(pathToFileURL(modPath).href);
fs.mkdirSync(outDir, { recursive: true });

const kebab = (s) => s.replace(/([A-Z])/g, (m) => '-' + m.toLowerCase());
const names = [];
for (const [key, fn] of Object.entries(hp)) {
  if (typeof fn !== 'function') continue;
  const css = fn('#9C92AC', 0.4);
  const m = css.match(/^url\('data:image\/svg\+xml,(.*)'\)$/s);
  if (!m) {
    console.error('skip', key);
    continue;
  }
  const svg = decodeURIComponent(m[1]);
  const name = kebab(key);
  fs.writeFileSync(`${outDir}/${name}.svg`, svg + '\n');
  names.push(name);
}
fs.writeFileSync(namesOut, JSON.stringify(names));
console.log('patterns exported:', names.length);
