import sys
import os
import time

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from neuronet import NeuroNet
except ImportError:
    print("Error: Could not import NeuroNet. Make sure it is compiled.")
    sys.exit(1)

def test_google():
    print("=== Testing NeuroNet with web-Google.txt ===")
    net = NeuroNet()
    
    data_file = "data/web-Google.txt"
    if not os.path.exists(data_file):
        print(f"File {data_file} not found. Please download it.")
        return

    print(f"Loading {data_file}...")
    start_time = time.time()
    net.cargar_datos(data_file)
    end_time = time.time()
    print(f"Load time: {end_time - start_time:.4f} seconds")
    
    print(f"Nodes: {net.num_nodos}")
    print(f"Edges: {net.num_aristas}")
    
    print("\n--- Running BFS from Node 0, Depth 2 ---")
    visited = net.bfs(0, 2)
    print(f"Visited count: {len(visited)}")
    
    print("\n--- Finding Max Degree Node ---")
    start_time = time.time()
    max_node = net.obtener_nodo_mayor_grado()
    end_time = time.time()
    degree = net.obtener_grado(max_node)
    print(f"Max Degree Node: {max_node} (Degree: {degree})")
    print(f"Calculation time: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    test_google()
