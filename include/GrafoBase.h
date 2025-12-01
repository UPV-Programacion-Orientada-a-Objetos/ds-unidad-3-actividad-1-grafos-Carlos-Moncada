#ifndef GRAFOBASE_H
#define GRAFOBASE_H

#include <vector>
#include <iostream>

class GrafoBase {
public:
    virtual ~GrafoBase() {}
    virtual void cargarDatos(const std::string& archivo) = 0;
    virtual std::vector<int> BFS(int nodoInicio, int profundidad) = 0;
    virtual int obtenerGrado(int nodo) = 0;
    virtual int obtenerNodoMayorGrado() = 0;
};

#endif // GRAFOBASE_H
