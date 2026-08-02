"""
Punto de reorden y sugerido de compra bajo demanda y plazo de entrega inciertos.

El problema real: en una comercializadora de insumos agrícolas, quebrar stock en
plena temporada de siembra cuesta la venta y al cliente; sobre-stockear inmoviliza
capital en un negocio de márgenes estrechos. La pregunta operativa no es "¿cuánto
pedimos?" sino "¿en qué nivel de inventario disparamos el pedido, y de qué tamaño?".

Este PoC simula esa decisión con una política (s, S) y muestra el intercambio real
entre nivel de servicio e inventario inmovilizado.

Datos: sintéticos, generados con una semilla fija. No proceden de ninguna empresa.

Uso:
    pip install -r requirements.txt
    python reorden.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # sin display en CI
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

SEMILLA = 20260802
DIAS = 730          # dos temporadas completas
SALIDA = Path(__file__).resolve().parents[2] / "static" / "poc" / "punto-reorden"

# Paleta alineada con el sitio
AZUL, VIOLETA, GRIS, ROJO = "#2563eb", "#4f46e5", "#6b7280", "#dc2626"


# ─────────────────────────────────────────────────────────────────────────────
# 1. Demanda
# ─────────────────────────────────────────────────────────────────────────────
def demanda_diaria(dias: int, rng: np.random.Generator) -> np.ndarray:
    """Demanda diaria de un insumo agrícola.

    Dos componentes que importan para dimensionar inventario:

    - Estacionalidad anual. La siembra concentra el consumo; fuera de temporada
      la demanda no desaparece, baja.
    - Sobredispersión. Los pedidos llegan en lotes grandes y esporádicos, así que
      la varianza supera a la media. Una Poisson lo subestimaría: usamos binomial
      negativa, que es la Poisson con la media aleatorizada por una Gamma.
    """
    t = np.arange(dias)
    base = 120.0
    estacional = 1.0 + 0.55 * np.sin(2 * np.pi * (t - 60) / 365.25)
    media = base * estacional

    # Binomial negativa parametrizada por media y factor de dispersión.
    # var = media * dispersion  =>  dispersion > 1 es sobredispersión.
    dispersion = 2.4
    p = 1.0 / dispersion
    n = media * p / (1.0 - p)
    return rng.negative_binomial(n, p).astype(float)


def plazo_entrega(rng: np.random.Generator, tam: int = 1) -> np.ndarray:
    """Plazo de entrega del proveedor, en días.

    Discretizado de una lognormal: casi siempre ~7 días, con cola a la derecha.
    Esa cola es justamente la que provoca los quiebres, y es la razón por la que
    el stock de seguridad debe cubrir la varianza del plazo, no solo la de la
    demanda.
    """
    dias = rng.lognormal(mean=np.log(7.0), sigma=0.35, size=tam)
    return np.clip(np.round(dias), 3, 30)


# ─────────────────────────────────────────────────────────────────────────────
# 2. Política de inventario
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class Resultado:
    z: float
    punto_reorden: float
    nivel_objetivo: float
    nivel_servicio: float      # fracción de demanda servida sin demora
    dias_quiebre: int
    inventario_medio: float
    pedidos: int
    traza: pd.DataFrame


def punto_de_reorden(mu_d: float, sd_d: float, mu_l: float, sd_l: float, z: float) -> float:
    """Punto de reorden con demanda y plazo de entrega inciertos.

        ROP = mu_d * mu_l  +  z * sqrt( mu_l * sd_d^2  +  mu_d^2 * sd_l^2 )

    El segundo término bajo la raíz es el que se olvida con frecuencia: si el
    proveedor es errático, la variabilidad del PLAZO domina el stock de
    seguridad, y comprar más seguido no arregla nada.
    """
    var_dl = mu_l * sd_d**2 + (mu_d**2) * sd_l**2
    return mu_d * mu_l + z * np.sqrt(var_dl)


def parametros_estimados() -> tuple[float, float, float, float]:
    """Parámetros estimados de un histórico previo, como en la práctica: el
    proceso no se conoce, se estima. Fijos, no dependen del escenario simulado."""
    hist = demanda_diaria(365, np.random.default_rng(SEMILLA + 99))
    l_hist = plazo_entrega(np.random.default_rng(SEMILLA + 7), 500)
    return hist.mean(), hist.std(ddof=1), l_hist.mean(), l_hist.std(ddof=1)


def simular(z: float, dias: int, semilla_escenario: int) -> Resultado:
    """Simula una política (s, S) día a día.

    s = punto de reorden. Al caer la POSICIÓN de inventario (stock físico más lo
    ya pedido y no recibido) por debajo de s, se emite un pedido hasta S.
    Usar la posición y no el stock físico es lo que evita pedir dos veces lo
    mismo mientras un pedido viaja.

    NÚMEROS ALEATORIOS COMUNES: la demanda y los plazos de entrega se derivan de
    `semilla_escenario`, no del valor de z. Así todas las políticas se enfrentan
    exactamente al mismo escenario y la diferencia observada entre ellas es la
    política, no el azar. Sin esto la curva de servicio sale no monótona y las
    comparaciones no significan nada.
    """
    esc = np.random.default_rng(semilla_escenario)
    dem = demanda_diaria(dias, esc)
    # Plazos pre-generados por número de pedido: el pedido k-ésimo sufre el mismo
    # retraso en todas las políticas.
    plazos = plazo_entrega(esc, 400).astype(int)

    mu_d, sd_d, mu_l, sd_l = parametros_estimados()
    s = punto_de_reorden(mu_d, sd_d, mu_l, sd_l, z)
    # Cantidad económica de pedido (Wilson): equilibra costo de emitir y de mantener.
    costo_pedido, costo_mantener_unidad_dia = 900.0, 0.06
    eoq = np.sqrt(2 * costo_pedido * mu_d / costo_mantener_unidad_dia)
    S = s + eoq

    stock = S
    en_transito: list[tuple[int, float]] = []   # (día de llegada, cantidad)
    filas, servida, total, quiebres, pedidos = [], 0.0, 0.0, 0, 0

    for dia in range(dias):
        # Recepciones del día
        llegan = sum(q for d, q in en_transito if d == dia)
        en_transito = [(d, q) for d, q in en_transito if d != dia]
        stock += llegan

        # Demanda; lo que no se sirve se pierde (venta perdida, no backorder:
        # en insumos agrícolas el cliente compra en otro lado ese mismo día).
        d = dem[dia]
        despacho = min(stock, d)
        stock -= despacho
        servida += despacho
        total += d
        if despacho < d:
            quiebres += 1

        # Decisión de reposición sobre la POSICIÓN de inventario
        posicion = stock + sum(q for _, q in en_transito)
        if posicion <= s:
            cantidad = S - posicion
            lt = int(plazos[pedidos % len(plazos)])
            en_transito.append((dia + lt, cantidad))
            pedidos += 1

        filas.append({"dia": dia, "stock": stock, "posicion": posicion,
                      "demanda": d, "recibido": llegan})

    traza = pd.DataFrame(filas)
    return Resultado(
        z=z, punto_reorden=s, nivel_objetivo=S,
        nivel_servicio=servida / total,
        dias_quiebre=quiebres,
        inventario_medio=traza["stock"].mean(),
        pedidos=pedidos, traza=traza,
    )


# ─────────────────────────────────────────────────────────────────────────────
# 3. Gráficos
# ─────────────────────────────────────────────────────────────────────────────
def estilo(ax) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(alpha=0.25, linewidth=0.6)
    ax.set_axisbelow(True)


def grafico_trayectoria(r: Resultado, ruta: Path) -> None:
    fig, ax = plt.subplots(figsize=(11, 4.2), dpi=150)
    t = r.traza["dia"]
    ax.fill_between(t, 0, r.traza["stock"], color=AZUL, alpha=0.16, linewidth=0)
    ax.plot(t, r.traza["stock"], color=AZUL, linewidth=1.2, label="Stock físico")
    ax.axhline(r.punto_reorden, color=VIOLETA, linestyle="--", linewidth=1.3,
               label=f"Punto de reorden ({r.punto_reorden:,.0f})")

    quiebre = r.traza[r.traza["stock"] <= 0]
    if len(quiebre):
        ax.scatter(quiebre["dia"], np.zeros(len(quiebre)), color=ROJO, s=14,
                   zorder=5, label=f"Días con quiebre ({len(quiebre)})")

    ax.set_xlabel("Día"); ax.set_ylabel("Unidades")
    ax.set_title(f"Trayectoria del inventario · política (s, S) · nivel de servicio "
                 f"{r.nivel_servicio:.1%}", fontsize=12, weight="bold", loc="left")
    ax.legend(frameon=False, fontsize=9, ncols=3)
    estilo(ax)
    fig.tight_layout(); fig.savefig(ruta, bbox_inches="tight"); plt.close(fig)


def grafico_frontera(df: pd.DataFrame, ruta: Path) -> None:
    """La curva que de verdad se lleva a un comité: cuánto inventario cuesta
    cada punto de nivel de servicio. El rendimiento decrece rápido."""
    fig, ax = plt.subplots(figsize=(8, 4.6), dpi=150)
    ax.plot(df["inventario_medio"], df["nivel_servicio"] * 100,
            "-o", color=VIOLETA, markersize=5, linewidth=1.8)

    for _, row in df.iterrows():
        if row["z"] in (0.0, 1.28, 1.65, 2.33, 3.0):
            ax.annotate(f"z={row['z']:.2f}",
                        (row["inventario_medio"], row["nivel_servicio"] * 100),
                        textcoords="offset points", xytext=(8, -10),
                        fontsize=8, color=GRIS)

    ax.axhline(98, color=ROJO, linestyle=":", linewidth=1.2)
    ax.text(df["inventario_medio"].min(), 98.15, " objetivo 98 %",
            fontsize=8.5, color=ROJO, va="bottom")
    ax.set_xlabel("Inventario medio inmovilizado (unidades)")
    ax.set_ylabel("Nivel de servicio (%)")
    ax.set_title("Cada punto de servicio cuesta más que el anterior",
                 fontsize=12, weight="bold", loc="left")
    estilo(ax)
    fig.tight_layout(); fig.savefig(ruta, bbox_inches="tight"); plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
REPLICAS = 40


def main() -> None:
    SALIDA.mkdir(parents=True, exist_ok=True)

    # Barrido del factor de seguridad z. Cada réplica es un escenario distinto,
    # pero TODAS las políticas ven los mismos escenarios (números comunes).
    zs = [0.0, 0.5, 1.0, 1.28, 1.65, 2.0, 2.33, 2.6, 3.0]
    semillas = [SEMILLA + 1000 * k for k in range(REPLICAS)]

    filas, trazas = [], {}
    for z in zs:
        reps = [simular(z, DIAS, s) for s in semillas]
        filas.append({
            "z": z,
            "servicio_teorico": stats.norm.cdf(z),
            "punto_reorden": reps[0].punto_reorden,
            "nivel_servicio": float(np.mean([r.nivel_servicio for r in reps])),
            "servicio_ee": float(np.std([r.nivel_servicio for r in reps], ddof=1)
                                 / np.sqrt(REPLICAS)),
            "dias_quiebre": float(np.mean([r.dias_quiebre for r in reps])),
            "inventario_medio": float(np.mean([r.inventario_medio for r in reps])),
            "pedidos": float(np.mean([r.pedidos for r in reps])),
        })
        trazas[z] = reps[0]      # una réplica representativa, para el gráfico

    df = pd.DataFrame(filas)

    # Política mínima que alcanza el objetivo de servicio
    objetivo = 0.98
    cumplen = df[df["nivel_servicio"] >= objetivo]
    elegida = cumplen.iloc[0] if len(cumplen) else df.iloc[-1]
    r_elegida = trazas[elegida["z"]]

    grafico_trayectoria(r_elegida, SALIDA / "trayectoria.png")
    grafico_frontera(df, SALIDA / "frontera-servicio.png")
    df.to_csv(Path(__file__).parent / "resultados.csv", index=False)

    pd.set_option("display.width", 120)
    print("\nBarrido del factor de seguridad\n" + "-" * 78)
    print(df.to_string(index=False, float_format=lambda v: f"{v:,.3f}"))
    print("-" * 78)
    print(f"\nPolítica mínima que alcanza {objetivo:.0%} de servicio:")
    print(f"  z = {elegida['z']:.2f}")
    print(f"  punto de reorden   = {elegida['punto_reorden']:,.0f} unidades")
    print(f"  nivel de servicio  = {elegida['nivel_servicio']:.2%}")
    print(f"  inventario medio   = {elegida['inventario_medio']:,.0f} unidades")
    print(f"  pedidos en 2 años  = {elegida['pedidos']:.1f} (promedio)")
    print(f"\n{REPLICAS} réplicas por política, con números aleatorios comunes.")
    print(f"\nFiguras en {SALIDA}")


if __name__ == "__main__":
    main()
