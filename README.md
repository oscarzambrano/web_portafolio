# Portfolio Personal - Oscar Zambrano

[![Netlify Status](https://api.netlify.com/api/v1/badges/[TEMPLATE-BADGE-ID]/deploy-status)](https://app.netlify.com/sites/[TEMPLATE-SITE-NAME]/deploys)

> Sitio web de currículum vitae profesional y portfolio para Oscar Zambrano, Subgerente de Data Analytics e Inteligencia Artificial en NS Agro S.A.

## 🌐 Sitio Web

**URL:** [https://oscar-zambrano.netlify.app](https://oscar-zambrano.netlify.app) _(TEMPLATE: Actualizar con URL final)_

## 📋 Descripción

Portfolio profesional construido con Hugo (generador de sitios estáticos) y el tema Hugo Academic. El sitio presenta:

- **Experiencia profesional** en Data Analytics e IA (NS Agro 2019-presente)
- **Reconocimientos**: Ganador Torneo de Innovación SAP NOW Chile 2024
- **Habilidades técnicas**: SAP BTP, AWS, Machine Learning, IA Generativa
- **Educación y certificaciones**
- **Información de contacto**

## 🏆 Destacados

- **Ganador SAP NOW Chile 2024**: Solución de IA Generativa con arquitectura No-Code/Low-Code
- **Early Adopter SAP HANA Vector Engine**
- **Casos de éxito publicados por SAP** sobre transformación digital en NS Agro
- **Expertise en ecosistema SAP**: BTP Cloud Foundry, HANA Cloud, Data Sphere, Analytics Cloud, AI Core

## 🛠️ Stack Tecnológico

### Framework Principal
- **Hugo**: v0.54.0 (Static Site Generator)
- **Tema**: Hugo Academic (por George Cushen)
- **Integración R**: blogdown para desarrollo en R/RStudio

### Frontend
- HTML5 / CSS3
- Bootstrap 3.3.7
- JavaScript
- Font Awesome 4.7.0
- Academicons 1.8.1

### Deployment
- **Netlify**: CI/CD automático desde GitHub
- **Build**: Hugo con minificación
- **DNS**: Netlify DNS o custom domain

## 📁 Estructura del Proyecto

```
web_portafolio/
├── config.toml                 # Configuración principal de Hugo
├── netlify.toml               # Configuración de deployment Netlify
├── index.Rmd                  # Index para blogdown (R)
├── MyCV.Rproj                 # Proyecto RStudio
│
├── content/                   # Contenido del sitio
│   ├── home/                  # Widgets de la página principal
│   │   ├── resumen.md        # Sobre mí / Intereses
│   │   ├── experiencia.md    # Experiencia laboral
│   │   ├── reconocimientos.md # Premios y reconocimientos
│   │   ├── educacion.md      # Educación y cursos
│   │   ├── projects.md       # Widget de habilidades
│   │   ├── academicas.md     # Experiencia académica
│   │   ├── publications.md   # Publicaciones
│   │   └── contact.md        # Contacto
│   │
│   ├── project/              # Habilidades categorizadas
│   │   ├── software.md       # Herramientas de software
│   │   ├── tecnicas.md       # Técnicas y metodologías
│   │   └── idiomas.md        # Idiomas
│   │
│   ├── publication/          # Publicaciones
│   └── post/                 # Blog posts (futuro)
│
├── static/                   # Assets estáticos
│   ├── img/                  # Imágenes
│   │   ├── yo.png           # Foto de perfil
│   │   └── [otras imágenes]
│   └── files/                # Archivos descargables (CV PDF, etc)
│
├── themes/                   # Temas de Hugo
│   └── hugo-academic/        # Tema Academic
│
├── public/                   # Sitio generado (no versionar si se usa Netlify)
└── fonts/                    # Fuentes personalizadas
```

## 🚀 Instalación Local

### Requisitos Previos

- **Hugo Extended** v0.120.0 o superior ([Descargar](https://gohugo.io/installation/))
- **Git** para control de versiones
- **R y RStudio** (opcional, para desarrollo con blogdown)

### Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/oscarzambrano/web_portafolio.git
cd web_portafolio
```

2. **Instalar Hugo Extended:**

**macOS (Homebrew):**
```bash
brew install hugo
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt-get install hugo
```

**Windows (Chocolatey):**
```bash
choco install hugo-extended
```

3. **Verificar instalación:**
```bash
hugo version
# Debe mostrar: hugo v0.120.0+extended o superior
```

## 💻 Uso y Desarrollo

### Servidor de Desarrollo Local

Ejecutar servidor local con hot-reload:

```bash
hugo server -D --navigateToChanged
```

El sitio estará disponible en: `http://localhost:1313/`

**Opciones útiles:**
- `-D`: Incluir borradores (draft: true)
- `--navigateToChanged`: Auto-navegar a contenido modificado
- `--disableFastRender`: Regenerar todo el sitio (útil para debugging)

### Desarrollo con R/blogdown

Si usas RStudio y blogdown:

```r
# Instalar blogdown (primera vez)
install.packages("blogdown")

# Servir el sitio
blogdown::serve_site()

# Crear nuevo post
blogdown::new_post("Título del Post")
```

### Build de Producción

Generar sitio estático optimizado:

```bash
hugo --gc --minify
```

El sitio generado estará en `/public/`

**Flags:**
- `--gc`: Limpia caché no utilizado
- `--minify`: Minifica HTML, CSS, JS

## 🌍 Deployment

### Netlify (Recomendado)

El sitio está configurado para deployment automático en Netlify:

1. **Conectar repositorio a Netlify:**
   - Ir a [Netlify](https://app.netlify.com/)
   - "New site from Git" → Seleccionar GitHub
   - Elegir repositorio `oscarzambrano/web_portafolio`

2. **Configuración automática:**
   - Netlify detecta `netlify.toml` automáticamente
   - Build command: `hugo --gc --minify`
   - Publish directory: `public`
   - Hugo version: 0.120.4

3. **Deployment:**
   - **Automático**: Cada push a `main` despliega automáticamente
   - **Preview**: Cada PR genera preview deployment

4. **Custom Domain (opcional):**
   - En Netlify: Domain settings → Add custom domain
   - Configurar DNS según instrucciones de Netlify

### Alternativas de Deployment

**GitHub Pages:**
```bash
# Configurar GitHub Actions (crear .github/workflows/deploy.yml)
# Ver documentación: https://gohugo.io/hosting-and-deployment/hosting-on-github/
```

**Vercel:**
```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy
vercel
```

## 📝 Actualizar Contenido

### Experiencia Laboral

Editar `content/home/experiencia.md`:
- Reemplazar `[TEMPLATE: ...]` con información real
- Agregar fechas específicas
- Completar logros y funciones

### Reconocimientos

Editar `content/home/reconocimientos.md`:
- Completar información del Early Adopter SAP HANA Vector Engine
- Agregar certificaciones obtenidas
- Incluir presentaciones en conferencias

### Educación

Editar `content/home/educacion.md`:
- Agregar maestrías/diplomados desde 2019
- Incluir certificaciones SAP, AWS, DataCamp
- Listar cursos relevantes completados

### Habilidades Técnicas

Editar `content/project/software.md` y `content/project/tecnicas.md`:
- Ya actualizados con stack SAP, AWS, ML
- Agregar nuevas tecnologías según sea necesario

### Información Personal

Editar `config.toml`:
- Actualizar Google Analytics ID (línea 15)
- Modificar URL base si tienes dominio custom (línea 1)
- Agregar/modificar redes sociales (sección `[[params.social]]`)

## 🔧 Configuración

### Google Analytics

1. Crear cuenta en [Google Analytics](https://analytics.google.com/)
2. Obtener ID de medición (formato: `G-XXXXXXXXXX`)
3. Editar `config.toml` línea 15:
```toml
googleAnalytics = "G-XXXXXXXXXX"
```

### SEO

Configurado en `config.toml` líneas 28-34:
- **description**: Meta descripción del sitio
- **keywords**: Palabras clave para SEO
- **og_image**: Imagen para redes sociales (Open Graph)

### Redes Sociales

Editar sección `[[params.social]]` en `config.toml`:
```toml
[[params.social]]
  icon = "twitter"          # Icono de Font Awesome
  icon_pack = "fa"          # Pack de iconos (fa o ai)
  link = "https://..."      # URL del perfil
```

## 🎨 Personalización

### Cambiar Tema de Color

Editar `config.toml` línea 37:
```toml
color_theme = "default"  # Opciones: default, ocean, forest, coffee
```

### Cambiar Fuente

Editar `config.toml` línea 42:
```toml
font = "playfair"  # Opciones: default, classic, playfair
```

### Agregar Widget en Homepage

1. Crear archivo en `content/home/nombre-widget.md`
2. Definir peso (`weight`) para ordenar
3. Hugo lo detecta automáticamente

## 📚 Recursos

### Documentación
- [Hugo Documentation](https://gohugo.io/documentation/)
- [Hugo Academic Theme](https://github.com/gcushen/hugo-academic)
- [Netlify Docs](https://docs.netlify.com/)
- [blogdown Book](https://bookdown.org/yihui/blogdown/)

### Tutoriales
- [Hugo Quick Start](https://gohugo.io/getting-started/quick-start/)
- [Deploy Hugo on Netlify](https://www.netlify.com/blog/2016/09/21/a-step-by-step-guide-hugo-on-netlify/)

## 🐛 Troubleshooting

### Error: Hugo command not found
```bash
# Verificar instalación
which hugo

# Reinstalar Hugo
# Ver sección "Instalación" arriba
```

### Cambios no se reflejan
```bash
# Limpiar caché y regenerar
hugo --gc
hugo server --disableFastRender
```

### Tema no se carga
```bash
# Verificar submódulo de tema
git submodule update --init --recursive
```

### Error en build de Netlify
- Verificar `HUGO_VERSION` en `netlify.toml` (debe ser 0.120.4+)
- Revisar logs de build en Netlify dashboard
- Probar build local: `hugo --gc --minify`

## 📞 Contacto

**Oscar Zambrano**
- Email: oscar.zambrano.cl@gmail.com
- LinkedIn: [oscarzambranoparra](https://www.linkedin.com/in/oscarzambranoparra)
- GitHub: [oscarzambrano](https://github.com/oscarzambrano)
- Empresa: [NS Agro S.A.](https://nsagro.cl)

## 📄 Licencia

Este proyecto es personal y propietario. El tema Hugo Academic tiene su propia licencia MIT.

---

**Última actualización:** Noviembre 2025
**Estado:** ✅ Producción (con templates pendientes de completar)

## ✅ Checklist de Actualización

### Completado
- [x] Actualizar configuración general (config.toml)
- [x] Corregir avatar (yo.png)
- [x] Eliminar Google+ (red social descontinuada)
- [x] Actualizar copyright (2019-2025)
- [x] Actualizar resumen profesional
- [x] Agregar experiencia NS Agro
- [x] Crear sección de reconocimientos SAP 2024
- [x] Actualizar habilidades técnicas (SAP, AWS, ML)
- [x] Configurar Netlify deployment
- [x] Mejorar SEO básico

### Pendiente (TEMPLATES para completar)
- [ ] Completar fechas exactas de roles en NS Agro
- [ ] Completar descripciones de Jefe de Ciencia de Datos y Data Scientist
- [ ] Agregar certificaciones SAP, AWS, DataCamp
- [ ] Completar cursos DataCamp destacados
- [ ] Agregar detalles Early Adopter SAP HANA Vector Engine
- [ ] Decidir si mantener experiencias anteriores (Equifax, etc.)
- [ ] Configurar Google Analytics (obtener ID)
- [ ] Configurar dominio custom (opcional)
- [ ] Agregar proyectos destacados al portfolio
- [ ] Considerar versión en inglés (opcional)

### Post-Deployment
- [ ] Conectar repositorio a Netlify
- [ ] Verificar build exitoso
- [ ] Probar sitio en producción
- [ ] Configurar SSL (automático en Netlify)
- [ ] Enviar sitemap a Google Search Console
- [ ] Compartir en LinkedIn
