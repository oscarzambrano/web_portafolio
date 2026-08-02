# HANDOFF — Rediseño de oscarzambrano.name

> **Estado de este documento.** Redactado por Oscar, corregido el 2026-08-02 contra
> el repositorio y contra las APIs de Netlify y GitHub. Las secciones marcadas
> ⚠️ **CORREGIDO** contradicen el borrador original: léelas antes que nada.
>
> Cada afirmación lleva su nivel de evidencia:
>
> | Etiqueta | Significado |
> |---|---|
> | ✅ **VERIFICADO** | Confirmado leyendo código o consultando la API. Fiable. |
> | 👁️ **OBSERVADO** | Visto en el sitio en vivo por Oscar; no re-verificable desde el contenedor (la política de red bloquea el host). |
> | 🔶 **HIPÓTESIS** | Explicación razonada y consistente con la evidencia, sin confirmar. |

---

## 0. Reglas de arranque (leer primero)

1. **Audita antes de proponer.** Respeta las etiquetas de evidencia de arriba.
   Corrige este documento antes de escribir código.

2. ⚠️ **CORREGIDO — No inventes contenido de CV, y no descartes el que ya está.**
   El borrador ordenaba descartar el perfil "Estadística / AC Nielsen / sector
   petrolero / PentaHo / tesis de series de tiempo" por pertenecer a otro Oscar
   Zambrano. **Eso es incorrecto** (evidencia en §1.2): ese contenido está firmado
   por la cuenta de Oscar. Regla vigente:
   - Cualquier dato biográfico que no esté en este documento ni en el repo se
     pregunta a Oscar. Sigue prohibido inventar.
   - El contenido 2012-2019 del repo es **historial propio verificado**, y Oscar
     ya autorizó publicar AC Nielsen, Data Conversion Service (Emaresa) y
     Equifax. El resto de esa etapa queda fuera por decisión suya (§1.2).
   - El hueco real es **2019 → 2026** (etapa NS Agro / Martínez y Valdivieso).
     El repo no contiene nada de ese periodo: la cronología confirmada por Oscar
     está en §1.3 y es la única fuente válida para esos años.

3. **No publiques datos de NS Agro.** Sin cifras internas, nombres de clientes,
   esquemas HANA, endpoints BTP, nombres de subaccounts ni credenciales. Métricas
   de impacto solo en términos relativos y aprobadas por Oscar antes de commitear.
   *(Nota: el repo hoy no contiene ningún dato de este tipo. Ver §2.6 para lo que
   sí conviene revisar.)*

4. Trabaja en rama (`redesign/*`), commits atómicos, sin force-push a `main`.

5. ⚠️ **NUEVO — `master` no es lo que está en producción.** Antes de auditar nada,
   lee §1.1. Auditar `master` es auditar código muerto.

---

## 1. Estado real del proyecto

### 1.1 ⚠️ CORREGIDO — Hay tres estados distintos, no uno

✅ **VERIFICADO** (API de Netlify + API de GitHub, 2026-08-02):

| # | Estado | Qué es |
|---|---|---|
| A | `master`, head `e61a20a` (2019-03-11) | Hugo + blogdown, tema `hugo-academic` vendorizado. **No es lo que se publica.** |
| B | `claude/analyze-repository-01W9Pue…`, commit `3b94444` | **Lo que está en producción ahora.** Hugo Academic + `netlify.toml`, con el CV ya actualizado a NS Agro. |
| C | La misma rama, head `49315c53` | Migración a **Hugo Blox** ya hecha y **nunca desplegada**. |

Detalle del proyecto Netlify:

- Proyecto: **`warden-cat-68477`** — *no existe ningún proyecto llamado
  `oscar-zambrano`*. URL primaria `https://www.oscarzambrano.name`.
- Sin protección por password ni SSO (`requiresPassword: false`).
- Deploy activo `692ce34c…`, `state: ready`, `context: production`, publicado
  **2025-12-01**, construido desde la rama `claude/analyze-repository-…`.
- Build: `hugo --gc --minify`, `publish = "public"`, `HUGO_VERSION = "0.120.4"`.

> **La rama de producción de Netlify es una rama generada por Claude.** Eso es un
> problema de configuración por sí solo: cualquiera que borre esa rama tira el
> sitio. Estabilizarlo es parte del trabajo (§7).

El estado C (Hugo Blox) trae `go.mod`, `hugoblox.yaml` (`hugo_version: 0.152.2`,
template `academic-cv`), `config/_default/{hugo,params,languages,menus,module}.yaml`,
`package.json` y `assets/`. Desaparece `themes/`: el tema pasa a Hugo Modules
(`blox-tailwind`, `blox-plugin-netlify`).

### 1.2 ⚠️ CORREGIDO — Procedencia del CV 2019

✅ **VERIFICADO** (`git log`, `config.toml`):

- 33 commits, un solo autor. Los que escriben el CV —`bc6055e` "Actualizacion
  2019" y `e61a20a` "Cursos"— son de
  `oscarzambrano <oscar.zambrano.cl@gmail.com>`, el email de la cuenta de Oscar.
