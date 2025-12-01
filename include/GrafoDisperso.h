#ifndef GRAFODISPERSO_H
#define GRAFODISPERSO_H

#include "GrafoBase.h"
#include <vector>
#include <string>
#include <algorithm>

class GrafoDisperso : public GrafoBase {
private:
    int numNodos;
    int numAristas;
    
    // CSR format
    std::vector<int> values;      // Not strictly needed for unweighted, but good for completeness
    std::vector<int> col_indices; // Column indices
    std::vector<int> row_ptr;     // Row pointers

public:
    GrafoDisperso();
    ~GrafoDisperso();

    void cargarDatos(const std::string& archivo) override;
    std::vector<int> BFS(int nodoInicio, int profundidad) override;
    int obtenerGrado(int nodo) override;
    int obtenerNodoMayorGrado() override;
    
    // Helper to get neighbors (useful for Python visualization)
    std::vector<int> obtenerVecinos(int nodo);
    
    int getNumNodos() const { return numNodos; }
    int getNumAristas() const { return numAristas; }
};

#endif // GRAFODISPERSO_H
