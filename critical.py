import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict

def preparar_dados(df):
    df['Folga'] = df['Late Start'] - df['Early Start']
    df['Crítico'] = df['Folga'] == 0
    return df

def construir_grafo(df):
    G = nx.DiGraph()
    for idx, row in df.iterrows():
        G.add_node(row['Item'], **row.to_dict())
        if row['Precedência'] != 'Início':
            G.add_edge(row['Precedência'], row['Item'])
    return G

def calcular_niveis(G):
    levels = {}
    for node in nx.topological_sort(G):
        preds = list(G.predecessors(node))
        if preds:
            levels[node] = max([levels[p] for p in preds]) + 1
        else:
            levels[node] = 0
    return levels

def gerar_posicao_customizada(G):
    levels = calcular_niveis(G)
    level_nodes = defaultdict(list)
    for node, lvl in levels.items():
        level_nodes[lvl].append(node)

    pos = {}
    for lvl, nodes in level_nodes.items():
        nodes_sorted = sorted(nodes)  # Para manter consistência
        y_positions = list(range(len(nodes_sorted)))
        y_centered = [y - (len(nodes_sorted) - 1) / 2 for y in y_positions]  # Centraliza no eixo Y
        for y, node in zip(y_centered, nodes_sorted):
            pos[node] = (lvl * 4, -y * 3)  # 4 de espaço horizontal, 3 de espaço vertical

    return pos

def desenhar_diagrama(G, pos):
    fig, ax = plt.subplots(figsize=(20, 10))

    # Desenhar arestas
    for u, v in G.edges():
        u_critico = G.nodes[u]['Crítico']
        v_critico = G.nodes[v]['Crítico']
        color = 'red' if u_critico and v_critico else 'black'
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color=color, arrows=True, arrowsize=20, connectionstyle='arc3,rad=0.2')

    # Desenhar nós
    for node in G.nodes():
        data = G.nodes[node]
        x, y = pos[node]
        cor_borda = 'red' if data['Crítico'] else 'black'

        # Desenha o retângulo
        bbox = dict(boxstyle="round,pad=0.5", edgecolor=cor_borda, facecolor='white', linewidth=2)
        texto = (f"{node}\n"
                 f"ES:{data['Early Start']}  EF:{data['Early Finish']}\n"
                 f"LS:{data['Late Start']}  LF:{data['Late Finish']}\n"
                 f"Folga:{data['Folga']}")
        ax.text(x, y, texto, ha='center', va='center', bbox=bbox, fontsize=9)

    ax.axis('off')
    plt.title('Método do Caminho Crítico - Diagrama Horizontal', fontsize=18)
    plt.tight_layout()
    plt.savefig('diagrama_horizontal.png', bbox_inches='tight', dpi=300)
    plt.show()

# Dados de exemplo
data = {
    'Item': ['I', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I2', 'J', 'K', 'L', 'F2'],
    'Early Start': [0, 1, 1, 1, 7, 9, 3, 4, 10, 8, 8, 16, 14, 16],
    'Early Finish': [1, 4, 2, 3, 16, 12, 4, 7, 14, 15, 13, 19, 15, 19],
    'Late Start': [1, 4, 1, 1, 10, 9, 3, 4, 10, 8, 8, 16, 14, 16],
    'Late Finish': [0, 9, 2, 3, 19, 12, 4, 7, 14, 15, 13, 19, 15, 19],
    'Precedência': ['Início', 'I', 'I', 'I', 'A', 'A', 'B', 'C', 'E', 'E', 'I2', 'I2', 'H', 'K']
}

# Rodar tudo
df = pd.DataFrame(data)
df = preparar_dados(df)
G = construir_grafo(df)
pos = gerar_posicao_customizada(G)
desenhar_diagrama(G, pos)
