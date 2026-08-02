# Pruebas de concepto

Demostraciones ejecutables de los problemas que resuelvo en el trabajo,
construidas sobre **datos sintéticos o públicos**. Ninguna contiene información
de clientes, proveedores, precios ni infraestructura de ninguna empresa.

Cada una es reproducible con semilla fija y se ejecuta con dos comandos.

## Etapa 1 — disponible

| | Qué demuestra |
|---|---|
| [**01 · Punto de reorden y sugerido de compra**](01-punto-reorden/) | Política (s, S) bajo demanda sobredispersa y plazo de entrega variable. La frontera entre nivel de servicio e inventario inmovilizado. |
| [**02 · Perfiles latentes, clusters y riesgo**](02-perfiles-latentes/) | Mezclas gaussianas para recuperar poblaciones ocultas en una cartera. Selección de K por BIC y comparación honesta contra k-means. |

## Etapa 2 — planificada

- **03 · Grafos y redes de relaciones** — detección de comunidades sobre una red
  de entidades, y qué revela la estructura que no revela la tabla.
- **04 · Geolocalización de red celular** — cobertura y vecindad sobre mapa, con
  datos abiertos de antenas.

## Etapa 3 — planificada

- **05 · Control estadístico de procesos** — cartas de control y capacidad, el
  ángulo Lean Six Sigma.
- **06 · Control de actualización de datos** — reescritura moderna del tablero de
  seguimiento de procesos de carga.

---

## Por qué datos sintéticos

Porque es la única forma honesta de mostrar el método sin exponer el dato. Un
portafolio que enseña cifras reales de un empleador es un problema, no un
mérito.

Simular tiene además una ventaja para demostrar rigor: **se conoce la respuesta
verdadera**, así que se puede medir si el método la recupera. En el PoC 02 eso
permite reportar un índice de Rand contra la estructura real; con datos
auténticos no habría contra qué comparar.

## Ejecutar cualquiera

```bash
cd <carpeta-del-poc>
pip install -r requirements.txt
python <script>.py
```
