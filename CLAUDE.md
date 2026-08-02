# CLAUDE.md

Sitio personal de Oscar Zambrano (oscarzambrano.name). El plan de trabajo completo
está en **[`docs/HANDOFF.md`](docs/HANDOFF.md) — léelo antes de tocar nada.**

## Reglas de arranque

1. **Audita antes de proponer.** El handoff etiqueta cada afirmación como
   VERIFICADO / OBSERVADO / HIPÓTESIS. Respeta las etiquetas y corrige el
   documento cuando encuentres algo distinto.
2. **No inventes contenido de CV.** Cualquier dato biográfico que no esté en el
   handoff o en el repo se le pregunta a Oscar. El contenido 2012-2019 del repo
   es historial propio verificado, pero necesita su confirmación explícita antes
   de publicarse.
3. **No publiques datos de NS Agro:** sin cifras internas, clientes, esquemas
   HANA, endpoints BTP, subaccounts ni credenciales. Métricas solo en términos
   relativos y aprobadas por Oscar antes de commitear.
4. Trabaja en rama (`redesign/*`), commits atómicos, sin force-push a `main`.

## Lo que hay que saber antes de auditar

- ⚠️ **`master` NO es lo que está en producción.** El deploy activo de Netlify
  sale de la rama `claude/analyze-repository-01W9PueHh1syph6jLPL8gpFg`
  (commit `3b94444`). Esa misma rama tiene commits posteriores **sin desplegar**
  que ya migraron el sitio a Hugo Blox. Son tres estados distintos: ver §1.1 del
  handoff.
- **El stack es Hugo, no Node.** `master` es Hugo + blogdown con el tema
  `hugo-academic` vendorizado. No hay `package.json` ni `npm run build`.
- **No hay renderizado en cliente.** Hugo es SSG puro. Si `/` se ve vacío, es un
  stub de alias de idioma, no CSR: ver §2.2 del handoff.
- **Proyecto Netlify:** `warden-cat-68477` (no `oscar-zambrano`).

## Prioridades

Por encima de todo el rediseño visual: el `noindex` y el contenido vacío en `/`.
Ambos apuntan a la misma causa de configuración (§2.2) y probablemente se cierran
con un par de líneas. Un portafolio que no se indexa y que se ve vacío al
compartirlo en LinkedIn no cumple su función, por bonito que quede.