- El mismo `config.toml` publica su LinkedIn (`oscarzambranoparra`), su GitHub
  (`oscarzambrano`), su teléfono y `© 2019 Oscar Zambrano`.
- La cronología encaja sin costuras con el perfil confirmado en §1.3: Lic.
  Estadística ULA 2014 → pasantía PDVSA → Chile 2016 (Nielsen) → Equifax
  2017-2019 → **NS Agro desde 2019**. El CV del repo termina justo donde
  empieza la etapa actual: es la misma carrera, sin solapamiento ni hueco.

**Conclusión:** no es otro Oscar. El análisis previo no inventó ese perfil: lo
leyó de aquí. El riesgo es el opuesto al que suponía el borrador — no hay un CV
falso, hay **un hueco de ~7 años**.

**Acción:** ✅ **RESUELTO el 2026-08-02.** Oscar confirmó que el historial es
suyo y autorizó publicar tres etapas: **AC Nielsen, Data Conversion Service
(Emaresa) y Equifax**. Ya están en el sitio y en el CV.

Quedan **fuera por decisión editorial** (no las añadas sin pedírselo): Comercial
"El Punto Solidario", la pasantía en Petróleos de Venezuela y la preparaduría en
la Escuela de Estadística de la ULA.

### 1.3 Perfil del propietario (confirmado por Oscar)

**Nombre de la empresa — importante.** Desde **2026**, NS Agro pasa a llamarse
**Martínez y Valdivieso** (myv.cl). Holding agrícola chileno-peruano.

