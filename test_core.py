import sys
import os

# Add current directory to path to find the compiled module
sys.path.append(os.getcwd())

try:
    from neuronet import NeuroNet
    print("Module imported successfully!")
except ImportError as e:
    print(f"Failed to import module: {e}")
    sys.exit(1)

def test_neuronet():
    net = NeuroNet()
    print("NeuroNet instance created.")
    
    data_file = "data/test_graph.txt"
    if not os.path.exists(data_file):
        print(f"File {data_file} not found.")
        return

    print(f"Loading data from {data_file}...")
    net.cargar_datos(data_file)
    
    print(f"Nodes: {net.num_nodos}")
    print(f"Edges: {net.num_aristas}")
    
    assert net.num_nodos > 0
    assert net.num_aristas > 0
    
    print("Testing BFS from node 0, depth 2...")
    visited = net.bfs(0, 2)
    print(f"Visited nodes: {visited}")
    
    # Expected: 0, 1, 2, 3, 4, 5, 6 (depending on order)
    # 0 -> 1, 2 (depth 1)
    # 1 -> 3, 4 (depth 2)
    # 2 -> 5, 6 (depth 2)
    # 3 -> 7 (depth 3 - should not be included if depth is strictly < 2? No, depth 2 usually means distance <= 2)
    # My BFS implementation: dist[v] = dist[u] + 1. If dist[u] >= depth continue.
    # So if depth is 2:
    # u=0 (dist=0). Neighbors 1, 2 get dist 1. Added.
    # u=1 (dist=1). Neighbors 3, 4 get dist 2. Added.
    # u=2 (dist=1). Neighbors 5, 6 get dist 2. Added.
    # u=3 (dist=2). dist[u] >= depth (2>=2) -> continue. Neighbors 7 NOT added.
    # So 7 should NOT be in the list.
    
    assert 7 not in visited
    assert 3 in visited
    
    print("Testing Degree...")
    deg0 = net.obtener_grado(0)
    print(f"Degree of node 0: {deg0}")
    assert deg0 == 2
    
    print("Testing Max Degree...")
    max_node = net.obtener_nodo_mayor_grado()
    print(f"Node with max degree: {max_node}")
    # Node 0: 2, Node 1: 2, Node 2: 2. Could be any of them depending on implementation.
    
    print("Test Passed!")

if __name__ == "__main__":
    test_neuronet()
