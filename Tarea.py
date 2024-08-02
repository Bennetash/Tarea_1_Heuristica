import networkx as nx
import matplotlib.pyplot as plt
import random
import folium

# Direcciones de los hogares
direcciones = [
    "Av. Providencia 1234",
    "Av. Apoquindo 5678",
    "Av. Libertador Bernardo O'Higgins 9101",
    "Av. Irarrázaval 1123",
    "Av. Vicuña Mackenna 1415",
    "Av. Matta 1617",
    "Av. Manuel Montt 1820",
    "Av. Tobalaba 2122",
    "Av. La Florida 2324",
    "Av. Pajaritos 2526",
    "Av. Américo Vespucio 2728",
    "Av. Las Condes 2930",
    "Av. Recoleta 3132",
    "Av. Independencia 3334",
    "Av. Grecia 3536"
]

# Coordenadas aproximadas de las direcciones (latitud, longitud)
coordenadas = [
    (-33.4263, -70.6266),  # Av. Providencia 1234
    (-33.4075, -70.5790),  # Av. Apoquindo 5678
    (-33.4429, -70.6530),  # Av. Libertador Bernardo O'Higgins 9101
    (-33.4578, -70.6107),  # Av. Irarrázaval 1123
    (-33.4630, -70.6110),  # Av. Vicuña Mackenna 1415
    (-33.4663, -70.6295),  # Av. Matta 1617
    (-33.4274, -70.6187),  # Av. Manuel Montt 1820
    (-33.4489, -70.5610),  # Av. Tobalaba 2122
    (-33.5132, -70.5889),  # Av. La Florida 2324
    (-33.4511, -70.7332),  # Av. Pajaritos 2526
    (-33.4965, -70.6188),  # Av. Américo Vespucio 2728
    (-33.4160, -70.5708),  # Av. Las Condes 2930
    (-33.4047, -70.6394),  # Av. Recoleta 3132
    (-33.4257, -70.6543),  # Av. Independencia 3334
    (-33.4703, -70.5868)   # Av. Grecia 3536
]

# Generar una matriz de distancias aleatoria para 15 hogares
def generar_matriz_distancia(size=15):
    matrix = [[random.randint(1, 20) if i != j else 0 for j in range(size)] for i in range(size)]
    return matrix

# Crear un grafo a partir de la matriz de distancias
def crear_grafo(matrix, direcciones):
    G = nx.Graph()
    size = len(matrix)
    for i in range(size):
        for j in range(size):
            if i != j:
                G.add_edge(direcciones[i], direcciones[j], weight=matrix[i][j])
    return G

# Crear un árbol de cobertura usando búsqueda en anchura (BFS)
def bfs_tree(G, start_node):
    return nx.bfs_tree(G, start_node)

# Crear un árbol de cobertura usando búsqueda en profundidad (DFS)
def dfs_tree(G, start_node):
    return nx.dfs_tree(G, start_node)

# Calcular el costo de un árbol
def calcular_costo_arbol(tree):
    return tree.size(weight='weight')

# Dibujar el grafo y el árbol de cobertura
def dibujar_grafo_y_arbol(G, tree, title):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))

    # Dibujar grafo completo
    nx.draw(G, pos, with_labels=True, labels={node: node for node in G.nodes()}, node_color='lightblue', node_size=500, edge_color='gray', alpha=0.5)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Dibujar árbol de cobertura
    nx.draw(tree, pos, with_labels=True, labels={node: node for node in tree.nodes()}, node_color='lightgreen', node_size=500, edge_color='blue', width=2)
    
    plt.title(title)
    plt.show()

# Mostrar el árbol de cobertura en un mapa de Santiago usando folium
def mostrar_arbol_en_mapa(tree, coordenadas, direcciones, title):
    map_center = (-33.45, -70.65)  # Centro aproximado de Santiago
    m = folium.Map(location=map_center, zoom_start=12)
    
    # Agregar marcadores para cada dirección
    for address, coord in zip(direcciones, coordenadas):
        folium.Marker(location=coord, popup=address).add_to(m)
    
    # Dibujar las rutas del árbol de cobertura
    for edge in tree.edges():
        start, end = edge
        if start in direcciones and end in direcciones:
            start_idx = direcciones.index(start)
            end_idx = direcciones.index(end)
            folium.PolyLine([coordenadas[start_idx], coordenadas[end_idx]], color="blue", weight=2.5, opacity=1).add_to(m)
    
    # Guardar y mostrar el mapa
    m.save(f"{title}.html")
    return m

# Matriz de distancias
distance_matrix = generar_matriz_distancia()
print("Matriz de Distancias:")
for row in distance_matrix:
    print(row)

# Crear grafo
G = crear_grafo(distance_matrix, direcciones)

# Nodo raíz (puede ser cualquier nodo, aquí seleccionamos uno aleatoriamente)
start_node = random.choice(direcciones)

# Árboles de cobertura usando BFS y DFS
bfs_cov_tree = bfs_tree(G, start_node)
dfs_cov_tree = dfs_tree(G, start_node)

# Costos de los árboles
bfs_cost = calcular_costo_arbol(bfs_cov_tree)
dfs_cost = calcular_costo_arbol(dfs_cov_tree)

# Dibujar y mostrar los resultados
print(f"Nodo raíz: {start_node}")
print(f"BFS Costo del Arbol: {bfs_cost}")
print(f"DFS Costo del Arbol: {dfs_cost}")

dibujar_grafo_y_arbol(G, bfs_cov_tree, f"Arbol de cobertura BFS (Costo: {bfs_cost})")
dibujar_grafo_y_arbol(G, dfs_cov_tree, f"Arbol de cobertura DFS (Costo: {dfs_cost})")

# Mostrar los árboles en el mapa de Santiago
bfs_map = mostrar_arbol_en_mapa(bfs_cov_tree, coordenadas, direcciones, f"Arbol de cobertura BFS (Costo: {bfs_cost})")
dfs_map = mostrar_arbol_en_mapa(dfs_cov_tree, coordenadas, direcciones, f"Arbol de cobertura DFS (Costo: {dfs_cost})")

# Mostrar mapas en el notebook (opcional, si estás usando Jupyter Notebook)
# from IPython.display import IFrame
# IFrame("BFS_Coverage_Tree.html", width=700, height=500)
# IFrame("DFS_Coverage_Tree.html", width=700, height=500)