- En el sitio, el empleador **actual** se nombra **Martínez y Valdivieso**.
- Los cargos de **2019 a 2025** se ejercieron bajo el nombre **NS Agro**; al
  citarlos, usar ese nombre y aclarar la continuidad (p. ej. "NS Agro, hoy
  Martínez y Valdivieso"). No reescribas la historia con el nombre nuevo.

**Trayectoria (confirmada por Oscar 2026-08-02):**

| Desde | Cargo | Empresa |
|---|---|---|
| 2019 | **Data Scientist** | NS Agro |
| 2020 | **Jefatura de Data Analytics y Data Science** (como departamento) | NS Agro |
| 2024 | **Subgerente de Data Analytics e IA** | NS Agro → Martínez y Valdivieso (2026) |

> ⚠️ Esto **corrige** el borrador original, que situaba el paso a Subgerente en
> ~junio 2026 y hablaba de "~6 años". Son **7 años** de trayectoria continua
> (2019→2026), con **~4 años en la Jefatura** (2020-2024) y el ascenso a
> Subgerente en **2024**. Prevalece esta tabla sobre cualquier otra fuente,
> incluida la rama sin desplegar (§2.6).

- Lidera un equipo de **2 personas** desde su rol de Jefatura.
- Base: Chile.
- Stack: SAP BTP Cloud Foundry, SAP HANA, SAP Business Data Cloud, SAP Fiori/UI5,
  Machine Learning, LLMs, Python, R, SQL.
- Credencial pública destacable: la empresa ganó el **SAP Innovation Tournament
  en SAP NOW Chile (septiembre 2024)** con una solución de IA generativa.
  Fuentes verificadas y matiz sobre el rol: **§1.4**.

**Vacíos a llenar con Oscar:** certificaciones SAP vigentes, idiomas
actualizados, y qué proyectos puede mostrar públicamente.
*(Formación académica en §1.5; años por cargo ya resueltos arriba.)*

### 1.4 Fuentes públicas verificadas (2026-08-02)

✅ **VERIFICADO por búsqueda web.** Estas son las referencias que el sitio puede
enlazar como prueba social. Todas resuelven y hablan de Oscar o de su trabajo.

**Referencia 1 — Torneo de Innovación, SAP NOW Chile (septiembre 2024)**

- SAP News Latinoamérica —
  `news.sap.com/latinamerica/2024/09/ns-agro-gana-torneo-innovacion-en-sap-now-chile/`
- Medios chilenos: Cooperativa, Tekios, La Quinta Emprende, Gerencia,
  ITSitio Chile, Portal Innova, TecNautas.

Hechos publicados: NS Agro ganó la final frente a **Arauco**; formato
*reverse shark-tank* con jurado de startups (Synaptic, WooCar, CryptoMate);
ganó por el componente *no-code/low-code*; pasó a la fase regional junto a
México, Brasil, Colombia y Argentina. La solución optimizaba precios.

> ⚠️ **La fuente de SAP lo nombra "Óscar Zambrano, data engineer en NS Agro"** y
> lo cita diciendo que lo más difícil fue *entender el problema que se les
> planteaba*. Oscar confirma que su rol real en ese equipo fue **científico de
> datos y especialista en IA**. El sitio usa el rol real y no reproduce la
> etiqueta de la fuente; si alguien abre el enlace verá "data engineer". Es una
> discrepancia conocida y aceptada, no un error a corregir.

**Referencia 2 — SAP HANA Cloud vector engine (M&V, 2025)**

- SAP, caso de cliente —
  `sap.com/assetdetail/2025/06/54beee34-187f-0010-bca6-c68f7e60039b.html`
- SAP, "Delivering timely customer quotes while improving profitability" —
  `sap.com/asset/dynamic/2025/08/b83db80d-1a7f-0010-bca6-c68f7e60039b.html`
  → **nombra a Oscar Zambrano como Chief of Data Analytics de M&V.**
- SAP News Latinoamérica —
  `news.sap.com/latinamerica/2025/01/ns-agro-lidera-transformacion-digital-de-martinez-y-valdivieso-con-sap-en-ia/`
- Medios: Cooperativa, Portal Agro Chile, Portal Innova, BNamericas,
  The Standard CIO, InnovaciónDigital360.

Hechos publicados: más del 95 % de la fuerza de venta de M&V opera en terreno;
el vendedor manda texto o audio; un bot transcribe; un modelo de ML en SAP BTP
arma la cotización usando el *vector engine* de SAP HANA Cloud; el precio se
calcula por cliente según pedido, historial y clasificación crediticia; el
equipo interno entrena el modelo con las librerías de ML embebidas en HANA,
accesibles desde R y Python. Operación en Chile y Perú.

> **Consecuencia para la regla 3.** Este proyecto **sí es publicable**: lo
> publicó SAP. La prohibición de datos internos sigue vigente para todo lo que
> no esté en estas fuentes — cifras, clientes, esquemas, endpoints, subaccounts.

**Corrección de una URL inventada.** La rama sin desplegar citaba
`news.sap.com/latinamerica/2025/01/ns-agro-lidera-innovacion-agricola/`, que no
existe. El hecho era real; el enlace, no. Sustituido por el correcto.

### 1.5 Trayectoria previa recuperable del repo (2012-2019)

✅ **VERIFICADO** — está en `content/` de `master`. Pendiente de confirmación
editorial de Oscar antes de publicarse.

- **Licenciado en Estadística**, Universidad de Los Andes, Mérida, Venezuela
  (2014). Título legalizado ante el Ministerio de Relaciones Exteriores de Chile.
- *Tesis*: modelos de series de tiempo aplicados a tasas de producción de
  petróleo (campos El Carito – Mulata, Monagas).
- **Equifax Chile** — Analista de Datos, Datos & Marketing Services (marzo 2017 –
  2019). Automatización de procesos, apps en Shiny R, dashboards operacionales.
- **Data Conversion Service S.A.** — Analista Estadístico (oct 2016 – mar 2017).
- **AC Nielsen Chile** — Estadístico Jr., Behavioral Methods (ene – sep 2016).
- **Petróleos de Venezuela S.A.** — pasante, Estudios Integrados de Yacimientos
  (feb – sep 2012).
- **Escuela de Estadística, ULA** — Preparador de Cátedra de Computación
  (2009-2011).
- Cursos: PM ONE (Equifax 2018), Analista BI en Pentaho (Kibernum 2018), Yellow
  Belt Lean (2018), Querying MS SQL Server (Sonda 2017).

Esto es **la única historia larga que el sitio tiene hoy**. Si el rediseño la
descarta, el sitio queda con 7 años de carrera y nada antes. Decisión de Oscar.

---

## 2. Hallazgos ⚠️ CORREGIDO

### 2.1 Tabla revisada

| # | Hallazgo | Evidencia | Causa raíz | Prioridad |
|---|---|---|---|---|
| 1 | El sitio emite `noindex` | 👁️ OBSERVADO | 🔶 Stub de alias de idioma en `/` (ver §2.2). **No es una variable de entorno de preview** | **P0** |
| 2 | ~~HTML sin contenido → CSR~~ **Diagnóstico incorrecto** | ✅ VERIFICADO | **No hay renderizado en cliente.** Hugo es SSG puro. Lo que se sirvió en `/` es el stub de alias (§2.2) | **P0** |
| 3 | Canonical apunta a `oscar-zambrano.netlify.app` | ✅ VERIFICADO | `baseurl` literal en `config.toml:1` del commit desplegado (§2.3) | **P1** |
| 4 | `oscar-zambrano.netlify.app/es/` da 404 | ✅ VERIFICADO | Ese subdominio **no es de este proyecto** (§2.3) | **P1** |
| 5 | Verificar HTTPS forzado y HSTS | 🔶 HIPÓTESIS | El `netlify.toml` desplegado no define `Strict-Transport-Security` | **P1** |
| 6 | 🆕 La rama de producción de Netlify es `claude/*` | ✅ VERIFICADO | Configuración del dashboard (§1.1) | **P1** |
| 7 | 🆕 Migración a Hugo Blox terminada y sin desplegar | ✅ VERIFICADO | §1.1 estado C | **P1** |
| 8 | 🆕 Contenido demo del tema vivo en el sitio | ✅ VERIFICADO | §2.4 | **P2** |
| 9 | 🆕 Habilidades solo como imágenes | ✅ VERIFICADO | §2.5 | **P2** |
| 10 | 🆕 `public/` commiteado, stale y contradictorio | ✅ VERIFICADO | §2.5 | **P2** |
| 11 | 🆕 **La rama sin desplegar tiene email y LinkedIn equivocados** | ✅ VERIFICADO | §2.6 | **P0** |
| 12 | 🆕 **La rama sin desplegar no compila** | ✅ VERIFICADO | §2.6 | **P0** |
| 13 | 🆕 Fechas de cargos inventadas en la rama sin desplegar | ✅ VERIFICADO | §2.6 | **P0** |
| 14 | 🆕 La rama sin desplegar es la plantilla demo de Hugo Blox | ✅ VERIFICADO | §2.6 | **P1** |

### 2.2 Hallazgos 1 y 2: una sola causa, y no es CSR

✅ **VERIFICADO — no existe ningún `noindex` de sitio en ninguna base de código:**

- En `master`, los 38 `noindex` son stubs de paginación de Hugo (`…/page/1/`).
  Es comportamiento **correcto y deseable**, no el problema.
- El `netlify.toml` desplegado define 6 reglas de headers (`X-Frame-Options`,
  `X-XSS-Protection`, `X-Content-Type-Options`, `Referrer-Policy` y caché) y
  **ningún `X-Robots-Tag`**.
- El proyecto no tiene protección por password.

🔶 **HIPÓTESIS (alta confianza).** El commit desplegado tiene
`defaultContentLanguageInSubdir = true` y no fija `disableAliases`. Con Hugo
0.120.4 el contenido se emite bajo `/es/` y la raíz `/` queda como **stub de
alias**, cuyo markup generado es exactamente:

```html
<!DOCTYPE html><html><head><title>/es/</title>
<link rel="canonical" href="…/es/"/>
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url=/es/"></head></html>
```

~200 bytes, sin contenido. **Eso explica los dos hallazgos a la vez**: el
`noindex` y el "HTML prácticamente sin contenido". No hay CSR en ninguna parte —
ni bundle de hidratación, ni router, ni fetch de datos; el JS es progressive
enhancement (jQuery/Bootstrap/isotope).

**Primer paso de la auditoría — cierra esto antes que nada:**

```bash
curl -sI  https://www.oscarzambrano.name/          # ¿302/200? ¿X-Robots-Tag?
curl -s   https://www.oscarzambrano.name/    | head -40   # ¿stub de alias?
curl -s   https://www.oscarzambrano.name/es/ | wc -c      # ¿contenido completo?
curl -sI  https://www.oscarzambrano.name/es/ | grep -i robots
```

Si `/es/` devuelve el sitio completo y `/` devuelve el stub, la hipótesis queda
confirmada y **el arreglo es de configuración, no de arquitectura**.

> No pude ejecutar estos comandos: la política de red de este entorno bloquea el
> host (403 en el CONNECT del proxy). Ejecútalos tú.

### 2.3 Hallazgos 3 y 4: verificado en código, y peor de lo pensado

✅ **VERIFICADO.** Primera línea de `config.toml` en el commit desplegado
(`3b94444`):

```toml
baseurl = "https://oscar-zambrano.netlify.app/"  # Actualizar con dominio final
```

El comentario delata un TODO que nunca se cerró. Y `oscar-zambrano.netlify.app`
**no es el subdominio de este proyecto** — el de verdad es
`warden-cat-68477.netlify.app`. Por eso da 404 accedido directo.

Es decir: el canonical **no divide la señal SEO entre dos dominios propios; apunta
a un origen ajeno o inexistente**, que es estrictamente peor. Arreglo: `baseURL`
al dominio propio.

En `master` el defecto es distinto y también grave: `baseurl = "/"` (desde
`91082cb`, 2017-10-14, que reemplazó `oscarzambrano.name/` en vez de corregirle
el esquema). Consecuencias: todo canonical relativo, `<loc>` de sitemaps sin
dominio (inválido) y 404 emitiendo `<link rel="canonical" href="">`.

En el estado C (Hugo Blox, sin desplegar) `config/_default/hugo.yaml` **sigue
teniendo** `baseURL: 'https://oscar-zambrano.netlify.app/'`. Corrígelo también
ahí, o el bug viaja con la migración.

### 2.4 🆕 Contenido demo del tema, vivo

✅ **VERIFICADO.** El `exampleSite` de `hugo-academic` quedó dentro del build:
publicaciones falsas (`person-re-identification`, `clothing-search`), un proyecto
demo "Deep Learning" y páginas huérfanas de R Markdown (`nuevas.knit`,
`nuevas.utf8`, `nuevo`) con boilerplate `summary(cars)`. Están **publicadas**.

### 2.5 🆕 Deuda de contenido y build

✅ **VERIFICADO:**

- **Habilidades solo como píxeles.** Los niveles por herramienta (R, Python, SQL,
  Spark, Hive, Impala, Pentaho, SPSS Modeler, SAS…), las técnicas y los idiomas
  existen únicamente dentro de `Herramientas.jpeg`, `Tecnica.png` e `Idioma.png`.
  No son indexables, ni accesibles, ni actualizables. Hay que re-autorarlos como
  datos estructurados.
- **`public/` commiteado (6,1 MB) e inconsistente:** raíz construida con Hugo
  0.54.0 (2019); `/es/` y `/en/` con 0.30.2 (2017). Se contradicen entre sí:
  fechas de Equifax distintas, un rango imposible *"Octubre de 2016 – Marzo
  2016"*, y el typo **"Oscarx cuenta con experiencia…"** vivo en `/es/` y `/en/`.
- **`/en/` es un locale fantasma:** `[Languages.en]` se eliminó de la config en
  2017, pero `public/en/` sigue publicado y anunciando `hreflang="en"`. No existe
  ni un solo archivo de contenido traducido (`*.en.md`) en el repo.
- **Avatar roto en cualquier rebuild de `master`:** `avatar = "Picture.jpg"` pero
  `static/img/Picture.jpg` no existe (solo está en `public/img/`).
- **Sin OG, sin Twitter Card, sin JSON-LD, sin `robots.txt`** en `master`.
  `head_custom.html` —el punto de inyección del tema— está vacío (0 bytes), así
  que añadirlos es un drop-in, no una reescritura de plantillas.
- `fonts/` (1,7 MB) no lo lee Hugo: peso muerto.

### 2.6 🆕 La rama sin desplegar NO es publicable como está

✅ **VERIFICADO** construyendo el commit `49315c5` con Hugo Extended 0.152.2
(2026-08-02). El commit del mensaje *"Migración completa: Hugo Academic → Hugo
Blox"* es, en realidad, **la plantilla `academic-cv` de Hugo Blox con algunos
datos encima** — y varios de esos datos son incorrectos.

**a) No compila.** Hugo la rechaza antes de renderizar:

