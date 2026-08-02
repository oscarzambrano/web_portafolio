# AGENTS.md — contexto del proyecto

Contexto para agentes que trabajen sobre este repositorio, incluido el agente de
Netlify. Si necesitas el porqué histórico de alguna decisión, está en
[`docs/HANDOFF.md`](docs/HANDOFF.md).

## Qué es

Sitio personal de Oscar Zambrano, en `https://www.oscarzambrano.name`. Es un CV
en línea, en español, de **dos páginas**: la portada (`/`) y la trayectoria
(`/experiencia/`). No es una aplicación: no hay backend, ni base de datos, ni
formularios, ni autenticación, ni estado de servidor.

## Stack

| Pieza | Detalle |
|---|---|
| Generador | **Hugo extended `0.152.2`** — la edición normal falla, el tema usa SCSS |
| Tema | **Hugo Blox** (`blox-tailwind`), vía **módulos de Go** — ver `go.mod`. **No hay carpeta `themes/`** |
| CSS | Tailwind v4, resuelto por Hugo durante el build; por eso hace falta `node_modules` |
| Node | 22, solo en build. **No hay runtime de Node en producción** |
| Salida | HTML estático en `public/`, servido desde la CDN |

Que el tema venga de módulos de Go significa que **el build necesita Go
instalado**. Sin Go, Hugo no puede resolver el tema y falla antes de renderizar.

## Contrato de build

```bash
npm ci --omit=dev
hugo --gc --minify
```

Definido en `netlify.toml`. `publish = "public"`.

- **Producción no lleva `-b`.** El `baseURL` sale de `config/_default/hugo.yaml`
  y es la única fuente de verdad. Pasar `-b $URL` haría que las URLs dependieran
  de una variable de Netlify y que un build local produjera un resultado
  distinto.
- **Las previsualizaciones sí llevan `-b $DEPLOY_PRIME_URL`**, o los enlaces
  internos apuntarían a producción.
- `--omit=dev` excluye `playwright-core`, que solo se usa en local para generar
  el CV. No lo instales en el build.

## Despliegue

| | |
|---|---|
| Proyecto Netlify | `oscar-zambrano` |
| Rama de producción | `master` |
| Dominio primario | `www.oscarzambrano.name` (Netlify DNS) |
| Ápex | `oscarzambrano.name` → redirige al primario |
| Funciones | ninguna — ni serverless, ni edge |

## Restricciones — romper cualquiera de estas rompe el sitio

1. **El `baseURL` debe ser el dominio propio y absoluto.** De ahí salen los
   canonical, el `sitemap.xml` y las etiquetas Open Graph. Si apunta a un
   `*.netlify.app`, le estás diciendo a Google que el sitio canónico es otro.
   Ya pasó una vez.

2. **`defaultContentLanguage` debe existir en `config/_default/languages.yaml`.**
   Si no, Hugo aborta el build entero con
   `config value "es" for defaultContentLanguage does not match any language definition`.
   El sitio es monolingüe: no declares un idioma sin contenido traducido, o
   generarás rutas vacías anunciando `hreflang` de algo que no existe.

3. **No añadas recursos externos.** La `Content-Security-Policy` de
   `netlify.toml` es `default-src 'self'`, y es viable justamente porque hoy el
   sitio no carga nada de fuera: el CSS y el JS son propios y con hashes SRI.
   Una fuente de Google, un script de analítica o un iframe **serán bloqueados
   por el navegador**, y no lo verás en el build: lo verá el visitante, en
   silencio, en la consola. Si de verdad hace falta un recurso externo, hay que
   actualizar la CSP en el mismo cambio y volver a verificarla.

4. **No actives prerenderizado.** Es una función para SPAs renderizadas en
   cliente: intercepta a los bots y les sirve una instantánea cacheada. Este
   sitio es estático, los crawlers ya reciben el HTML completo, y el
   prerenderizado solo introduce contenido obsoleto. Netlify lo tiene además
   marcado como obsoleto.

5. **No versiones `public/`.** Está en `.gitignore`. Netlify lo construye en
   cada deploy. El repositorio ya arrastró 6 MB de salida de build desfasada.

6. **No cambies el correo ni el LinkedIn sin confirmación de Oscar.** Una versión
   anterior de este sitio publicó una dirección y un perfil que no existen. Los
   correctos son `oscar.zambrano.cl@gmail.com` y
   `linkedin.com/in/oscarzambranoparra`.

7. **No inventes datos de CV.** Cargos, fechas y logros vienen de
   `docs/HANDOFF.md` §1.3 y §1.5. Si falta un dato, se pregunta.

8. **Añadir funciones o formularios cambia el modelo de seguridad.** Hoy la
   superficie de ataque es prácticamente nula porque no hay código ejecutándose
   en servidor. Si introduces una función, revisa CSP, cabeceras y validación de
   entrada en el mismo cambio.

## Dónde está cada cosa

| Qué | Archivo |
|---|---|
| Perfil, cargos, formación, capacidades, premios | `content/authors/admin/_index.md` |
| Portada y sus secciones | `content/_index.md` |
| Página de trayectoria | `content/experiencia.md` |
| `baseURL`, idioma, taxonomías | `config/_default/hugo.yaml` |
| Marca, SEO, navbar, pie | `config/_default/params.yaml` |
| Menú | `config/_default/menus.yaml` |
| Traducciones que faltan en el tema | `i18n/es.yaml` |
| Imagen de compartir (Open Graph, 1200×630) | `assets/media/sharing.png` |
| Favicon | `assets/media/icon.png` |
| CV en PDF | `static/cv/oscar-zambrano-cv.pdf` |
| Plantilla y generador del CV | `tools/cv/` |
| Build, redirecciones y cabeceras | `netlify.toml` |

## Trampas conocidas

- **`date_format` usa el layout de referencia de Go** (`2006`, `January 2006`).
  Escribir `'enero 2006'` imprime la palabra literal, no un mes traducido. Hugo
  localiza los nombres de mes solo, vía `time.Format`.
- **El bloque `markdown` ignora `subtitle`.** Lo que pongas ahí no se renderiza;
  llévalo al cuerpo del texto.
- **El tema no trae la clave `experience` en español.** Está suplida en
  `i18n/es.yaml`. Si aparece otro encabezado en inglés, añádelo ahí en lugar de
  copiar el partial entero.
- **Sin barras de porcentaje en las capacidades.** Decisión editorial: no
  comunican nada verificable.

## El CV en PDF

Se genera a mano y **se commitea**, porque el build de Netlify no tiene
navegador:

```bash
npm install --no-save playwright-core
node tools/cv/build-cv.mjs
```

Si cambias el perfil del sitio, **regenera el PDF en el mismo cambio** o quedará
desfasado respecto a lo que el sitio afirma.

## Verificación antes de dar un cambio por bueno

```bash
npm ci --omit=dev && hugo --gc --minify     # debe terminar sin errores ni warnings

grep -rl noindex public/                    # no debe encontrar nada
grep -o 'canonical href=[^ >]*' public/index.html    # dominio propio
grep -o '<loc>[^<]*</loc>' public/sitemap.xml        # URLs absolutas, sin taxonomías vacías
```

Y en el navegador: consola sin errores, sin desborde horizontal a 360 px, y la
consola sin violaciones de CSP.
