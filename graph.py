import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.artist import Artist
from matplotlib.lines import Line2D
from matplotlib.patches import Patch



def init_graph(criteria,edges):
    G = nx.DiGraph()

    for key, label in criteria.items():
        G.add_node(key, label=label)


    for source, target, weight in edges:
        G.add_edge(source, target, weight=weight)

    return  G



def build_weighted_graph(W, nodes):
        G = nx.DiGraph()
        G.add_nodes_from(nodes)

        for i, u in enumerate(nodes):
            for j, v in enumerate(nodes):

                if W[i, j] != 0:
                    G.add_edge(u, v, weight=W[i, j])

        return G



def initialize_weight_matrix(G, seed=42):

    rng = np.random.default_rng(seed)

    nodes = sorted(G.nodes(), key=lambda x: int(x[1:]))
    n = len(nodes)

    W0 = np.zeros((n,n))

    index = {node:i for i,node in enumerate(nodes)}

    for u,v,data in G.edges(data=True):

        i = index[u]
        j = index[v]

        if data["weight"] > 0:
            W0[i,j] = rng.uniform(0,1)
        else:
            W0[i,j] = rng.uniform(-1,0)

    return W0, nodes


def plot_fcm(
    G,
    benefit_vector,
    position = None,
    edge_type="sign",
    weight_decimals=2,
    edge_label_fontsize=14,
    node_label_fontsize=11,
    edge_width=2.0,
    node_size=3000,
    manual_adjust_right=True
):
    """
    Plot della Fuzzy Cognitive Map.

    Parameters
    ----------
    G : nx.DiGraph
        Grafo diretto con attributo 'weight' sugli archi.
    benefit_vector : list
        Lista che identifica i criteri benefit (1) e cost (0).
    edge_type : str
        'sign'    -> mostra solo + e -
        'weights' -> mostra i pesi sugli archi; linea continua per pesi positivi,
                     tratteggiata per pesi negativi
        'abs'     -> mostra il valore assoluto dei pesi
    weight_decimals : int
        Numero di cifre decimali nelle etichette degli archi.
    edge_label_fontsize : int
        Dimensione del font delle etichette degli archi.
    node_label_fontsize : int
        Dimensione del font delle etichette dei nodi.
    edge_width : float
        Spessore costante degli archi.
    node_size : int
        Dimensione dei nodi.
    manual_adjust_right : bool
        Se True, applica piccoli aggiustamenti manuali ai nodi sul lato destro.
    """

    if edge_type not in {"sign", "weights", "abs"}:
        raise ValueError("edge_type deve essere uno tra: 'sign', 'weights', 'abs'")

    plt.figure(figsize=(18, 14))

    if position is None:
        pos = nx.kamada_kawai_layout(G, scale=4)
    else:
        pos = position

    if manual_adjust_right:
        for node, dx, dy in [
            ("C2", 0.18, 0.05),
            ("C3", 0.10, 0.12),
            ("C1", 0.15, -0.05),
            ("C18", 0.10, -0.12),
            ("C17", 0.05, -0.05),
        ]:
            if node in pos:
                pos[node][0] += dx
                pos[node][1] += dy

    nodes = list(G.nodes())
    edges = list(G.edges())

    node_colors = [
        "lightgreen" if benefit_vector[i] == 1 else "lightcoral"
        for i in range(len(nodes))
    ]

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=node_size,
        node_color=node_colors,
        edgecolors="black",
        linewidths=1.2
    )

    nx.draw_networkx_labels(
        G,
        pos,
        font_size=node_label_fontsize,
        font_weight="bold"
    )

    if edge_type == "sign":
        edge_labels = {
            (u, v): "+" if G[u][v]["weight"] > 0 else "-"
            for u, v in edges
        }
    elif edge_type == "weights":
        # Mostra solo il valore assoluto; il segno è rappresentato dallo stile della linea
        edge_labels = {
            (u, v): f"{abs(G[u][v]['weight']):.{weight_decimals}f}"
            for u, v in edges
        }
    else:  # abs
        edge_labels = {
            (u, v): f"{abs(G[u][v]['weight']):.{weight_decimals}f}"
            for u, v in edges
        }

    if edge_type == "weights":
        positive_edges = [(u, v) for u, v in edges if G[u][v]["weight"] >= 0]
        negative_edges = [(u, v) for u, v in edges if G[u][v]["weight"] < 0]

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=positive_edges,
            arrows=True,
            arrowstyle="-|>",
            arrowsize=30,
            width=edge_width,
            edge_color="black",
            style="solid",
            min_source_margin=15,
            min_target_margin=25
        )

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=negative_edges,
            arrows=True,
            arrowstyle="-|>",
            arrowsize=30,
            width=edge_width,
            edge_color="black",
            style="dashed",
            min_source_margin=15,
            min_target_margin=25
        )
    else:
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=edges,
            arrows=True,
            arrowstyle="-|>",
            arrowsize=30,
            width=edge_width,
            edge_color="black",
            style="solid",
            min_source_margin=15,
            min_target_margin=25
        )

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=edge_label_fontsize,
        font_weight="bold",
        label_pos=0.60,
        rotate=True,
        bbox=dict(
            facecolor="white",
            edgecolor="gray",
            boxstyle="square,pad=0.08",
            alpha=0.85
        )
    )

    patch_handles = [
        Patch(facecolor="lightgreen", edgecolor="black", label="Benefit Criteria"),
        Patch(facecolor="lightcoral", edgecolor="black", label="Cost Criteria"),
    ]

    line_handles = []
    if edge_type == "weights":
        line_handles = [
            Line2D([0], [0], color="black", lw=2.0, linestyle="solid",
                   label="Positive Influence"),
            Line2D([0], [0], color="black", lw=2.0, linestyle="dashed",
                   label="Negative Influence")
        ]

    legend_elements: list[Artist] = patch_handles + line_handles

    plt.legend(
        handles=legend_elements,
        loc="upper left",
        bbox_to_anchor=(-0.02, 1.0),
        fontsize=14,
        title="Legend",
        title_fontsize=16,
        borderpad=1.2
    )

    title_map = {
        "sign": "Causal Graph",
        "weights": "Weighted Fuzzy Cognitive Map Graph",
        "abs": "Reversed Absolute Valued Graph for Centrality Computation",
    }

    plt.title(title_map[edge_type], fontsize=18)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

    return pos