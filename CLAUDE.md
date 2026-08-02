# CLAUDE.md

El contexto del proyecto está en **[`AGENTS.md`](AGENTS.md)** — stack, contrato
de build, despliegue, restricciones y trampas conocidas. Léelo antes de tocar
nada. No dupliques su contenido aquí: dos documentos con las mismas reglas
acaban contradiciéndose.

El porqué histórico de cada decisión, con el nivel de evidencia de cada
afirmación, está en [`docs/HANDOFF.md`](docs/HANDOFF.md).

## Lo mínimo para no romper nada

1. **No inventes datos de CV.** Cargos, fechas y logros salen de
   `docs/HANDOFF.md` §1.3 y §1.5. Si falta un dato, pregúntale a Oscar.
2. **No toques el correo ni el LinkedIn sin confirmación.** Este sitio ya
   publicó una vez unos que no existen.
3. **No publiques datos internos de la empresa.** Lo que SAP ya publicó (§1.4
   del handoff) sí es citable; el resto no.
4. **Nada de recursos externos** sin actualizar la CSP en el mismo cambio.
5. Trabaja en rama, commits atómicos, sin force-push a `master`.

## Comandos

```bash
npm ci --omit=dev && hugo --gc --minify   # build (Hugo EXTENDED 0.152.2 + Go)
hugo server                                # desarrollo
node tools/cv/build-cv.mjs                 # regenerar el CV en PDF
```