```
Error: failed to decode "languages": config value "es" for
defaultContentLanguage does not match any language definition
```

`config/_default/hugo.yaml` declara `defaultContentLanguage: es`, pero
`config/_default/languages.yaml` **solo define `en`**. Hay que definir `es` (o
cambiar el idioma por defecto) antes de que la rama pueda desplegarse.

**b) Datos de contacto equivocados — P0.** En
`content/authors/admin/_index.md`:

| Campo | En la rama | Correcto (§1.3, `master`) |
|---|---|---|
| Email | `oscarzambranoa@gmail.com` | `oscar.zambrano.cl@gmail.com` |
| LinkedIn | `linkedin.com/in/oscarzambranoa` | `linkedin.com/in/oscarzambranoparra` |

Un portafolio con el contacto equivocado es peor que no tener portafolio.
**Corrige esto antes que cualquier otra cosa.**

**c) Fechas de cargos inventadas.** La rama afirma Subgerente desde **enero
2022**, "Jefe de Ciencia de Datos" 2020-2021 y Data Scientist solo durante 2019.
Contrástalo con la tabla confirmada en §1.3: la Jefatura empieza en **2020** y
**no termina en 2021** —se extiende hasta 2024—, el cargo se llama **Jefatura de
Data Analytics y Data Science**, y el paso a Subgerente es de **2024**, no de
2022. La titulación aparece fechada 2010-2015; `master` dice 2014. La bio abre
con **"más de 10 años de experiencia"**, sin respaldo.

