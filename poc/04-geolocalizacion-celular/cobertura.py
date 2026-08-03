"""
Cobertura de una red celular urbana: dónde falta señal y a cuánta gente afecta.

El problema real: una red de antenas no se evalúa por cuántas antenas tiene,
sino por a cuánta gente deja sin servicio. Un hueco de cobertura sobre un cerro
deshabitado no importa; el mismo hueco sobre un barrio denso es una avería
comercial. La pregunta no es "¿qué porcentaje del territorio cubrimos?" sino
"¿qué porcentaje de la POBLACIÓN cubrimos, y dónde está la que no?".

Este PoC modela la propagación sobre una ciudad sintética, teselación de Voronoi
para asignar servidor, y detecta los huecos ponderados por población.

Datos: sintéticos, con semilla fija. No proceden de ningún operador.

Uso:
    pip install -r requirements.txt
    python cobertura.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from scipy.spatial import Voronoi, cKDTree, voronoi_plot_2d

SEMILLA = 20260802
SALIDA = Path(__file__).resolve().parents[2] / "static" / "poc" / "geolocalizacion-celular"

AZUL, VIOLETA, GRIS, ROJO, VERDE = "#2563eb", "#4f46e5", "#6b7280", "#dc2626", "#059669"

CIUDAD_KM = 12.0          # lado del área modelada
N_ANTENAS = 46
POT_TX_DBM = 43.0         # potencia de transmisión típica de macrocelda
EXP_PERDIDA = 3.4         # exponente de pérdida de trayecto, entorno urbano
UMBRAL_DBM = -100.0       # bajo esto se considera sin servicio útil
SIGMA_SOMBRA_DB = 9.0     # desviación del sombreado, típica urbana
RHO_SOMBRA = 0.5          # correlación de la sombra entre enlaces
PENETRACION_DB = 19.0     # pérdida media al entrar a un edificio
REJILLA = 320


# ─────────────────────────────────────────────────────────────────────────────
# 1. Ciudad sintética
# ─────────────────────────────────────────────────────────────────────────────
def generar_ciudad(rng: np.random.Generator):
    """Antenas y población sobre la misma ciudad, con formas distintas.

    Las antenas siguen el centro histórico, donde estuvo la demanda cuando se
    construyó la red; la población tiene además dos polos periféricos.

    Nota honesta sobre el resultado: este desfase resultó ser MENOR de lo que
    se esperaba al diseñar el escenario. Las antenas periféricas, aunque pocas,
    alcanzan a cubrir los polos de población, y los huecos terminan cayendo
    sobre terreno vacío. El guion previsto era el contrario.

    Se deja tal cual. Ajustar los parámetros hasta que la simulación diga lo
    que uno quería es exactamente el error que este PoC pretende ilustrar.
    """
    # Antenas: concentradas en el centro, con dispersión
    n_centro = int(N_ANTENAS * 0.62)
    centro = rng.normal(0, 2.1, size=(n_centro, 2))
    periferia = rng.uniform(-CIUDAD_KM / 2, CIUDAD_KM / 2,
                            size=(N_ANTENAS - n_centro, 2))
    antenas = np.clip(np.vstack([centro, periferia]),
                      -CIUDAD_KM / 2 + 0.3, CIUDAD_KM / 2 - 0.3)

    # Población: tres núcleos. Uno coincide con el centro; dos no.
    nucleos = np.array([[0.0, 0.0], [4.3, -3.6], [-4.0, 3.9]])
    pesos = np.array([0.45, 0.32, 0.23])
    return antenas, nucleos, pesos


def malla_poblacion(nucleos: np.ndarray, pesos: np.ndarray):
    """Densidad de población sobre una rejilla, como mezcla de gaussianas."""
    ejes = np.linspace(-CIUDAD_KM / 2, CIUDAD_KM / 2, REJILLA)
    X, Y = np.meshgrid(ejes, ejes)
    dens = np.zeros_like(X)
    anchos = [2.3, 1.5, 1.4]
    for (cx, cy), w, s in zip(nucleos, pesos, anchos):
        dens += w * np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / (2 * s ** 2))
    dens /= dens.sum()
    return X, Y, dens


# ─────────────────────────────────────────────────────────────────────────────
# 2. Propagación
# ─────────────────────────────────────────────────────────────────────────────
def sombreado(forma: tuple[int, int], rng: np.random.Generator,
              sigma_db: float = SIGMA_SOMBRA_DB) -> np.ndarray:
    """Desvanecimiento por sombra, espacialmente correlacionado.

    Sin esto el modelo no sirve. Con pura pérdida por distancia, 46 antenas en
    12 km cubren TODO: hasta el punto más alejado recibe unos -85 dBm, muy por
    encima del umbral. Concluiríamos que no hay huecos de cobertura, y sería
    falso.

    Los huecos reales no los causa la distancia: los causa la OBSTRUCCIÓN —un
    edificio, un cerro, un patio interior—. Y esa obstrucción está
    correlacionada en el espacio: si hay sombra en un punto, muy probablemente
    la hay un metro más allá. Por eso se filtra ruido blanco con un núcleo
    gaussiano en vez de sumar ruido independiente por píxel, que produciría
    huecos de un píxel sin sentido físico.
    """
    from scipy.ndimage import gaussian_filter
    ruido = rng.normal(0.0, 1.0, size=forma)
    # ~500 m de longitud de correlación, típica en entorno urbano
    campo = gaussian_filter(ruido, sigma=REJILLA * 0.5 / CIUDAD_KM, mode="reflect")
    campo /= campo.std()
    return campo * sigma_db


def potencia_recibida(X: np.ndarray, Y: np.ndarray, antenas: np.ndarray,
                      rng: np.random.Generator):
    """Mejor servidor y potencia recibida en cada punto de la rejilla.

    Modelo log-distancia con sombreado:

        P_rx = P_tx - 10 · n · log10(d) + S(x, y)

    El móvil se engancha a la antena que le llega más fuerte, no a la más
    cercana. Con sombreado esas dos dejan de coincidir, que es lo que pasa de
    verdad y lo que hace que las celdas no sean polígonos limpios de Voronoi.
    """
    puntos = np.column_stack([X.ravel(), Y.ravel()])
    d = np.linalg.norm(puntos[:, None, :] - antenas[None, :, :], axis=2)
    d = np.maximum(d, 0.05)                      # evita log(0) bajo la antena
    prx = POT_TX_DBM - 10.0 * EXP_PERDIDA * np.log10(d * 1000.0)

    # Sombra CORRELACIONADA entre enlaces.
    #
    # Un primer intento sumaba una sombra independiente por antena. No producía
    # ni un hueco: al quedarse el móvil con el máximo de 46 enlaces
    # independientes, la diversidad macro promedia los desvanecimientos y
    # siempre hay alguna antena que llega bien.
    #
    # En la realidad los enlaces NO son independientes: el edificio que bloquea
    # al móvil lo bloquea en casi todas las direcciones. Se modela con una
    # componente común más una por enlace,
    #     S_i = √ρ · S_común  +  √(1-ρ) · S_i
    # con ρ ≈ 0.5, valor habitual en la literatura. La componente común no se
    # promedia, y es la que abre los huecos.
    comun = sombreado(X.shape, rng).ravel()
    for i in range(len(antenas)):
        prx[:, i] += (np.sqrt(RHO_SOMBRA) * comun
                      + np.sqrt(1 - RHO_SOMBRA) * sombreado(X.shape, rng).ravel())

    mejor = prx.max(axis=1)
    servidor = prx.argmax(axis=1)

    # Pérdida de penetración a interiores. El umbral de servicio se evalúa para
    # un usuario DENTRO de un edificio, que es donde se cursa la mayor parte del
    # tráfico. Es la razón por la que un operador puede reportar 99 % de
    # cobertura exterior y aun así tener quejas: son dos mapas distintos.
    penetracion = PENETRACION_DB + sombreado(X.shape, rng, sigma_db=5.0)
    mejor = mejor.reshape(X.shape) - penetracion
    return mejor, servidor.reshape(X.shape)


# ─────────────────────────────────────────────────────────────────────────────
# 3. Gráficos
# ─────────────────────────────────────────────────────────────────────────────
def estilo(ax) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(alpha=0.25, linewidth=0.6)
    ax.set_axisbelow(True)


def grafico_voronoi(antenas: np.ndarray, nucleos: np.ndarray, ruta: Path) -> None:
    """Celdas de servicio. Cada polígono es el área donde esa antena es la más
    cercana: la geometría de la red, antes de mirar la propagación."""
    vor = Voronoi(antenas)
    fig, ax = plt.subplots(figsize=(8.4, 8), dpi=150)
    voronoi_plot_2d(vor, ax=ax, show_vertices=False, show_points=False,
                    line_colors=GRIS, line_width=0.9, line_alpha=0.55)
    ax.scatter(antenas[:, 0], antenas[:, 1], s=46, marker="^", color=VIOLETA,
               edgecolors="white", linewidths=0.7, zorder=5, label="Antenas")
    ax.scatter(nucleos[:, 0], nucleos[:, 1], s=320, marker="o", color=ROJO,
               alpha=0.22, zorder=3)
    ax.scatter(nucleos[:, 0], nucleos[:, 1], s=44, marker="x", color=ROJO,
               linewidths=2.2, zorder=6, label="Núcleos de población")
    lim = CIUDAD_KM / 2
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect("equal")
    ax.set_xlabel("km"); ax.set_ylabel("km")
    ax.set_title("Celdas de servicio y dónde vive la gente",
                 fontsize=12.5, weight="bold", loc="left")
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    estilo(ax)
    fig.tight_layout(); fig.savefig(ruta, bbox_inches="tight"); plt.close(fig)


def grafico_cobertura(X, Y, señal, dens, antenas, ruta: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.8, 8), dpi=150)
    cmap = LinearSegmentedColormap.from_list(
        "señal", ["#7f1d1d", "#dc2626", "#f59e0b", "#84cc16", "#059669"])
    im = ax.pcolormesh(X, Y, señal, cmap=cmap, shading="auto",
                       vmin=UMBRAL_DBM - 15, vmax=-70)
    cb = fig.colorbar(im, ax=ax, shrink=0.82, pad=0.02)
    cb.set_label("Potencia recibida del mejor servidor (dBm)")

    # Huecos: sin señal útil
    ax.contour(X, Y, señal, levels=[UMBRAL_DBM], colors="black",
               linewidths=1.6, linestyles="--")
    # Dónde vive la gente
    ax.contour(X, Y, dens, levels=4, colors="white", linewidths=0.9, alpha=0.75)
    ax.scatter(antenas[:, 0], antenas[:, 1], s=26, marker="^", color="white",
               edgecolors="black", linewidths=0.5, zorder=5)

    lim = CIUDAD_KM / 2
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect("equal")
    ax.set_xlabel("km"); ax.set_ylabel("km")
    ax.set_title("Señal, y población superpuesta\n"
                 "línea negra: umbral de servicio  ·  contornos blancos: densidad",
                 fontsize=12.5, weight="bold", loc="left")
    fig.tight_layout(); fig.savefig(ruta, bbox_inches="tight"); plt.close(fig)


def grafico_carga(carga: pd.DataFrame, ruta: Path) -> None:
    """Población servida por antena. Una red equilibrada tendría barras
    parecidas; el desequilibrio es donde se congestiona."""
    fig, ax = plt.subplots(figsize=(9, 4.4), dpi=150)
    d = carga.sort_values("poblacion_pct", ascending=False).head(20)
    colores = [ROJO if v > d["poblacion_pct"].quantile(0.85) else AZUL
               for v in d["poblacion_pct"]]
    ax.bar(range(len(d)), d["poblacion_pct"], color=colores)
    ax.set_xticks(range(len(d)))
    ax.set_xticklabels([f"A{i}" for i in d.index], fontsize=8)
    ax.axhline(100 / len(carga), color=GRIS, linestyle="--", linewidth=1.2)
    ax.text(len(d) - 0.5, 100 / len(carga),
            f"  reparto uniforme ({100/len(carga):.1f} %)",
            fontsize=8.5, color=GRIS, va="bottom", ha="right")
    ax.set_ylabel("Población servida (%)")
    ax.set_title("Las 20 antenas más cargadas · el reparto no es parejo",
                 fontsize=12, weight="bold", loc="left")
    estilo(ax)
    fig.tight_layout(); fig.savefig(ruta, bbox_inches="tight"); plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
def main() -> None:
    SALIDA.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEMILLA)

    antenas, nucleos, pesos = generar_ciudad(rng)
    X, Y, dens = malla_poblacion(nucleos, pesos)
    señal, servidor = potencia_recibida(X, Y, antenas, rng)

    # ── Métricas ─────────────────────────────────────────────────────────────
    sin_servicio = señal < UMBRAL_DBM
    territorio_sin = sin_servicio.mean()
    poblacion_sin = dens[sin_servicio].sum()

    carga = pd.DataFrame({
        "poblacion_pct": [dens[servidor == i].sum() * 100 for i in range(len(antenas))],
        "area_km2": [(servidor == i).mean() * CIUDAD_KM ** 2 for i in range(len(antenas))],
    })

    # Vecinas de traspaso: antenas cuyas celdas se tocan
    arbol = cKDTree(antenas)
    vecinas = [len(arbol.query_ball_point(a, r=2.6)) - 1 for a in antenas]

    grafico_voronoi(antenas, nucleos, SALIDA / "celdas-voronoi.png")
    grafico_cobertura(X, Y, señal, dens, antenas, SALIDA / "cobertura-poblacion.png")
    grafico_carga(carga, SALIDA / "carga-por-antena.png")
    carga.round(3).to_csv(Path(__file__).parent / "carga-por-antena.csv")

    print(f"\nCiudad de {CIUDAD_KM:.0f}×{CIUDAD_KM:.0f} km · {len(antenas)} antenas")
    print(f"Umbral de servicio: {UMBRAL_DBM:.0f} dBm\n" + "-" * 62)
    print(f"Territorio sin servicio : {territorio_sin:6.2%}")
    print(f"Población sin servicio  : {poblacion_sin:6.2%}")
    print("-" * 62)
    razon = poblacion_sin / territorio_sin if territorio_sin else float("nan")
    print(f"Razón población/territorio: {razon:.2f}x")
    if razon < 1:
        print("  → Los huecos caen sobre terreno poco poblado: la métrica de")
        print(f"    territorio EXAGERA el problema {1/razon:.1f} veces.")
    else:
        print("  → Los huecos caen sobre zonas pobladas: la métrica de")
        print(f"    territorio SUBESTIMA el problema {razon:.1f} veces.")
    print("\nConcentración de carga")
    top5 = carga.nlargest(5, "poblacion_pct")["poblacion_pct"].sum()
    print(f"  Las 5 antenas más cargadas sirven al {top5:.1f} % de la población")
    print(f"  Reparto uniforme daría        : {5 * 100 / len(antenas):.1f} %")
    print(f"  Vecinas de traspaso (mediana) : {int(np.median(vecinas))}")
    print(f"\nFiguras en {SALIDA}")


if __name__ == "__main__":
    main()
