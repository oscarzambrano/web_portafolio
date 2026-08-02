---
# Deja el título vacío para usar el del sitio
title: ''
date: 2026-08-02
type: landing

design:
  spacing: '6rem'

sections:
  # ── Perfil ────────────────────────────────────────────────────────────────
  - block: resume-biography-3
    content:
      username: admin
      text: ''
      # El PDF se genera con `node tools/cv/build-cv.mjs` y se commitea:
      # Netlify no tiene navegador en el build. Regenéralo si cambia el perfil.
      button:
        text: Descargar CV
        url: '/cv/oscar-zambrano-cv.pdf'
      headings:
        about: 'Perfil'
        education: 'Formación'
        interests: 'Intereses'
    design:
      background:
        gradient_mesh:
          enable: true
      avatar:
        size: large
        shape: circle

  # ── Referencia SAP 1 de 2: SAP HANA Cloud vector engine ───────────────────
  # Todo lo que sigue está publicado por SAP. No se añade ninguna cifra
  # interna ni detalle de arquitectura que no esté ya en esas fuentes.
  - block: markdown
    id: proyecto
    content:
      title: 'Precios asistidos por IA para una fuerza de venta en terreno'
      text: |-
        *Caso publicado por SAP — SAP HANA Cloud vector engine.*

        **El problema.** Más del 95 % de la fuerza de venta de Martínez y
        Valdivieso trabaja en terreno, con conectividad intermitente y sin
        acceso cómodo a los sistemas centrales. Cotizar bien exige considerar
        al cliente, su historial y su riesgo — en un mercado de márgenes
        estrechos donde cada variable de la negociación mueve la rentabilidad.

        **El enfoque.** El vendedor envía un mensaje de texto o de voz con los
        productos y las condiciones de pago. Un bot transcribe el audio, y un
        modelo de machine learning alojado en SAP BTP arma la cotización
        cruzando esos datos con el *vector engine* de SAP HANA Cloud.

        **El resultado.** El precio se genera para cada cliente concreto, a
        partir del detalle del pedido, su historial de compras y su
        clasificación crediticia. La fuerza de venta remota puede cotizar en el
        momento, y la empresa sostiene su rentabilidad mientras crece.

        **Tecnologías.** SAP HANA Cloud (*vector engine* y librerías de machine
        learning embebidas, accesibles desde R y Python), SAP BTP, modelo
        entrenado por el equipo interno.

        **Publicado por SAP:**
        [caso de cliente — vector engine](https://www.sap.com/assetdetail/2025/06/54beee34-187f-0010-bca6-c68f7e60039b.html) ·
        [Martínez y Valdivieso, cotizaciones a tiempo](https://www.sap.com/asset/dynamic/2025/08/b83db80d-1a7f-0010-bca6-c68f7e60039b.html) ·
        [SAP News Latinoamérica](https://news.sap.com/latinamerica/2025/01/ns-agro-lidera-transformacion-digital-de-martinez-y-valdivieso-con-sap-en-ia/)

        **En medios:**
        [Cooperativa](https://www.cooperativa.cl/noticias/corporativo/especiales/sap/tecnologia-sap-basada-en-ia-ns-agro-lidera-la-transformacion-digital-de/2025-05-05/175725.html) ·
        [Portal Agro Chile](https://www.portalagrochile.cl/2025/01/06/ns-agro-lidera-la-transformacion-digital-de-martinez-y-valdivieso-con-tecnologia-sap-basada-en-ia/) ·
        [Portal Innova](https://portalinnova.cl/ns-agro-lidera-la-transformacion-digital-de-martinez-y-valdivieso-con-tecnologia-sap-basada-en-ia/) ·
        [BNamericas](https://www.bnamericas.com/en/news/ns-agro-leads-the-digital-transformation-of-martinez-y-valdivieso-with-ai-based-sap-technology)
    design:
      columns: '1'

  # ── Referencia SAP 2 de 2: Torneo de Innovación SAP NOW Chile 2024 ────────
  - block: markdown
    id: reconocimientos
    content:
      title: 'Torneo de Innovación SAP NOW Chile 2024'
      text: |-
        NS Agro ganó la final frente a **Arauco** con una solución de IA
        generativa de componente *no-code/low-code*, en un formato
        *reverse shark-tank* donde un jurado de startups evaluó a las empresas
        participantes. El triunfo dio el paso a la fase regional de
        Latinoamérica, junto a México, Brasil, Colombia y Argentina.

        La solución optimizaba precios para dar competitividad en un mercado de
        márgenes muy estrechos, donde la capacidad de negociación es clave y
        cada variable comercial impacta la rentabilidad.

        Participé en el equipo ganador como **científico de datos y
        especialista en IA**. Sobre el reto, lo resumí entonces en una frase:
        lo más difícil fue *entender el problema que se nos planteaba*.

        **Publicado por SAP:**
        [SAP News Latinoamérica](https://news.sap.com/latinamerica/2024/09/ns-agro-gana-torneo-innovacion-en-sap-now-chile/)

        **En medios chilenos:**
        [Cooperativa](https://cooperativa.cl/noticias/corporativo/especiales/sap-now-chile/ia-e-innovacion-sap-now-chile-reunio-a-lo-mas-destacado-en-tecnologia/2024-09-02/140841.html) ·
        [Tekios](https://tekiosmag.com/2024/09/06/ns-agro-gana-torneo-de-innovacion-en-sap-now-chile/) ·
        [La Quinta Emprende](https://laquintaemprende.cl/2024/09/ns-agro-gana-torneo-de-innovacion-en-sap-now-chile/) ·
        [Gerencia](https://www.gerencia.cl/innovation/innovacion-empresarial-sap-destaca-rol-de-la-tecnologia/) ·
        [ITSitio Chile](https://www.itsitio.com/ch/eventos/sap-now-en-chile-la-empresa-mostro-innovacion-y-el-futuro-de-la-digitalizacion-en-las-organizaciones/)
    design:
      columns: '1'
      # OJO: no fijes aquí un color de fondo. Un valor como '#f3f4f6' no cambia
      # con el tema: en modo oscuro el texto se aclara pero el fondo sigue
      # claro, y la sección queda ilegible. Deja que el tema lo resuelva.

  # ── Contacto ──────────────────────────────────────────────────────────────
  - block: markdown
    id: contacto
    content:
      title: 'Contacto'
      text: |-
        Si trabajas en analítica sobre plataforma SAP, en IA aplicada al agro,
        o quieres comentar algo de lo de arriba, escríbeme.

        [oscar.zambrano.cl@gmail.com](mailto:oscar.zambrano.cl@gmail.com) ·
        [LinkedIn](https://www.linkedin.com/in/oscarzambranoparra) ·
        [GitHub](https://github.com/oscarzambrano)

        Santiago, Chile.
    design:
      columns: '1'
      background:
        gradient_mesh:
          enable: true
---