> Ojo: el único dato que la rama acierta es el año de inicio (2019). Todo lo
> demás está corrido. No la uses como fuente para el timeline.

**d) Otros problemas de contenido:**

- Barras de porcentaje en habilidades (95 %, 90 %, **Machine Learning 100 %**),
  justo lo que prohíbe §5. `experience.md` las oculta, pero los datos siguen ahí.
- Premio *"SAP HANA Vector Engine Early Adopter"* citando
  `news.sap.com/latinamerica/2025/01/ns-agro-lidera-innovacion-agricola/`.
  **Verificar que esa URL exista** antes de publicarla.
- El botón "Descargar CV" apunta al Google Drive de 2019, es decir, al CV de
  Estadística. El sitio prometería un perfil SAP y entregaría el CV antiguo.
- Foto de perfil: `yo.png`, la foto casual en la nieve. No es un retrato
  profesional.
- Menú **en inglés** (Bio, Papers, Talks, News, Experience, Projects, Courses)
  sobre un sitio en español; "Papers", "Talks" y "News" apuntan a anclas
  inexistentes.
- `content/` conserva **todo el contenido demo de Hugo Blox**: posts
  (`get-started`, `second-brain`, `teach-courses`…), un curso completo sobre
  Hugo Blox, publicaciones falsas (`conference-paper`, `journal-article`,
  `preprint`), proyectos `pandas`/`pytorch`/`scikit` y un evento de ejemplo.
  Además, esos posts **rompen el build** al intentar descargar imágenes remotas
  de Unsplash y HuggingFace.

**e) El diseño sí sirve.** Una vez corregido el idioma y quitado el contenido
demo, la plantilla renderiza bien: limpia, moderna, con dark mode, selector de
tema y conmutador de idioma. **Recomendación: conservar el tema, rehacer el
contenido.**

