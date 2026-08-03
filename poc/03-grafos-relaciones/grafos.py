"""
Grafos de relaciones: qué revela la estructura que no revela la tabla.

El problema real: en una cartera de proveedores y clientes, las entidades no son
independientes. Comparten domicilios, representantes, cuentas bancarias. Una
tabla las muestra como filas separadas; el grafo muestra que quince de ellas son
en realidad un mismo grupo económico. Esa diferencia importa para el riesgo de
concentración —y para detectar partes relacionadas que no se declararon—.

Este PoC construye una red de entidades enlazadas por atributos compartidos,
recupera los grupos con detección de comunidades, y muestra por qué las medidas
de centralidad responden preguntas distintas entre sí.

Datos: sintéticos, con semilla fija. No proceden de ninguna empresa.

Uso:
    pip install -r requirements.txt
    python grafos.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

SEMILLA = 20260802
SALIDA = Path(__file__).resolve().parents[2] / "static" / "poc" / "grafos-relaciones"

AZUL, VIOLETA, GRIS, ROJO, VERDE = "#2563eb", "#4f46e5", "#6b7280", "#dc2626", "#059669"
PALETA = [AZUL, VIOLETA, VERDE, "#d97706", "#0891b2", "#db2777", "#65a30d", "#7c3aed"]


# ─────────────────────────────────────────────────────────────────────────────
# 1. La red
# ─────────────────────────────────────────────────────────────────────────────
def construir_red(rng: np.random.Generator) -> tuple[nx.Graph, dict[int, int]]:
    """Red de entidades enlazadas por atributos compartidos.

    Se generan grupos económicos de tamaño desigual: unos pocos grandes y una
    cola de pequeños. Dentro de cada grupo los enlaces son densos (comparten
    domicilio, representante); entre grupos hay unos pocos enlaces —operaciones
    cruzadas legítimas— que son justamente los que confunden a un análisis
    ingenuo.

    Se añade además un puñado de entidades PUENTE: pertenecen a un grupo pero
    operan con varios. En el mundo real son intermediarios, y son los nodos que
    más importan aunque casi nunca sean los más conectados.
    """
    tamanos = [26, 21, 17, 14, 11, 9, 7, 5]
    grupo_de: dict[int, int] = {}
    G = nx.Graph()
    nodo = 0

    for g, n in enumerate(tamanos):
        miembros = list(range(nodo, nodo + n))
        nodo += n
        for m in miembros:
            grupo_de[m] = g
            G.add_node(m, grupo=g)
        # Enlaces internos densos: cada par se une con probabilidad alta
        for i, a in enumerate(miembros):
            for b in miembros[i + 1:]:
                if rng.random() < 0.28:
                    G.add_edge(a, b, tipo="interno")
        # Garantiza que el grupo sea conexo: sin esto aparecen falsos subgrupos
        for a, b in zip(miembros, miembros[1:]):
            G.add_edge(a, b, tipo="interno")

    # Enlaces entre grupos: escasos, aleatorios
    nodos = list(G.nodes)
    for _ in range(18):
        a, b = rng.choice(nodos, size=2, replace=False)
        if grupo_de[int(a)] != grupo_de[int(b)]:
            G.add_edge(int(a), int(b), tipo="cruzado")

    # Entidades puente: pocas conexiones, pero hacia muchos grupos distintos
    for puente in rng.choice(nodos, size=4, replace=False):
        puente = int(puente)
        destinos = rng.choice(nodos, size=6, replace=False)
        for d in destinos:
            if grupo_de[int(d)] != grupo_de[puente]:
                G.add_edge(puente, int(d), tipo="puente")

    return G, grupo_de


# ─────────────────────────────────────────────────────────────────────────────
# 2. Análisis
# ─────────────────────────────────────────────────────────────────────────────
def detectar_comunidades(G: nx.Graph) -> dict[int, int]:
    """Detección de comunidades por modularidad (Louvain).

    A diferencia de un clustering clásico, NO hay que decirle cuántos grupos
    buscar: la modularidad los determina. Eso es una ventaja real cuando no se
    sabe cuántos grupos económicos hay —que es siempre—.
    """
    comunidades = nx.community.louvain_communities(G, seed=SEMILLA)
    return {n: i for i, com in enumerate(comunidades) for n in com}


def centralidades(G: nx.Graph) -> pd.DataFrame:
    """Tres medidas que responden preguntas distintas.

    - GRADO: ¿con cuántos opera directamente? Mide volumen de relación.
    - INTERMEDIACIÓN: ¿por cuántos caminos más cortos pasa? Mide poder de
      corte — si desaparece, ¿se desconecta la red?
    - VECTOR PROPIO: ¿está conectado a nodos importantes? Mide influencia
      heredada.

    Confundirlas es el error más común. Un nodo de grado bajo puede tener la
    intermediación más alta de la red: es el único puente entre dos grupos, y
    es exactamente el que hay que mirar.
    """
    return pd.DataFrame({
        "grado": pd.Series(dict(G.degree())),
        "intermediacion": pd.Series(nx.betweenness_centrality(G, seed=SEMILLA)),
        "vector_propio": pd.Series(nx.eigenvector_centrality_numpy(G)),
    })


# ─────────────────────────────────────────────────────────────────────────────
# 3. Gráficos
# ─────────────────────────────────────────────────────────────────────────────
def estilo(ax) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(alpha=0.25, linewidth=0.6)
    ax.set_axisbelow(True)


def grafico_red(G: nx.Graph, com: dict[int, int], cent: pd.DataFrame,
                ruta: Path) -> None:
    pos = nx.spring_layout(G, seed=SEMILLA, k=0.42, iterations=180)
    fig, ax = plt.subplots(figsize=(10, 8), dpi=150)

    cruzados = [(u, v) for u, v, d in G.edges(data=True) if d.get("tipo") != "interno"]
    internos = [(u, v) for u, v, d in G.edges(data=True) if d.get("tipo") == "interno"]
    nx.draw_networkx_edges(G, pos, edgelist=internos, alpha=0.18,
                           width=0.7, edge_color=GRIS, ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=cruzados, alpha=0.55,
                           width=1.4, edge_color=ROJO, ax=ax)

    tam = 40 + 1400 * cent["intermediacion"].reindex(list(G.nodes)).to_numpy()
    colores = [PALETA[com[n] % len(PALETA)] for n in G.nodes]
    nx.draw_networkx_nodes(G, pos, node_size=tam, node_color=colores,
                           linewidths=0.6, edgecolors="white", ax=ax)

    # Rotula solo los cinco de mayor intermediación
    top = cent.nlargest(5, "intermediacion").index
    nx.draw_networkx_labels(G, pos, labels={n: f"E{n}" for n in top},
                            font_size=9, font_weight="bold", ax=ax)

    ax.set_title("Comunidades detectadas · el tamaño es intermediación,\n"
                 "las aristas rojas cruzan grupos",
                 fontsize=13, weight="bold", loc="left")
    ax.axis("off")
    fig.tight_layout(); fig.savefig(ruta, bbox_inches="tight"); plt.close(fig)


def grafico_centralidad(cent: pd.DataFrame, ruta: Path) -> None:
    """Grado contra intermediación. Si midieran lo mismo, los puntos caerían en
    una recta. No caen: ahí está el argumento."""
    fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
    ax.scatter(cent["grado"], cent["intermediacion"], s=42, alpha=0.65,
               color=AZUL, edgecolors="white", linewidths=0.6)

    top = cent.nlargest(5, "intermediacion")
    ax.scatter(top["grado"], top["intermediacion"], s=90, color=ROJO,
               edgecolors="white", linewidths=0.8, zorder=5,
               label="Mayor intermediación")
    for n, fila in top.iterrows():
        ax.annotate(f"E{n}", (fila["grado"], fila["intermediacion"]),
                    textcoords="offset points", xytext=(9, 2),
                    fontsize=9, color=ROJO, weight="bold")

    r = np.corrcoef(cent["grado"], cent["intermediacion"])[0, 1]
    ax.set_xlabel("Grado (con cuántos opera directamente)")
    ax.set_ylabel("Intermediación (por cuántos caminos pasa)")
    ax.set_title(f"Estar muy conectado no es lo mismo que ser crítico  ·  r = {r:.2f}",
                 fontsize=12, weight="bold", loc="left")
    ax.legend(frameon=False, fontsize=9)
    estilo(ax)
    fig.tight_layout(); fig.savefig(ruta, bbox_inches="tight"); plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
def main() -> None:
    SALIDA.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEMILLA)

    G, grupo_real = construir_red(rng)
    com = detectar_comunidades(G)
    cent = centralidades(G)

    # ¿Recupera la detección los grupos económicos verdaderos?
    reales = [grupo_real[n] for n in G.nodes]
    detectadas = [com[n] for n in G.nodes]
    from sklearn.metrics import adjusted_rand_score
    ari = adjusted_rand_score(reales, detectadas)
    modularidad = nx.community.modularity(
        G, [{n for n in G.nodes if com[n] == c} for c in set(com.values())])

    grafico_red(G, com, cent, SALIDA / "red-comunidades.png")
    grafico_centralidad(cent, SALIDA / "centralidad.png")

    top = cent.nlargest(6, "intermediacion").copy()
    top["grupo"] = [grupo_real[n] for n in top.index]
    top["grados_del_grupo"] = [
        int(np.median([d for m, d in G.degree() if grupo_real[m] == grupo_real[n]]))
        for n in top.index]
    top.round(4).to_csv(Path(__file__).parent / "centralidad-top.csv")

    print(f"\nRed: {G.number_of_nodes()} entidades, {G.number_of_edges()} relaciones")
    print(f"Grupos económicos reales : {len(set(reales))}")
    print(f"Comunidades detectadas   : {len(set(detectadas))}")
    print(f"Modularidad              : {modularidad:.3f}")
    print(f"Índice de Rand ajustado  : {ari:.3f}")
    print(f"\nCorrelación grado ↔ intermediación: "
          f"{np.corrcoef(cent['grado'], cent['intermediacion'])[0, 1]:.3f}")
    print("\nEntidades más críticas por intermediación\n" + "-" * 68)
    print(top[["grado", "intermediacion", "vector_propio", "grupo"]]
          .to_string(float_format=lambda v: f"{v:,.4f}"))
    print("-" * 68)
    print(f"\nFiguras en {SALIDA}")


if __name__ == "__main__":
    main()
