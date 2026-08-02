"""
Perfiles latentes, clusters y análisis de riesgo sobre una población heterogénea.

El problema real: una cartera de clientes no es una población, son varias
mezcladas. Tratarlas con un promedio único esconde justo lo que interesa —quién
paga tarde, quién compra estacionalmente, quién concentra el riesgo—. La
pregunta no es "¿cuál es el cliente medio?" sino "¿cuántas poblaciones hay aquí
dentro, y en qué se diferencian?".

Este PoC recupera esas poblaciones sin conocerlas de antemano, elige el número
de grupos con un criterio formal en vez de a ojo, y compara el análisis de
perfiles latentes contra k-means para mostrar cuándo el segundo se equivoca.

Datos: sintéticos, con semilla fija. No proceden de ninguna empresa.

Uso:
    pip install -r requirements.txt
    python perfiles.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

SEMILLA = 20260802
N = 3000
SALIDA = Path(__file__).resolve().parents[2] / "static" / "poc" / "perfiles-latentes"

AZUL, VIOLETA, GRIS, ROJO, VERDE = "#2563eb", "#4f46e5", "#6b7280", "#dc2626", "#059669"
INDICADORES = ["frecuencia_compra", "ticket_medio", "dias_mora", "uso_credito"]


# ─────────────────────────────────────────────────────────────────────────────
# 1. Población
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class Perfil:
    nombre: str
    peso: float
    medias: np.ndarray
    escalas: np.ndarray        # desviaciones por indicador
    correlacion: float         # entre ticket y uso de crédito
    riesgo: float              # probabilidad real de impago


PERFILES = [
    # Grupo grande, compacto: el "cliente sano" que domina la cartera.
    Perfil("Recurrente sano", 0.44, np.array([12.0, 4.6, 2.0, 0.28]),
           np.array([2.2, 0.30, 1.6, 0.09]), 0.15, 0.02),
    # Estacional: compra concentrada, ticket alto, dispersión ALTA.
    # k-means lo parte en dos porque no tolera varianzas distintas.
    Perfil("Estacional de alto ticket", 0.24, np.array([4.0, 6.1, 5.0, 0.46]),
           np.array([1.8, 0.75, 4.2, 0.17]), 0.55, 0.09),
    # Grupo pequeño y muy disperso: el riesgo vive aquí.
    Perfil("Moroso concentrado", 0.12, np.array([3.2, 5.2, 34.0, 0.86]),
           np.array([1.5, 0.60, 13.0, 0.11]), 0.40, 0.41),
    # Ocasional de bajo valor: mucha frecuencia baja, poco riesgo.
    Perfil("Ocasional de bajo valor", 0.20, np.array([1.8, 3.4, 6.0, 0.19]),
           np.array([0.9, 0.42, 3.4, 0.10]), 0.05, 0.05),
]


def generar(n: int, rng: np.random.Generator) -> pd.DataFrame:
    """Genera la cartera como mezcla finita de perfiles.

    Cada perfil tiene su propia matriz de covarianza. Esto es deliberado: es
    exactamente el supuesto que k-means viola (asume grupos esféricos y de
    tamaño parecido) y que un modelo de mezcla sí puede representar.
    """
    pesos = np.array([p.peso for p in PERFILES])
    clases = rng.choice(len(PERFILES), size=n, p=pesos / pesos.sum())

    filas = []
    for k, p in enumerate(PERFILES):
        idx = np.where(clases == k)[0]
        m = len(idx)
        if m == 0:
            continue

        # Correlación inducida entre ticket (1) y uso de crédito (3)
        corr = np.eye(4)
        corr[1, 3] = corr[3, 1] = p.correlacion
        cov = np.outer(p.escalas, p.escalas) * corr
        x = rng.multivariate_normal(p.medias, cov, size=m)

        d = pd.DataFrame(x, columns=INDICADORES)
        d["clase_real"] = k
        d["impago"] = rng.random(m) < p.riesgo
        filas.append(d)

    df = pd.concat(filas, ignore_index=True).sample(frac=1, random_state=SEMILLA)

    # Dominios físicos: nada de frecuencias negativas ni uso de crédito > 1
    df["frecuencia_compra"] = df["frecuencia_compra"].clip(lower=0.1)
    df["dias_mora"] = df["dias_mora"].clip(lower=0.0)
    df["uso_credito"] = df["uso_credito"].clip(0.0, 1.0)
    return df.reset_index(drop=True)


# ─────────────────────────────────────────────────────────────────────────────
# 2. Selección del número de perfiles
# ─────────────────────────────────────────────────────────────────────────────
def seleccionar(X: np.ndarray, ks: range) -> pd.DataFrame:
    """Ajusta mezclas gaussianas y k-means para cada K.

    El número de grupos NO se elige mirando el gráfico. Se elige por BIC, que
    penaliza la complejidad: sin esa penalización, añadir grupos siempre mejora
    el ajuste y se termina segmentando ruido.
    """
    filas = []
    for k in ks:
        gmm = GaussianMixture(n_components=k, covariance_type="full",
                              n_init=8, random_state=SEMILLA, max_iter=500).fit(X)
        km = KMeans(n_clusters=k, n_init=10, random_state=SEMILLA).fit(X)
        filas.append({
            "k": k,
            "bic": gmm.bic(X),
            "aic": gmm.aic(X),
            "log_verosimilitud": gmm.score(X) * len(X),
            "inercia_kmeans": km.inertia_,
            "convergio": gmm.converged_,
        })
    return pd.DataFrame(filas)


# ─────────────────────────────────────────────────────────────────────────────
# 3. Gráficos
# ─────────────────────────────────────────────────────────────────────────────
def estilo(ax) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(alpha=0.25, linewidth=0.6)
    ax.set_axisbelow(True)


def grafico_bic(sel: pd.DataFrame, k_opt: int, k_real: int, ruta: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.4), dpi=150)
    ax.plot(sel["k"], sel["bic"], "-o", color=VIOLETA, markersize=6, linewidth=1.8)
    ax.axvline(k_opt, color=ROJO, linestyle="--", linewidth=1.3)
    ax.annotate(f"BIC mínimo: K={k_opt}", (k_opt, sel["bic"].min()),
                textcoords="offset points", xytext=(12, 18), color=ROJO, fontsize=9.5)
    if k_real != k_opt:
        ax.axvline(k_real, color=GRIS, linestyle=":", linewidth=1.2)
    ax.set_xlabel("Número de perfiles (K)"); ax.set_ylabel("BIC (menor es mejor)")
    ax.set_title("El número de grupos se elige por criterio, no a ojo",
                 fontsize=12, weight="bold", loc="left")
    ax.set_xticks(list(sel["k"]))
    estilo(ax)
    fig.tight_layout(); fig.savefig(ruta, bbox_inches="tight"); plt.close(fig)


ROTULOS = {
    "frecuencia_compra": "Frecuencia\nde compra",
    "ticket_medio": "Ticket medio\n(log)",
    "dias_mora": "Días\nde mora",
    "uso_credito": "Uso de\ncrédito",
}


def grafico_perfiles(df: pd.DataFrame, etiqueta: str,
                     nombres: dict[int, str], ruta: Path) -> None:
    """Perfiles medios por indicador, estandarizados. Es la lectura que un área
    comercial puede accionar: en qué se diferencia cada grupo.

    OJO con las etiquetas: el índice que asigna la mezcla a cada grupo es
    arbitrario y NO coincide con el orden de los perfiles verdaderos. Hay que
    mapear cada grupo recuperado a la clase real mayoritaria dentro de él, o la
    leyenda miente.
    """
    z = df.groupby(etiqueta)[INDICADORES].mean()
    z = (z - df[INDICADORES].mean()) / df[INDICADORES].std()

    fig, ax = plt.subplots(figsize=(9.5, 4.6), dpi=150)
    colores = [AZUL, VIOLETA, ROJO, VERDE, "#d97706", "#0891b2"]
    for i, (grupo, fila) in enumerate(z.iterrows()):
        ax.plot([ROTULOS[c] for c in INDICADORES], fila.values, "-o",
                linewidth=2, markersize=6, color=colores[i % len(colores)],
                label=nombres.get(grupo, f"Perfil {grupo}"))
    ax.axhline(0, color=GRIS, linewidth=0.9, linestyle="--")
    ax.set_ylabel("Desviaciones respecto a la media global")
    ax.set_title("Cada perfil se diferencia en algo distinto",
                 fontsize=12, weight="bold", loc="left")
    ax.legend(frameon=False, fontsize=9)
    estilo(ax)
    fig.tight_layout(); fig.savefig(ruta, bbox_inches="tight"); plt.close(fig)


def grafico_riesgo(tabla: pd.DataFrame, ruta: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=150)
    colores = [ROJO if v > tabla["impago"].mean() else AZUL for v in tabla["impago"]]
    barras = ax.barh(tabla["perfil"], tabla["impago"] * 100, color=colores, height=0.6)
    ax.bar_label(barras, fmt="%.1f %%", padding=4, fontsize=9.5)
    global_pct = tabla["impago_global"].iloc[0] * 100
    ax.axvline(global_pct, color=GRIS, linestyle="--", linewidth=1.2)
    ax.text(global_pct, len(tabla) - 0.35,
            f"  cartera global {tabla['impago_global'].iloc[0]:.1%}",
            fontsize=8.5, color=GRIS, va="top")
    ax.set_xlabel("Tasa de impago observada (%)")
    ax.set_title("El promedio de la cartera no describe a ningún cliente",
                 fontsize=12, weight="bold", loc="left")
    ax.set_xlim(0, max(tabla["impago"]) * 118)
    estilo(ax)
    fig.tight_layout(); fig.savefig(ruta, bbox_inches="tight"); plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
def main() -> None:
    SALIDA.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEMILLA)

    df = generar(N, rng)
    X = StandardScaler().fit_transform(df[INDICADORES].to_numpy())

    # ── Selección de K ───────────────────────────────────────────────────────
    sel = seleccionar(X, range(1, 9))
    k_opt = int(sel.loc[sel["bic"].idxmin(), "k"])

    # ── Ajuste final y comparación ──────────────────────────────────────────
    gmm = GaussianMixture(n_components=k_opt, covariance_type="full",
                          n_init=8, random_state=SEMILLA, max_iter=500).fit(X)
    df["perfil_gmm"] = gmm.predict(X)
    df["perfil_kmeans"] = KMeans(n_clusters=k_opt, n_init=10,
                                 random_state=SEMILLA).fit_predict(X)

    ari_gmm = adjusted_rand_score(df["clase_real"], df["perfil_gmm"])
    ari_km = adjusted_rand_score(df["clase_real"], df["perfil_kmeans"])

    # ── Riesgo por perfil ────────────────────────────────────────────────────
    # El índice del grupo recuperado es arbitrario: se nombra por la clase real
    # mayoritaria dentro de él. Sin este paso, cualquier etiqueta es adivinanza.
    dominante = (df.groupby("perfil_gmm")["clase_real"]
                   .agg(lambda s: s.value_counts().index[0]))
    nombres = {g: PERFILES[c].nombre for g, c in dominante.items()}

    tabla = (df.groupby("perfil_gmm")
               .agg(n=("impago", "size"), impago=("impago", "mean"))
               .reset_index())
    tabla["impago_global"] = df["impago"].mean()
    tabla["perfil"] = [nombres[g] for g in tabla["perfil_gmm"]]
    tabla = tabla.sort_values("impago", ascending=True)

    # ── Salidas ──────────────────────────────────────────────────────────────
    grafico_bic(sel, k_opt, len(PERFILES), SALIDA / "seleccion-bic.png")
    grafico_perfiles(df, "perfil_gmm", nombres, SALIDA / "perfiles-medios.png")
    grafico_riesgo(tabla, SALIDA / "riesgo-por-perfil.png")
    sel.to_csv(Path(__file__).parent / "seleccion.csv", index=False)
    tabla.to_csv(Path(__file__).parent / "riesgo-por-perfil.csv", index=False)

    print("\nSelección del número de perfiles\n" + "-" * 74)
    print(sel.to_string(index=False, float_format=lambda v: f"{v:,.1f}"))
    print("-" * 74)
    print(f"K real = {len(PERFILES)}   ·   K elegido por BIC = {k_opt}")
    print(f"\nRecuperación de la estructura verdadera (índice de Rand ajustado):")
    print(f"  mezcla gaussiana : {ari_gmm:.3f}")
    print(f"  k-means          : {ari_km:.3f}")
    print(f"\nRiesgo por perfil recuperado\n" + "-" * 74)
    print(tabla[["perfil", "n", "impago"]].to_string(
        index=False, float_format=lambda v: f"{v:,.3f}"))
    print("-" * 74)
    print(f"Impago global de la cartera: {df['impago'].mean():.1%}")
    print(f"Razón entre el perfil más y menos riesgoso: "
          f"{tabla['impago'].max() / max(tabla['impago'].min(), 1e-9):.1f}x")
    print(f"\nFiguras en {SALIDA}")


if __name__ == "__main__":
    main()
