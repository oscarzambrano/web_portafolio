/**
 * Genera el CV en PDF a partir de tools/cv/cv.html.
 *
 * El PDF se commitea porque Netlify no tiene navegador en el build. Si cambias
 * el contenido del sitio, vuelve a correr esto para que el PDF no se desfase:
 *
 *   npm install --no-save playwright-core
 *   node tools/cv/build-cv.mjs
 *
 * Requiere un Chromium local. Se toma de PLAYWRIGHT_BROWSERS_PATH o de la ruta
 * que se pase en CHROMIUM_PATH.
 */
import { chromium } from 'playwright-core';
import { existsSync, copyFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const aqui = dirname(fileURLToPath(import.meta.url));
const raiz = resolve(aqui, '../..');
const salida = resolve(raiz, 'static/cv/oscar-zambrano-cv.pdf');

const candidatos = [
  process.env.CHROMIUM_PATH,
  '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  '/usr/bin/chromium',
  '/usr/bin/google-chrome',
].filter(Boolean);

const navegador = candidatos.find((p) => existsSync(p));
if (!navegador) {
  console.error('No encontré Chromium. Define CHROMIUM_PATH.');
  process.exit(1);
}

// El HTML referencia avatar.jpg como archivo hermano.
copyFileSync(
  resolve(raiz, 'content/authors/admin/avatar.jpg'),
  resolve(aqui, 'avatar.jpg'),
);

mkdirSync(dirname(salida), { recursive: true });

const browser = await chromium.launch({ executablePath: navegador, args: ['--no-sandbox'] });
const page = await browser.newPage();
await page.goto(pathToFileURL(resolve(aqui, 'cv.html')).href, { waitUntil: 'networkidle' });
await page.pdf({
  path: salida,
  format: 'A4',
  printBackground: true,
  // Los márgenes los define @page en el CSS.
  margin: { top: '0', right: '0', bottom: '0', left: '0' },
});
await browser.close();

console.log('CV generado en', salida);
