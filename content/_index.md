---
# Leave the homepage title empty to use the site title
title: ''
date: 2025-01-01
type: landing

design:
  # Default section spacing
  spacing: '6rem'

sections:
  - block: resume-biography-3
    content:
      # Choose a user profile to display (a folder name within `content/authors/`)
      username: admin
      text: ''
      # Show a call-to-action button under your biography? (optional)
      button:
        text: Descargar CV
        url: https://drive.google.com/open?id=1343BInJybFxvWUXvcRyLE-FkBJjC5RDz
      headings:
        about: 'Sobre mí'
        education: 'Educación'
        interests: 'Intereses'
    design:
      background:
        gradient_mesh:
          enable: true
      avatar:
        size: large
        shape: circle

  - block: markdown
    content:
      title: '🏆 Logros Destacados 2024'
      subtitle: ''
      text: |-
        ## Ganador Torneo de Innovación SAP NOW Chile 2024

        Desarrollé una solución de **IA Generativa** con arquitectura **No-Code/Low-Code** que clasificó para representar a Chile en la competencia regional LAC.

        - Prototipo funcional desarrollado en **2 días**
        - Reconocimiento por SAP a nivel corporativo
        - Proyecto featured en [La Quinta Emprende](https://laquintaemprende.cl/2024/09/ns-agro-gana-torneo-de-innovacion-en-sap-now-chile-2024/)

        ## SAP HANA Vector Engine Early Adopter

        Participación en programa exclusivo de **Early Adopters** de SAP para tecnologías de vectores y embeddings, aplicando **RAG** (Retrieval-Augmented Generation) y **LLMs** en producción.
    design:
      columns: '1'
      background:
        color: '#f3f4f6'

  - block: markdown
    content:
      title: '💼 Experiencia Profesional'
      subtitle: ''
      text: |-
        ### NS Agro S.A. | 2019 - Actualidad

        **Subgerente Data Analytics e IA** (2022 - Presente)
        - Liderazgo de transformación digital con SAP BTP
        - Implementación de arquitectura cloud-native en SAP Cloud Foundry
        - Desarrollo de modelos ML en producción con SAP AI Core

        **Jefe de Ciencia de Datos** (2020 - 2021)
        - Liderazgo de equipo de Data Science (2+ personas)
        - Implementación de modelos predictivos empresariales

        **Data Scientist** (2019 - 2020)
        - Desarrollo de dashboards ejecutivos con SAP Analytics Cloud
        - Análisis de datos y modelado estadístico
    design:
      columns: '1'

  - block: markdown
    content:
      title: '🛠️ Stack Tecnológico'
      subtitle: ''
      text: |-
        #### SAP Business Technology Platform
        - **SAP BTP Cloud Foundry Runtime**: Arquitectura cloud-native
        - **SAP HANA Cloud**: Data modeling, in-memory computing
        - **SAP Data Sphere**: Enterprise data architecture
        - **SAP Analytics Cloud**: Dashboards ejecutivos
        - **SAP AI Core & Launchpad**: MLOps, model deployment
        - **SAP HANA Vector Engine**: Embeddings, RAG (Early Adopter)

        #### Cloud & DevOps
        - **AWS**: EC2, ECR, S3
        - **Docker & Kubernetes**: Containerización
        - **Posit Workbench, Jupyter, VS Code**
        - **Atlassian Suite**: Jira, Confluence, Bitbucket

        #### Machine Learning & IA
        - **LLMs & IA Generativa**: Fine-tuning, RAG, Prompt Engineering
        - **Frameworks**: TensorFlow, PyTorch, Scikit-learn
        - **Hugging Face Transformers**
        - **MLOps**: CI/CD para modelos ML
    design:
      columns: '2'
      background:
        color: '#ffffff'

  - block: markdown
    content:
      title: '📬 Contacto'
      subtitle: ''
      text: |-
        ¿Interesado en colaborar en proyectos de **IA Generativa**, **SAP BTP** o **Transformación Digital**?

        Contáctame vía [LinkedIn](https://www.linkedin.com/in/oscarzambranoa) o [email](mailto:oscarzambranoa@gmail.com).
    design:
      columns: '1'
      background:
        gradient_mesh:
          enable: true
---