> ⚠️ **Riesgo activo:** esta es la misma rama que Netlify tiene configurada como
> producción. El commit publicado es anterior a la migración, así que en vivo se
> ve la versión Academic — pero **cualquier deploy nuevo de esta rama publicaría
> el email y el LinkedIn equivocados**. Estabilizar la rama de producción
> (hallazgo #6) es urgente por este motivo, no solo por higiene.

### 2.7 🆕 Revisar antes de republicar

No hay cifras internas ni datos de NS Agro en el repo. Pero conviene el criterio
de Oscar sobre:

- **Cliente nombrado de un empleador anterior:** *"Proyecto para EMARESA S.A"* y
  su herramienta interna *RastPro* (entrada de Data Conversion Service).
- **Equipo y mandato internos de Nielsen:** *"Behavioral Methods"* y *"evaluar el
  riesgo de sesgo en la muestra…"*.
- **PDVSA:** *"estimar las reservas remanentes"* sobre campos nombrados. Sin
  cifras, y la tesis es académica/pública, lo que lo atenúa.
- **PII:** teléfono personal en texto plano con `autolink = true`.
- **CV en Google Drive:** el enlace de Word es una URL `/edit`. Verificar los
  permisos de compartición.
- Enlace muerto a Google+ (servicio cerrado en 2019) en `master`.

---

## 3. Fase 0 — Auditoría ⚠️ CORREGIDO

El borrador daba comandos de un proyecto npm. **Este proyecto no tiene Node ni
`package.json` en `master`**; es Hugo. Comandos reales:

```bash
# 0. Cerrar primero el diagnóstico del noindex — ver §2.2
curl -sI https://www.oscarzambrano.name/ && curl -sI https://www.oscarzambrano.name/es/

# 1. Situarse en lo que SÍ está desplegado
git fetch origin
git log --oneline -20 origin/claude/analyze-repository-01W9PueHh1syph6jLPL8gpFg
git diff --stat 3b94444 origin/claude/analyze-repository-01W9PueHh1syph6jLPL8gpFg

# 2. Inventario del stack real
cat netlify.toml
cat hugoblox.yaml go.mod package.json      # solo en el estado C
ls config/_default/                         # estado C
cat config.toml                             # estados A y B

# 3. ¿Buildea?
hugo version
hugo --gc --minify --environment production
hugo --printPathWarnings --printUnusedTemplates

# 4. SEO / render
grep -rn "robots\|noindex" --include="*.html" --include="*.toml" --include="*.yaml" \
  . | grep -v node_modules | grep -v "page/1"
grep -rn "baseurl\|baseURL" config.toml config/ netlify.toml
```

Entregar un **informe de auditoría** (no código todavía) con:

- Confirmación o refutación de la hipótesis de §2.2, con el output de `curl`.
- Los tres estados de §1.1: qué tiene cada uno y cuál conviene como línea base.
- Estado del build en cada uno, con errores y warnings.
- Lighthouse en las 4 categorías, mobile y desktop, contra producción.
- Inventario del contenido existente (§1.4) para no reescribir lo que sirve.
- Estado responsive real: 360px, 768px, 1440px.
- Accesibilidad: contraste, jerarquía de headings, alt, foco visible, teclado.
- Diagnóstico de los 10 hallazgos de §2.1.

---

## 4. Fase 1 — Decisiones a confirmar con Oscar ⚠️ CORREGIDO

1. ⚠️ **La pregunta no es "¿refactor o rewrite?" sino "¿qué se hace con la
   migración a Hugo Blox que ya existe y no está desplegada?"** (§1.1 estado C).
   **Recomendación escrita: terminarla y desplegarla.** Es SSG, está mantenida,
   resuelve render y SEO de raíz, y el trabajo está hecho a medias — descartarla
   es tirar trabajo y volver a un tema de 2017 abandonado. Pero antes hay que
   comprobar que buildea y que su contenido es correcto. Decisión de Oscar.
2. **Estabilizar la rama de producción de Netlify** (§2.1 #6). Apuntarla a `main`
   o a una rama estable, no a `claude/*`.
3. **Audiencia primaria:** ¿headhunters/roles ejecutivos, red SAP/AgTech, o
   consultoría? Define el copy y el CTA.
4. **¿Bilingüe ES/EN?** Ojo: hoy **no existe contenido traducido**, solo rutas.
   El estado C ya puso `defaultContentLanguageInSubdir: false`. Decidir si se
   completa EN o se elimina el andamiaje i18n.
5. **¿Qué se hace con la etapa 2012-2019?** (§1.4). Es la única historia larga
   que hay.
6. **¿Blog técnico?** Solo si Oscar se compromete a un ritmo sostenible. Un blog
   con dos posts de hace un año resta. *(Hoy `content/post/` está vacío y aun así
   renderiza un encabezado "Mis Notas" vacío.)*
7. **Demos interactivas:** ¿hay algo mostrable sin exponer datos de NS Agro?
   Alternativa: datasets sintéticos o públicos (ODEPA, INIA, Banco Mundial).

---

## 5. Fase 2 — Arquitectura de contenido propuesta

Sujeta a la decisión de audiencia. Estructura base:

- **Hero** — nombre, cargo, una línea de propuesta de valor, foto profesional,
  CTA (contacto + CV en PDF). Sin jerga vacía.
- **Perfil** — 3-4 párrafos: qué problema resuelve, en qué industria, con qué stack.
- **Experiencia** — timeline con la progresión en NS Agro. El paso a Subgerente
  es la señal más fuerte del CV: que se lea.
- **Capacidades técnicas** — agrupadas: Plataforma SAP / Data & ML / Desarrollo.
  Sin barras de porcentaje (nadie las cree). ⚠️ **Como datos estructurados en
  Markdown o YAML, no como imágenes** (§2.5).
- **Proyectos** — 3-4 casos con formato problema → enfoque → tecnologías →
  resultado. Resultado en términos relativos si el absoluto es confidencial.
- **Reconocimientos** — SAP Innovation Tournament 2024, con link a la fuente.
- **Contacto** — email, LinkedIn, GitHub. Formulario solo si hay backend real.

---

## 6. Fase 3 — Requisitos no funcionales

- **Render:** SSG. El contenido debe estar en el HTML inicial. *(Ya se cumple; lo
  que falla es que `/` sirva un stub — §2.2.)*
- **URLs:** ⚠️ `baseURL` al **dominio propio** en producción. Nunca un
  `*.netlify.app`. Revisar `config.toml` y `config/_default/hugo.yaml`.
- **Routing de idioma:** decidir explícitamente `defaultContentLanguageInSubdir`
  y, si queda `true`, gestionar la raíz con un redirect real (301 en
  `netlify.toml`), no con un stub de alias con `noindex`.
- **SEO:** `index,follow` en producción; canonical al dominio propio;
  Open Graph + Twitter Card (crítico para compartir en LinkedIn); JSON-LD
  `Person` + `sitemap.xml` con URLs absolutas + `robots.txt`.
- **Performance:** Lighthouse ≥90 en las 4 categorías, mobile. LCP <2.5s.
  Imágenes en AVIF/WebP con dimensiones explícitas.
- **A11y:** WCAG 2.1 AA. Contraste ≥4.5:1, navegación completa por teclado,
  `prefers-reduced-motion` respetado.
- **Responsive:** mobile-first real, probado en 360px.
- **Seguridad:** mantener los headers que ya existen y **añadir HSTS**.
- **Deploy:** Netlify, preview por PR, desde una rama estable. `noindex` SOLO en
  deploy-preview y branch-deploy — nunca en production.
- **Repo:** dejar de versionar `public/` (añadirlo a `.gitignore`) y eliminar el
  `exampleSite` del tema del build.

---

## 7. Definition of Done

- [ ] `curl -sI https://www.oscarzambrano.name/` no devuelve `X-Robots-Tag`, y el
      HTML de `/` no contiene `<meta name="robots" content="noindex">`
- [ ] `/` sirve contenido real, no un stub de alias con meta-refresh
- [ ] El contenido principal es visible con JS deshabilitado
- [ ] Canonical apunta al dominio propio en todas las rutas; ningún
      `*.netlify.app` en `baseURL`
- [ ] `sitemap.xml` con URLs absolutas
- [ ] Preview correcto en el validador de LinkedIn Post Inspector
- [ ] Lighthouse ≥90 × 4, mobile, en producción
- [ ] Sin errores de consola
- [ ] La rama de producción de Netlify es una rama estable, no `claude/*`
- [ ] El `exampleSite` del tema y las páginas huérfanas ya no se publican
- [ ] Sin datos internos de NS Agro en el repo ni en el bundle
- [ ] CV en PDF descargable y sincronizado con el contenido del sitio
- [ ] `sitemap.xml` enviado a Google Search Console

---

## 8. Preguntas abiertas para Oscar

1. ⚠️ **El CV de 2019 del repo (Estadística ULA, PDVSA, Nielsen, Equifax) está
   firmado por tu cuenta y parece tu trayectoria real (§1.2). ¿Lo confirmas? Y si
   es tuyo, ¿quieres mostrarlo en el sitio nuevo o dejarlo fuera?**
2. ⚠️ **¿Terminamos y desplegamos la migración a Hugo Blox que quedó a medias, o
   la descartamos?** (§1.1 estado C, §4.1)
3. ¿Certificaciones SAP vigentes? *(Los años por cargo ya están resueltos —
   ver la tabla de §1.3.)*
   - ¿El cambio de nombre a Martínez y Valdivieso es un rebrand del holding
     completo o solo de la filial operativa? Define cómo se nombra la empresa
     en el hero y en el timeline.
4. ¿Qué proyectos de NS Agro son mostrables públicamente y con qué nivel de detalle?
5. ¿Objetivo real del sitio: buscar oportunidades, o presencia profesional estable?
6. ¿Existe foto profesional o hay que producirla? *(La actual es una foto de
   teléfono de 2015, 300×300.)*
7. ¿Mantener el teléfono personal publicado en el sitio?
8. ¿Quién mantiene el sitio después? Define cuánta complejidad tolera el proyecto.

---

## 9. Estado del rediseño — qué ya está hecho

✅ Aplicado en la rama `claude/oscarzambrano-handoff-audit-s1qu9p` el 2026-08-02.
Se trajo aquí la migración a Hugo Blox (§1.1 estado C) y se corrigió. **Build
verificado localmente con Hugo Extended 0.152.2: limpio, sin errores ni
warnings.**

### Correcciones de fondo

| Qué | Antes | Ahora |
|---|---|---|
| Email | `oscarzambranoa@gmail.com` (no existe) | `oscar.zambrano.cl@gmail.com` |
| LinkedIn | `/in/oscarzambranoa` (no existe) | `/in/oscarzambranoparra` |
| Build | Abortaba: `defaultContentLanguage: es` sin idioma `es` | Compila |
| `baseURL` | `oscar-zambrano.netlify.app` | `www.oscarzambrano.name` |
| Cronología | Subgerente 2022, Jefatura 2020-2021 | 2019 / 2020 / 2024 (§1.3) |
| Bio | "más de 10 años de experiencia" | Redactada sobre hechos verificables |
| URL del premio | `.../ns-agro-lidera-innovacion-agricola/` (inexistente) | Fuentes reales (§1.4) |
| Botón CV | Apuntaba al PDF de Estadística de 2019 | Retirado hasta tener CV vigente |
| Contenido | Plantilla demo de Hugo Blox completa | Solo contenido de Oscar |
| Habilidades | Barras de 95 % / 100 % | Agrupadas, sin porcentajes |
| Idioma | Menú en inglés, locale `en` fantasma | Todo en español, solo `es` |

### Mejoras de diseño y SEO

- **Foto**: se reemplazó la casual en la nieve por el retrato con traje
  (recortado a 800×800 desde `Pic.jpg`, con relleno desenfocado a los lados).
- **Tarjeta de Open Graph**: `assets/media/sharing.png`, 1200×630, con retrato,
  nombre y cargo. Antes el `og:image` era el favicon.
- **i18n**: `i18n/es.yaml` añade `experience`, que falta en el tema y hacía que
  el encabezado saliera como "Experience".
- **Fechas**: `date_format` era `'enero 2006'`, que no es un layout válido de Go
  e imprimía la palabra literal. Ahora es `'2006'`.
- **Sitemap**: pasó de incluir taxonomías vacías a 2 URLs reales, absolutas.
- **Netlify**: HSTS añadido; 301 desde `/es/*` y `/en/*`; `HUGO_VERSION` 0.120.4
  → 0.152.2; `HUGO_ENV` (obsoleto) → `HUGO_ENVIRONMENT`; producción sin `-b`
  para que el `baseURL` del config sea la única fuente de verdad.
- **Simplificación**: se apagaron el buscador y el selector de paleta (funciones
  de demo; el selector además tiene su etiqueta hardcodeada en inglés). Con eso
  desapareció la dependencia de pagefind en el build.
- **Pie**: decía `© 2026 Martínez y Valdivieso` — atribuía el sitio personal al
  empleador. Ahora `© 2026 Oscar Zambrano`, sin insignia Creative Commons.
- **Repo**: se dejó de versionar `public/` (6,1 MB), y se eliminaron `fonts/`
  (1,7 MB sin uso), `themes/`, `MyCV.Rproj`, `index.Rmd` y las imágenes viejas.
  El árbol de trabajo pasó de ~12 MB a ~250 KB.

### Responsive verificado

Sin desborde horizontal en **360, 390, 768 y 1440 px** (medido con
`scrollWidth` vs `clientWidth`).

### Lo que queda pendiente

1. **Desplegar.** Netlify sigue apuntando a `claude/analyze-repository-…`. Hay
   que mover la rama de producción a una estable y borrar la de Claude.
2. **Foto actual.** La que se usa es de 2015. Es la mejor disponible, no una
   buena foto.
3. ~~CV en PDF vigente.~~ ✅ Hecho: `static/cv/oscar-zambrano-cv.pdf`, generado
   con `node tools/cv/build-cv.mjs` desde `tools/cv/cv.html`. El botón
   "Descargar CV" de la portada apunta ahí. **Si cambias el perfil, regenéralo**
   o el PDF se desfasa del sitio.
4. **Lighthouse** contra producción, una vez desplegado.
5. ~~Etapa 2012-2019.~~ ✅ Publicadas AC Nielsen, Data Conversion Service
   (Emaresa) y Equifax. La trayectoria ya es continua de 2016 a hoy.
6. **Certificaciones SAP e idiomas**: no se publican por falta de datos.
7. **Meses de los cargos en NS Agro**: Oscar dio años (2019, 2020, 2024). El
   sitio y el CV muestran enero como mes de inicio porque el formato de fecha
   exige un mes. **Confirmar con Oscar** si alguno cae en otro mes.
