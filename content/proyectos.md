---
title: 'Pruebas de concepto'
date: 2026-08-02
type: landing

design:
  spacing: '5rem'

sections:
  - block: markdown
    id: intro
    content:
      title: 'Pruebas de concepto'
      text: |-
        Demostraciones ejecutables de los problemas que resuelvo en el trabajo,
        construidas sobre **datos sintéticos**. Ninguna contiene información de
        clientes, proveedores, precios ni infraestructura de ninguna empresa.

        Simular tiene una ventaja para demostrar rigor: se conoce la respuesta
        verdadera, así que se puede medir si el método la recupera. Con datos
        reales no habría contra qué comparar.

        Todas son reproducibles con semilla fija. El código está en
        [github.com/oscarzambrano/web_portafolio](https://github.com/oscarzambrano/web_portafolio/tree/master/poc).
    design:
      columns: '1'

  - block: markdown
    id: punto-reorden
    content:
      title: 'Punto de reorden y sugerido de compra'
      text: |-
        **El problema.** Quebrar stock en plena temporada de siembra cuesta la
        venta y al cliente, que compra al lado ese mismo día. Sobre-stockear
        inmoviliza capital en un negocio de márgenes estrechos. La pregunta
        operativa no es cuánto pedir, sino en qué nivel disparar el pedido.

        **El enfoque.** Política (s, S) simulada día a día sobre dos temporadas,
        con demanda estacional y sobredispersa —binomial negativa, no Poisson—
        y plazo de entrega lognormal con cola a la derecha. El punto de reorden
        incorpora la varianza del plazo, no solo la de la demanda: cuando el
        proveedor es errático, esa es la que manda.

        **El resultado.** Los rendimientos decrecen rápido. Subir de 90 % a 96 %
        de servicio cuesta unas 300 unidades de inventario medio; subir de 98 %
        a 99.4 % cuesta 360 más, para menos de un cuarto de la mejora. Esa curva
        es la conversación que hay que tener con el negocio.

        ![Frontera entre servicio e inventario](/poc/punto-reorden/frontera-servicio.png)

        **Rigor.** 40 réplicas por política con números aleatorios comunes: todas
        se enfrentan al mismo escenario, de modo que la diferencia entre ellas es
        la política y no el azar. Sin eso, la curva salía no monótona.

        [Ver el código y el detalle →](https://github.com/oscarzambrano/web_portafolio/tree/master/poc/01-punto-reorden)
    design:
      columns: '1'

  - block: markdown
    id: perfiles-latentes
    content:
      title: 'Perfiles latentes, clusters y riesgo'
      text: |-
        **El problema.** Una cartera de clientes no es una población: son varias
        mezcladas. El promedio esconde justo lo que interesa —quién paga tarde,
        quién compra estacionalmente, quién concentra el riesgo—.

        **El enfoque.** Modelo de mezcla gaussiana con covarianza libre por
        componente, sobre frecuencia de compra, ticket, mora y uso de crédito.
        El número de grupos se elige por BIC, no mirando el gráfico: sin
        penalizar la complejidad, añadir grupos siempre mejora el ajuste y se
        termina segmentando ruido.

        **El resultado.** El criterio recupera exactamente los cuatro perfiles
        simulados, con un índice de Rand de 0.98 frente a 0.93 de k-means. Y la
        lectura de negocio: la cartera impaga 9 % en promedio, pero ese número no
        describe a nadie —el riesgo varía **21 veces** entre el mejor y el peor
        perfil, y el 12 % de los clientes concentra la mayor parte de la pérdida.

        ![Riesgo por perfil](/poc/perfiles-latentes/riesgo-por-perfil.png)

        [Ver el código y el detalle →](https://github.com/oscarzambrano/web_portafolio/tree/master/poc/02-perfiles-latentes)
    design:
      columns: '1'

  - block: markdown
    id: proximas
    content:
      title: 'En preparación'
      text: |-
        - **Grafos y redes de relaciones** — detección de comunidades sobre una
          red de entidades.
        - **Geolocalización de red celular** — cobertura y vecindad sobre mapa,
          con datos abiertos de antenas.
        - **Control estadístico de procesos** — cartas de control y capacidad.
        - **Control de actualización de datos** — tablero de seguimiento de
          procesos de carga.
    design:
      columns: '1'
---
