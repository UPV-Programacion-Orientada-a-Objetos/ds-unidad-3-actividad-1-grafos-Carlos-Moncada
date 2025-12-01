#include "../include/GrafoDisperso.h"
#include <fstream>
#include <sstream>
#include <iostream>
#include <queue>
#include <algorithm>
#include <limits>
#include <chrono>

GrafoDisperso::GrafoDisperso() : numNodos(0), numAristas(0) {}

GrafoDisperso::~GrafoDisperso() {}

void GrafoDisperso::cargarDatos(const std::string& archivo) {
    std::cout << "[C++ Core] Inicializando GrafoDisperso..." << std::endl;
    std::cout << "[C++ Core] Cargando dataset '" << archivo << "'..." << std::endl;
    std::ifstream file(archivo);
    if (!file.is_open()) {
        std::cerr << "Error al abrir el archivo: " << archivo << std::endl;
        return;
    }

    // Pass 1: Determine number of nodes and degrees
    int maxNodeId = -1;
    int u, v;
    std::string line;
    
    // Temporary degree count
    // Since we don't know numNodes yet, we might need a map or a dynamic vector.
    // However, for efficiency with known benchmarks, nodes are usually 0 to N-1.
    // Let's assume we can resize vector as we go or use a map if IDs are very sparse.
    // Given the requirement "Matrices poco densas", usually implies contiguous or near-contiguous IDs.
    // Let's assume contiguous IDs for now, but handle resizing.
    
    std::vector<int> degrees;
    
    while (std::getline(file, line)) {
        if (line.empty() || line[0] == '#') continue;
        std::stringstream ss(line);
        if (ss >> u >> v) {
            maxNodeId = std::max(maxNodeId, std::max(u, v));
            if (degrees.size() <= maxNodeId) {
                degrees.resize(maxNodeId + 1, 0);
            }
            degrees[u]++;
            // If undirected, we would add degrees[v]++ too. 
            // The README example shows "0 11342", "1 0". It seems directed or at least edges are listed.
            // "web-Google.txt" is directed.
            // Let's assume the file contains all edges. If it's undirected, usually both (u,v) and (v,u) are present or we treat it as directed.
            // The prompt says "Grafo dirigido y no dirigido" in topics, but let's stick to the file format.
            // Usually SNAP web-Google is directed.
        }
    }

    numNodos = maxNodeId + 1;
    numAristas = 0; // Will count in pass 2 or just sum degrees

    // Initialize row_ptr
    row_ptr.resize(numNodos + 1);
    row_ptr[0] = 0;
    for (int i = 0; i < numNodos; ++i) {
        row_ptr[i + 1] = row_ptr[i] + degrees[i];
    }
    numAristas = row_ptr[numNodos];

    // Allocate col_indices
    col_indices.resize(numAristas);
    
    // Reset file for Pass 2
    file.clear();
    file.seekg(0, std::ios::beg);
    
    // Temporary vector to keep track of where we are inserting in each row
    std::vector<int> current_pos = row_ptr;

    while (std::getline(file, line)) {
        if (line.empty() || line[0] == '#') continue;
        std::stringstream ss(line);
        if (ss >> u >> v) {
            col_indices[current_pos[u]] = v;
            current_pos[u]++;
        }
    }
    
    file.close();
    std::cout << "[C++ Core] Carga completa. Nodos: " << numNodos << " | Aristas: " << numAristas << std::endl;
    
    // Estimate memory: 3 vectors of ints. 
    // values (numAristas) + col_indices (numAristas) + row_ptr (numNodos+1)
    // 4 bytes per int.
    long long memory_bytes = (long long)numAristas * 4 * 2 + (long long)(numNodos + 1) * 4;
    double memory_mb = memory_bytes / (1024.0 * 1024.0);
    std::cout << "[C++ Core] Estructura CSR construida. Memoria estimada: " << memory_mb << " MB." << std::endl;
}

std::vector<int> GrafoDisperso::BFS(int nodoInicio, int profundidad) {
    std::cout << "[C++ Core] Ejecutando BFS nativo..." << std::endl;
    // Simple timer
    auto start = std::chrono::high_resolution_clock::now();

    std::vector<int> visitados;
    if (nodoInicio < 0 || nodoInicio >= numNodos) return visitados;

    std::vector<int> dist(numNodos, -1);
    std::queue<int> q;

    q.push(nodoInicio);
    dist[nodoInicio] = 0;
    visitados.push_back(nodoInicio);

    while (!q.empty()) {
        int u = q.front();
        q.pop();

        if (dist[u] >= profundidad) continue;

        for (int i = row_ptr[u]; i < row_ptr[u + 1]; ++i) {
            int v = col_indices[i];
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                visitados.push_back(v);
                q.push(v);
            }
        }
    }
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> elapsed = end - start;
    std::cout << "[C++ Core] Nodos encontrados: " << visitados.size() << ". Tiempo ejecución: " << elapsed.count() << "ms." << std::endl;
    return visitados;
}

int GrafoDisperso::obtenerGrado(int nodo) {
    if (nodo < 0 || nodo >= numNodos) return 0;
    return row_ptr[nodo + 1] - row_ptr[nodo];
}

int GrafoDisperso::obtenerNodoMayorGrado() {
    int maxGrado = -1;
    int maxNodo = -1;
    for (int i = 0; i < numNodos; ++i) {
        int grado = obtenerGrado(i);
        if (grado > maxGrado) {
            maxGrado = grado;
            maxNodo = i;
        }
    }
    return maxNodo;
}

std::vector<int> GrafoDisperso::obtenerVecinos(int nodo) {
    std::vector<int> vecinos;
    if (nodo < 0 || nodo >= numNodos) return vecinos;
    
    for (int i = row_ptr[nodo]; i < row_ptr[nodo + 1]; ++i) {
        vecinos.push_back(col_indices[i]);
    }
    return vecinos;
}
