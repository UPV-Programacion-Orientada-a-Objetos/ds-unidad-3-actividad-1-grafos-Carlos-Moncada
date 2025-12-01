from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "../include/GrafoDisperso.h":
    cdef cppclass GrafoDisperso:
        GrafoDisperso() except +
        void cargarDatos(string archivo)
        vector[int] BFS(int nodoInicio, int profundidad)
        int obtenerGrado(int nodo)
        int obtenerNodoMayorGrado()
        vector[int] obtenerVecinos(int nodo)
        int getNumNodos()
        int getNumAristas()
