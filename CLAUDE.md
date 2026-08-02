# CLAUDE.md

Sitio personal de Oscar Zambrano (oscarzambrano.name). Hugo + Hugo Blox, en
español, desplegado en Netlify. El contexto completo está en
**[`docs/HANDOFF.md`](docs/HANDOFF.md) — léelo antes de tocar nada.**

## Reglas de arranque

1. **No inventes contenido de CV.** Cualquier dato biográfico que no esté en el
   handoff o en el repo se le pregunta a Oscar. La cronología válida está en
   §1.3 del handoff y prevalece sobre cualquier otra fuente.
2. **No toques los datos de contacto sin confirmación.** Una versión anterior de
   este sitio publicó un email y un LinkedIn que no existen. Los correctos son
   `oscar.zambrano.cl@gmail.com` y `/in/oscarzambranoparra`.
3. **No publiques datos internos de la empresa:** sin cifras, clientes, esquemas
   HANA, endpoints BTP, subaccounts ni credenciales. Lo que SAP ya publicó (§1.4
   del handoff) sí es citable — el resto no.
4. Trabaja en rama, commits atómicos, sin force-push a `main`.

## Cómo trabajar en esto

```bash
npm install                 # dependencias de Tailwind
hugo --gc --minify          # build (requiere Hugo EXTENDED 0.152.2+ y Go)
hugo server                 # desarrollo
```

- El tema llega por **módulos de Go** (ver `go.mod`), no por `themes/`. Hace
  falta Go instalado para construir.
- Hugo **extended**: el tema usa SCSS. La edición normal falla.
- `public/` y `resources/` no se versionan. Netlify construye en cada deploy.

## Dónde está cada cosa

| Qué | Dónde |
|---|---|
| Perfil, cargos, formación, capacidades, premios | `content/authors/admin/_index.md` |
| Portada y sus secciones | `content/_index.md` |
| Página de trayectoria | `content/experiencia.md` |
| baseURL, idioma, taxonomías | `config/_default/hugo.yaml` |
| Marca, SEO, navbar, pie | `config/_default/params.yaml` |
| Traducciones que faltan en el tema | `i18n/es.yaml` |
| Imagen de compartir (Open Graph) | `assets/media/sharing.png` |
| Build, redirects y cabeceras | `netlify.toml` |

## Cosas que se rompieron antes y conviene no repetir

- **`baseURL` debe ser el dominio propio.** Si apunta a un `*.netlify.app`, los
  canonical mandan a Google a otro origen.
- **`defaultContentLanguage` debe existir en `languages.yaml`.** Si no, el build
  aborta entero.
- **No declares un idioma sin contenido traducido:** genera rutas vacías con
  `hreflang` de un idioma inexistente.
- **`date_format` usa el layout de Go** (`2006`, `January 2006`). Escribir
  `'enero 2006'` imprime la palabra literal.
- **El bloque `markdown` ignora `subtitle`.** Lo que pongas ahí no se ve.
- **Sin barras de porcentaje en habilidades.** No comunican nada verificable.

## Pendiente

Netlify (proyecto `oscar-zambrano`) todavía construye producción desde la rama
`claude/analyze-repository-01W9PueHh1syph6jLPL8gpFg`. Hay que cambiarlo a
`master` en el dashboard — *Site configuration → Build & deploy → Branches and
deploy contexts* — y solo **después** de mergear, porque el `master` actual es
el sitio de 2019 y no tiene `netlify.toml`. Ver §9 del handoff para el resto.
