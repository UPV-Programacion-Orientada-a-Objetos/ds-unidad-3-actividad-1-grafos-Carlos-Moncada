import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Ensure we can import the cython module
sys.path.append(os.getcwd())
try:
    from neuronet import NeuroNet
except ImportError:
    messagebox.showerror("Error", "No se pudo importar el módulo 'neuronet'. Asegúrate de haber compilado la extensión.")
    sys.exit(1)

class NeuroNetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroNet - Análisis de Grafos Masivos")
        self.root.geometry("1000x800")
        
        self.graph_engine = NeuroNet()
        self.loaded = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame de Control
        control_frame = tk.Frame(self.root, padx=10, pady=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Botón Cargar
        self.btn_load = tk.Button(control_frame, text="Cargar Dataset", command=self.load_dataset)
        self.btn_load.pack(side=tk.LEFT, padx=5)
        
        # Etiquetas de Estado
        self.lbl_status = tk.Label(control_frame, text="Estado: Esperando archivo...")
        self.lbl_status.pack(side=tk.LEFT, padx=20)
        
        self.lbl_nodes = tk.Label(control_frame, text="Nodos: 0")
        self.lbl_nodes.pack(side=tk.LEFT, padx=10)
        
        self.lbl_edges = tk.Label(control_frame, text="Aristas: 0")
        self.lbl_edges.pack(side=tk.LEFT, padx=10)
        
        # Frame de Análisis
        analysis_frame = tk.Frame(self.root, padx=10, pady=10, bg="#f0f0f0")
        analysis_frame.pack(side=tk.TOP, fill=tk.X)
        
        tk.Label(analysis_frame, text="Nodo Inicio:", bg="#f0f0f0").pack(side=tk.LEFT)
        self.entry_start = tk.Entry(analysis_frame, width=10)
        self.entry_start.pack(side=tk.LEFT, padx=5)
        
        tk.Label(analysis_frame, text="Profundidad:", bg="#f0f0f0").pack(side=tk.LEFT)
        self.entry_depth = tk.Entry(analysis_frame, width=5)
        self.entry_depth.pack(side=tk.LEFT, padx=5)
        self.entry_depth.insert(0, "2")
        
        self.btn_bfs = tk.Button(analysis_frame, text="Ejecutar BFS", command=self.run_bfs, state=tk.DISABLED)
        self.btn_bfs.pack(side=tk.LEFT, padx=10)
        
        self.btn_max_degree = tk.Button(analysis_frame, text="Nodo Mayor Grado", command=self.find_max_degree, state=tk.DISABLED)
        self.btn_max_degree.pack(side=tk.LEFT, padx=10)
        
        # Área de Visualización
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
    def load_dataset(self):
        filename = filedialog.askopenfilename(title="Seleccionar Dataset", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not filename:
            return
        
        try:
            self.lbl_status.config(text="Cargando...", fg="blue")
            self.root.update()
            
            self.graph_engine.cargar_datos(filename)
            
            num_nodes = self.graph_engine.num_nodos
            num_edges = self.graph_engine.num_aristas
            
            self.lbl_nodes.config(text=f"Nodos: {num_nodes}")
            self.lbl_edges.config(text=f"Aristas: {num_edges}")
            self.lbl_status.config(text=f"Cargado: {os.path.basename(filename)}", fg="green")
            
            self.loaded = True
            self.btn_bfs.config(state=tk.NORMAL)
            self.btn_max_degree.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar archivo: {str(e)}")
            self.lbl_status.config(text="Error", fg="red")

    def run_bfs(self):
        if not self.loaded:
            return
            
        try:
            start_node = int(self.entry_start.get())
            depth = int(self.entry_depth.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese números válidos.")
            return
            
        try:
            visited_nodes = self.graph_engine.bfs(start_node, depth)
            messagebox.showinfo("BFS Resultado", f"Nodos encontrados: {len(visited_nodes)}")
            
            self.visualize_subgraph(visited_nodes, start_node)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en BFS: {str(e)}")

    def find_max_degree(self):
        if not self.loaded:
            return
        
        try:
            node = self.graph_engine.obtener_nodo_mayor_grado()
            degree = self.graph_engine.obtener_grado(node)
            messagebox.showinfo("Mayor Grado", f"Nodo: {node}\nGrado: {degree}")
            
            # Visualize neighborhood of max degree node
            neighbors = self.graph_engine.obtener_vecinos(node)
            nodes_to_draw = [node] + neighbors
            self.visualize_subgraph(nodes_to_draw, node)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    def visualize_subgraph(self, nodes, center_node=None):
        self.ax.clear()
        
        # Limit visualization size to avoid freezing
        if len(nodes) > 1000:
            if not messagebox.askyesno("Advertencia", f"El subgrafo tiene {len(nodes)} nodos. ¿Desea visualizarlo? (Puede ser lento)"):
                return
            # Maybe sample or just show first N
            nodes = nodes[:1000]
        
        # Build NetworkX graph for visualization
        G = nx.Graph()
        
        # We need edges between these nodes. 
        # Since our C++ engine is optimized for traversal, getting all edges for a set of nodes might be slow if we query one by one.
        # But for visualization we need them.
        # Let's iterate over nodes and get their neighbors.
        
        for u in nodes:
            G.add_node(u)
            neighbors = self.graph_engine.obtener_vecinos(u)
            for v in neighbors:
                if v in nodes: # Only add edges within the subgraph
                    G.add_edge(u, v)
        
        pos = nx.spring_layout(G, seed=42)
        
        # Draw
        nx.draw_networkx_nodes(G, pos, ax=self.ax, node_size=50, node_color='lightblue')
        nx.draw_networkx_edges(G, pos, ax=self.ax, alpha=0.5)
        
        if center_node is not None and center_node in G:
            nx.draw_networkx_nodes(G, pos, ax=self.ax, nodelist=[center_node], node_size=100, node_color='red')
            
        self.ax.set_title(f"Visualización ({len(G.nodes)} nodos)")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = NeuroNetApp(root)
    root.mainloop()
