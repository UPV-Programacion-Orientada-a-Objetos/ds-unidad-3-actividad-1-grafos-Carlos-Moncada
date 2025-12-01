# distutils: language = c++

from neuronet_core cimport GrafoDisperso
from libcpp.string cimport string
from libcpp.vector cimport vector

cdef class NeuroNet:
    cdef GrafoDisperso* c_grafo  # Hold a pointer to the C++ instance

    def __cinit__(self):
        self.c_grafo = new GrafoDisperso()

    def __dealloc__(self):
        del self.c_grafo

    def cargar_datos(self, archivo: str):
        """Carga un dataset desde un archivo de texto."""
        cdef string c_archivo = archivo.encode('utf-8')
        self.c_grafo.cargarDatos(c_archivo)

    def bfs(self, nodo_inicio: int, profundidad: int):
        """Ejecuta BFS desde un nodo dado hasta cierta profundidad."""
        print(f"[Cython] Solicitud recibida: BFS desde Nodo {nodo_inicio}, Profundidad {profundidad}.")
        result = self.c_grafo.BFS(nodo_inicio, profundidad)
        print("[Cython] Retornando lista de adyacencia local a Python.")
        return result

    def obtener_grado(self, nodo: int):
        """Obtiene el grado de un nodo."""
        return self.c_grafo.obtenerGrado(nodo)

    def obtener_nodo_mayor_grado(self):
        """Retorna el ID del nodo con mayor grado."""
        return self.c_grafo.obtenerNodoMayorGrado()

    def obtener_vecinos(self, nodo: int):
        """Retorna los vecinos directos de un nodo."""
        return self.c_grafo.obtenerVecinos(nodo)
    
    @property
    def num_nodos(self):
        return self.c_grafo.getNumNodos()
    
    @property
    def num_aristas(self):
        return self.c_grafo.getNumAristas()
