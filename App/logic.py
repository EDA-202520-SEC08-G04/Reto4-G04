import csv
import math
import time
import os
import sys
from datetime import datetime
from DataStructures.List import array_list as lt
from DataStructures.Map import map_linear_probing as mp
import DataStructures.Graph.digraph as G
from DataStructures.Graph import dfs as dfs
from DataStructures.Graph import dfo as df
from DataStructures.Graph import dijkstra as dih
from DataStructures.Graph import dfs as dfs
from DataStructures.Priority_queue import priority_queue as pq
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def new_logic():
    grafo_dist = G.new_graph(2000)
    grafo_agua = G.new_graph(2000)
    catalog = {
        "grafo_distancia": grafo_dist,
        "grafo_agua": grafo_agua,
        "mapa_eventos": mp.new_map(25000, 0.5),
        "lista_eventos": lt.new_list(),
        "total_grullas": 0,
        "total_eventos": 0,
        "nodos_por_tag": {},
        "posiciones_nodos": []
    }
    return catalog


def load_data(catalog, filename):
    filepath = os.path.join("Data", filename)

    events_py = []
    tags_vistos = set()

    with open(filepath, mode="r", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row is None:
                continue

            row = {k.strip(): v for k, v in row.items() if k is not None}

            fecha_str = row["timestamp"].strip()
            try:
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S.%f")
            except Exception:
                fecha = datetime.strptime(fecha_str.split('.')[0], "%Y-%m-%d %H:%M:%S")

            dist_agua = 0.0
            raw_comment = row.get("comments", "")
            if raw_comment:
                clean = raw_comment.replace('"', "").replace("'", "").strip()
                if clean:
                    try:
                        dist_agua = float(clean)
                    except ValueError:
                        pass

            tag = row["tag-local-identifier"].strip()

            evento = {
                "id": row["event-id"],
                "lat": float(row["location-lat"]),
                "lon": float(row["location-long"]),
                "timestamp": fecha,
                "tag_id": tag,
                "water_dist": dist_agua
            }

            events_py.append(evento)
            tags_vistos.add(tag)

    catalog["total_grullas"] = len(tags_vistos)
    catalog["total_eventos"] = len(events_py)

    events_py.sort(key=lambda e: e["timestamp"])

    lista = catalog["lista_eventos"]
    for ev in events_py:
        lt.add_last(lista, ev)

    eventos_por_tag = {}
    for ev in events_py:
        tag = ev["tag_id"]
        if tag not in eventos_por_tag:
            eventos_por_tag[tag] = []
        eventos_por_tag[tag].append(ev)

    grafo_dist = catalog["grafo_distancia"]
    grafo_agua = catalog["grafo_agua"]

    nodos_por_id = {}
    event_to_node = {}
    seq_nodos_por_tag = {}
    posiciones_nodos = []
    nodos_por_tag = {}

    for tag, eventos_tag in eventos_por_tag.items():
        nodo_actual = None
        seq_nodos = []

        for evento in eventos_tag:
            crear_nodo = True

            if nodo_actual is not None:
                dist = haversine(
                    evento["lat"], evento["lon"],
                    nodo_actual["lat"], nodo_actual["lon"]
                )
                dt_h = abs((evento["timestamp"] - nodo_actual["creation_time"]).total_seconds()) / 3600.0

                if dist < 3.0 and dt_h < 3.0:
                    crear_nodo = False

            if crear_nodo:
                node_id = evento["id"]

                nodo_info = {
                    "id": node_id,
                    "lat": evento["lat"],
                    "lon": evento["lon"],
                    "creation_time": evento["timestamp"],
                    "events_py": [evento["id"]],
                    "tags_py": [tag],
                    "tags_set": {tag},
                    "event_count": 1,
                    "water_sum": evento["water_dist"]
                }

                G.insert_vertex(grafo_dist, node_id, nodo_info)
                G.insert_vertex(grafo_agua, node_id, nodo_info)

                nodos_por_id[node_id] = nodo_info
                nodo_actual = nodo_info
                seq_nodos.append(node_id)

                posiciones_nodos.append((evento["lat"], evento["lon"], node_id))

                if tag not in nodos_por_tag:
                    nodos_por_tag[tag] = []
                nodos_por_tag[tag].append(node_id)
            else:
                nodo_actual["events_py"].append(evento["id"])
                nodo_actual["event_count"] += 1
                nodo_actual["water_sum"] += evento["water_dist"]

                if tag not in nodo_actual["tags_set"]:
                    nodo_actual["tags_set"].add(tag)
                    nodo_actual["tags_py"].append(tag)

            event_to_node[evento["id"]] = nodo_actual["id"]

        seq_nodos_por_tag[tag] = seq_nodos

    for nodo in nodos_por_id.values():
        ev_list = lt.new_list()
        for eid in nodo["events_py"]:
            lt.add_last(ev_list, eid)
        nodo["events"] = ev_list

        tags_list = lt.new_list()
        for t in nodo["tags_py"]:
            lt.add_last(tags_list, t)
        nodo["tags"] = tags_list

    mapa_eventos = catalog["mapa_eventos"]
    for eid, node_id in event_to_node.items():
        mp.put(mapa_eventos, eid, node_id)

    for tag, seq in seq_nodos_por_tag.items():
        for i in range(1, len(seq)):
            origen_id = seq[i - 1]
            destino_id = seq[i]

            if origen_id == destino_id:
                continue

            info_o = nodos_por_id[origen_id]
            info_d = nodos_por_id[destino_id]

            w_dist = haversine(
                info_o["lat"], info_o["lon"],
                info_d["lat"], info_d["lon"]
            )
            G.add_edge(grafo_dist, origen_id, destino_id, w_dist)

            if info_d["event_count"] > 0:
                w_water = info_d["water_sum"] / info_d["event_count"]
            else:
                w_water = 0.0
            G.add_edge(grafo_agua, origen_id, destino_id, w_water)

    catalog["posiciones_nodos"] = posiciones_nodos
    catalog["nodos_por_tag"] = nodos_por_tag

def nodo_mas_cercano(grafo, lat, lon):
    vertices = G.vertices(grafo)  # lista EDA (array_list)

    best_node = None
    best_dist = float("inf")

    # recorrer usando la API de array_list
    for idx in range(lt.size(vertices)):
        vid = lt.get_element(vertices, idx)
        info = G.get_vertex_information(grafo, vid)
        d = haversine(lat, lon, info["lat"], info["lon"])

        if d < best_dist:
            best_dist = d
            best_node = vid

    return best_node

def nodos_visitados_por_grulla(lista_eventos, grulla_id, mapa_eventos):
    nodos = []
    size = lt.size(lista_eventos)
    for i in range(0, size):
        e = lt.get_element(lista_eventos, i)
        if e["tag_id"] == grulla_id:
            nodo = mp.get(mapa_eventos, e["id"])
            if nodo is not None:
                nodos.append(nodo)
    return nodos

def req_1(catalog, lat_or, lon_or, lat_dest, lon_dest, grulla_id):

    """
    Retorna el resultado del requerimiento 1
    """
    grafo = catalog["grafo_distancia"]
    lista_eventos = catalog["lista_eventos"]
    mapa_eventos = catalog["mapa_eventos"]

    # 1. nodos más cercanos
    nodo_origen = nodo_mas_cercano(grafo, lat_or, lon_or)
    nodo_destino = nodo_mas_cercano(grafo, lat_dest, lon_dest)

    # 2. nodos visitados por la grulla (para verificar si existe)
    nodos_grulla = nodos_visitados_por_grulla(lista_eventos, grulla_id, mapa_eventos)
    if nodo_origen not in nodos_grulla["elements"]:
        return {"error": f"La grulla {grulla_id} no pasó por el nodo origen."}

    # 3. DFS normal
    
    search = G.contains_vertex(grafo, nodo_origen)
    print("--------------")
    print(grafo)
    print("--------------")
    if not dfs.has_path_to( str(nodo_destino),grafo):
        
        return {"error": "No existe un camino viable entre los puntos."}

    ruta = dfs.path_to(search, nodo_destino)
    ruta = list(ruta)  # pila → lista

    # 4. calcular distancias
    dist_total = 0
    distancias = []
    for i in range(len(ruta)-1):
        A = G.get_vertex_information(grafo, ruta[i])
        B = G.get_vertex_information(grafo, ruta[i+1])
        d = haversine(A["lat"], A["lon"], B["lat"], B["lon"])
        dist_total += d
        distancias.append(d)

    # 5. preparar información detallada
    detalles = []
    for i, vid in enumerate(ruta):
        info = G.get_vertex_information(grafo, vid)
        tags = [lt.get_element(info["tags"], j)
                for j in range(1, lt.size(info["tags"])+1)]

        detalles.append({
            "id": vid,
            "lat": info["lat"],
            "lon": info["lon"],
            "num_grullas": len(tags),
            "tags_preview": tags[:3] + tags[-3:] if len(tags) > 6 else tags,
            "dist_next": distancias[i] if i < len(distancias) else 0
        })

    return {
        "nodo_inicio_grulla": nodos_grulla[0],  # primer punto migratorio real de la grulla
        "distancia_total": dist_total,
        "total_puntos": len(ruta),
        "primeros_5": detalles[:5],
        "ultimos_5": detalles[-5:]
    }


def req_2(catalog, lat_origen, lon_origen, lat_destino, lon_destino, radio_km):
    """
    Retorna el resultado del requerimiento 2
    """
    
    grafo = catalog["grafo_distancia"]
    vertices_grafo = G.vertices(grafo)

    nodo_origen = None
    min_dist_origen = float('inf')
    for i in vertices_grafo["elements"]:
        info = G.get_vertex_information(grafo, i)
        d = haversine(lat_origen, lon_origen, info["lat"], info["lon"])
        if d < min_dist_origen:
            min_dist_origen = d
            nodo_origen = i

    nodo_destino = None
    min_dist_destino = float('inf')
    for i in vertices_grafo["elements"]:
        info = G.get_vertex_information(grafo, i)
        d = haversine(lat_destino, lon_destino, info["lat"], info["lon"])
        if d < min_dist_destino:
            min_dist_destino = d
            nodo_destino = i

    visitados = mp.new_map(num_elements=G.order(grafo), load_factor=0.5)
    mp.put(visitados, nodo_origen, {'marked': True, 'edge_from': None})
    cola = lt.new_list()
    lt.add_last(cola, nodo_origen)

    ultimo_dentro_radio = nodo_origen

    while lt.size(cola) > 0:
        actual = lt.get_element(cola, 0)
        lt.delete_element(cola, 0)

        info_actual = G.get_vertex_information(grafo, actual)
        distancia_al_origen = haversine(lat_origen, lon_origen, info_actual["lat"], info_actual["lon"])
        if distancia_al_origen <= radio_km:
            ultimo_dentro_radio = actual

        adjs = G.adjacents(grafo, actual)
        for j in adjs["elements"]:
            if not mp.contains(visitados, j):
                lt.add_last(cola, j)
                mp.put(visitados, j, {'marked': True, 'edge_from': actual})

    if not mp.contains(visitados, nodo_destino):
        return {"error": "No existe un camino viable entre los puntos."}

    camino = lt.new_list()
    v = nodo_destino
    while v is not None:
        lt.add_first(camino, v)
        info_v = mp.get(visitados, v)
        if info_v is None:
            v = None
        else:
            v = info_v['edge_from']

    distancia_total = 0
    detalles = lt.new_list()
    n_camino = lt.size(camino)

    for i in range(n_camino):
        vid = lt.get_element(camino, i)
        info = G.get_vertex_information(grafo, vid)
        punto = {
            "id": vid,
            "lat": info["lat"],
            "lon": info["lon"],
            "num_individuos": lt.size(info["tags"]),
            "tags_prim": lt.new_list(),
            "tags_ult": lt.new_list(),
            "dist_next": "Desconocido"
        }

        if lt.size(info["tags"]) >= 3:
            limite_prim = 3
        else:
            limite_prim = lt.size(info["tags"])
        for k in range(limite_prim):
            lt.add_last(punto["tags_prim"], lt.get_element(info["tags"], k))
        inicio_ult = 0
        if lt.size(info["tags"]) > 3:
            inicio_ult = lt.size(info["tags"]) - 3
        for k in range(inicio_ult, lt.size(info["tags"])):
            lt.add_last(punto["tags_ult"], lt.get_element(info["tags"], k))

        if i < n_camino - 1:
            info_sig = G.get_vertex_information(grafo, lt.get_element(camino, i + 1))
            punto["dist_next"] = haversine(info["lat"], info["lon"], info_sig["lat"], info_sig["lon"])
            distancia_total += punto["dist_next"]

        lt.add_last(detalles, punto)

    if n_camino >= 5:
        limite_mostrar = 5
    else:
        limite_mostrar = n_camino
    primeros = lt.sub_list(detalles, 0, limite_mostrar)
    ultimos = lt.sub_list(detalles, n_camino - limite_mostrar, limite_mostrar)

    respuesta = {
        "ultimo_nodo_dentro_radio": ultimo_dentro_radio,
        "distancia_total": distancia_total,
        "total_puntos": n_camino,
        "primeros_5": primeros,
        "ultimos_5": ultimos
    }

    return respuesta


def cmp_tags(a, b):
    if a == b:
        return 0
    return 1
def construir_info_punto(orden, grafo, indice):
    v = lt.get_element(orden, indice)
    info = G.get_vertex_information(grafo, v)

    punto = {
        "id": v,
        "lat": info["lat"],
        "lon": info["lon"],
        "num_individuos": 0,
        "tags_prim": lt.new_list(),
        "tags_ult": lt.new_list(),
        "dist_prev": "Desconocido",
        "dist_next": "Desconocido"
    }
    tags = info["tags"]
    n_tags = lt.size(tags)
    punto["num_individuos"] = n_tags


    limite_prim = 3
    if n_tags < 3:
        limite_prim = n_tags
    for i in range(limite_prim):
        lt.add_last(punto["tags_prim"], lt.get_element(tags, i))


    inicio_ult = 0
    if n_tags > 3:
        inicio_ult = n_tags - 3
    for i in range(inicio_ult, n_tags):
        lt.add_last(punto["tags_ult"], lt.get_element(tags, i))

    if indice > 0:
        v_prev = lt.get_element(orden, indice-1)
        info_prev = G.get_vertex_information(grafo, v_prev)
        punto["dist_prev"] = haversine(
            info["lat"], info["lon"],
            info_prev["lat"], info_prev["lon"]
        )

    if indice < lt.size(orden) - 1:
        v_next = lt.get_element(orden, indice+1)
        info_next = G.get_vertex_information(grafo, v_next)
        punto["dist_next"] = haversine(
            info["lat"], info["lon"],
            info_next["lat"], info_next["lon"]
        )

    return punto
def req_3(catalog, grafo):
    """
    Retorna el resultado del requerimiento 3
    """
    answer = {
        "total_puntos": 0,
        "total_individuos": 0,
        "primeros": lt.new_list(),  
        "ultimos": lt.new_list(),    
        "ruta_valida": True
    }

    orden = df.topological_sort(grafo)
    n = lt.size(orden)

  
    if n == 0:
        answer["ruta_valida"] = False
        return answer

   
    answer["total_puntos"] = n

  
    vertices = G.vertices(grafo)
    individuos = lt.new_list()

    for i in range(lt.size(vertices)):
        v = lt.get_element(vertices, i)
        info = G.get_vertex_information(grafo, v)
        tags = info["tags"]

        for j in range(lt.size(tags)):
            tg = lt.get_element(tags, j)
            if lt.is_present(individuos, tg, cmp_tags) == -1:
                lt.add_last(individuos, tg)

    answer["total_individuos"] = lt.size(individuos)
    limite_prim = 5
    if n < 5:
        limite_prim = n
    for i in range(limite_prim):
        info_p = construir_info_punto(orden, grafo, i)
        lt.add_last(answer["primeros"], info_p)
    inicio_ult = 0
    if n > 5:
        inicio_ult = n - 5
    for i in range(inicio_ult, n):
        info_p = construir_info_punto(orden, grafo, i)
        lt.add_last(answer["ultimos"], info_p)

    return answer


def req_4(catalog, lat_origen, lon_origen):
    """
    Retorna el resultado del requerimiento 4
    """
    
    grafo = catalog["grafo_agua"]
    vertices_grafo = G.vertices(grafo)

    nodo_inicio = None
    min_dist = float('inf')
    for i in range(lt.size(vertices_grafo)):
        vid = lt.get_element(vertices_grafo, i)
        info = G.get_vertex_information(grafo, vid)
        d = haversine(lat_origen, lon_origen, info["lat"], info["lon"])
        if d < min_dist:
            min_dist = d
            nodo_inicio = vid

    if nodo_inicio is None:
        return {"error": "No se encontró un nodo cercano al origen."}

    visitados = mp.new_map(lt.size(vertices_grafo), 0.5)
    mp.put(visitados, nodo_inicio, True)

    nodos_mst = lt.new_list()
    lt.add_last(nodos_mst, nodo_inicio)

    dist_total = 0.0
    mst_edges = lt.new_list()

    heap = pq.new_heap(is_min_pq=True)

    adjs_inicio = G.adjacents(grafo, nodo_inicio)
    for j in range(lt.size(adjs_inicio)):
        vecino = lt.get_element(adjs_inicio, j)
        peso = mp.get(G.get_vertex(grafo, nodo_inicio)["adjacents"], vecino)
        pq.insert(heap, peso, (nodo_inicio, vecino))

    while not pq.is_empty(heap):
        arista = pq.remove(heap)
        origen, destino = arista[0], arista[1]

        if not mp.contains(visitados, destino):
            mp.put(visitados, destino, True)
            lt.add_last(nodos_mst, destino)
            lt.add_last(mst_edges, (origen, destino))
            dist_total += mp.get(G.get_vertex(grafo, origen)["adjacents"], destino)

            adjs_destino = G.adjacents(grafo, destino)
            for k in range(lt.size(adjs_destino)):
                vecino = lt.get_element(adjs_destino, k)
                if not mp.contains(visitados, vecino):
                    peso = mp.get(G.get_vertex(grafo, destino)["adjacents"], vecino)
                    pq.insert(heap, peso, (destino, vecino))

    total_individuos = 0
    detalles = lt.new_list()
    for i in range(lt.size(nodos_mst)):
        vid = lt.get_element(nodos_mst, i)
        info = G.get_vertex_information(grafo, vid)
        total_individuos += lt.size(info["tags"])

        tags_prim = lt.new_list()
        tags_ult = lt.new_list()
        n_tags = lt.size(info["tags"])

        limite_prim = min(3, n_tags)
        for k in range(limite_prim):
            tag = lt.get_element(info["tags"], k)
            lt.add_last(tags_prim, tag)

        inicio_ult = max(0, n_tags - 3)
        for k in range(inicio_ult, n_tags):
            tag = lt.get_element(info["tags"], k)
            lt.add_last(tags_ult, tag)

        dist_next = "Desconocido"
        if i < lt.size(nodos_mst) - 1:
            info_next = G.get_vertex_information(grafo, lt.get_element(nodos_mst, i + 1))
            dist_next = haversine(info["lat"], info["lon"], info_next["lat"], info_next["lon"])

        lt.add_last(detalles, {
            "id": vid,
            "lat": info["lat"],
            "lon": info["lon"],
            "num_individuos": lt.size(info["tags"]),
            "tags_prim": tags_prim,
            "tags_ult": tags_ult,
            "dist_next": dist_next
        })

    n_puntos = lt.size(nodos_mst)
    limite = min(5, n_puntos)
    primeros_5 = lt.sub_list(detalles, 0, limite)
    ultimos_5 = lt.sub_list(detalles, n_puntos - limite, limite)

    return {
        "total_puntos": n_puntos,
        "total_individuos": total_individuos,
        "distancia_total": dist_total,
        "primeros_5": primeros_5,
        "ultimos_5": ultimos_5
    }


def construir_punto_camino(camino, grafo, indice):
    v = lt.get_element(camino, indice)
    info = G.get_vertex_information(grafo, v)
    
    punto = {
        "id": v,
        "lat": info["lat"],
        "lon": info["lon"],
        "num_individuos": 0,
        "tags_prim": lt.new_list(),
        "tags_ult": lt.new_list(),
        "dist_next": "Desconocido"
    }
    
    tags = info["tags"]
    n_tags = lt.size(tags)
    punto["num_individuos"] = n_tags
    
    if n_tags >= 3:
        limite_prim = 3
    else:
        limite_prim = n_tags
    for i in range(limite_prim):
        lt.add_last(punto["tags_prim"], lt.get_element(tags, i))
    
    inicio_ult = 0
    if n_tags > 3:
        inicio_ult = n_tags - 3
    for i in range(inicio_ult, n_tags):
        lt.add_last(punto["tags_ult"], lt.get_element(tags, i))
        
    if indice < lt.size(camino) - 1:
        v_next = lt.get_element(camino, indice + 1)
        info_next = G.get_vertex_information(grafo, v_next)
        vertices = grafo["vertices"]
        nodo_v = mp.get(vertices, v)
        adjs = nodo_v["adjacents"]
        peso = mp.get(adjs, v_next)   
        punto["dist_next"] = peso
        
        
    return punto


def req_5(catalog, punto_origen, punto_destino, grafo):
    lat1, lon1 = punto_origen
    lat2, lon2 = punto_destino
    
    origen_real = None
    min_dist = float('inf')
    vertices = G.vertices(grafo)
    
    for i in range(lt.size(vertices)):
        ele = lt.get_element(vertices, i)
        info = G.get_vertex_information(grafo, ele)
        d = haversine(lat1, lon1, info["lat"], info["lon"])
        if d < min_dist:
            min_dist = d
            origen_real = ele

    destino_real = None
    min_dist2 = float('inf')
    for i in range(lt.size(vertices)):
        ele = lt.get_element(vertices, i)
        info = G.get_vertex_information(grafo, ele)
        d = haversine(lat2, lon2, info["lat"], info["lon"])
        if d < min_dist2:
            min_dist2 = d
            destino_real = ele
    
    search = dih.dijkstra(grafo, origen_real)
    
    answer = {
        "ruta_valida": False,
        "total_puntos": 0,
        "total_segmentos": 0,
        "costo_total": 0.0,
        "primeros": lt.new_list(),
        "ultimos": lt.new_list()
    }
    
    if dih.has_path_to(destino_real, search):
        camino = dih.path_to(destino_real, search)
        puntos = lt.size(camino)
        segmento = puntos - 1
        costo = dih.dist_to(destino_real, search)
        
        answer["ruta_valida"] = True
        answer["total_puntos"] = puntos
        answer["total_segmentos"] = segmento
        answer["costo_total"] = costo
        
        limite_prim = 5 if puntos >= 5 else puntos
        for i in range(limite_prim):
            p = construir_punto_camino(camino, grafo, i)
            lt.add_last(answer["primeros"], p)
        
        inicio_ult = 0
        if puntos > 5:
            inicio_ult = puntos - 5
        for i in range(inicio_ult, puntos):
            p = construir_punto_camino(camino, grafo, i)
            lt.add_last(answer["ultimos"], p)
    
    return answer

def req_6(control):
    """
    Identifica las subredes hídricas (componentes conectados) dentro del grafo.
    Usa DFS para encontrar componentes conectados.
    """

    graph = control["grafo_agua"]  

    if graph is None or len(graph) == 0:
        return {"error": "No existe un grafo hídrico cargado."}

    visited = set()
    subredes = []
    subred_id = 1
    for nodo in graph.keys():
        if nodo not in visited:

            # Nueva subred
            stack = [nodo]
            componente = []

            while stack:
                actual = stack.pop()

                if actual in visited:
                    continue

                visited.add(actual)
                componente.append(actual)

                for vecino in graph[actual]["adj"]:
                    if vecino not in visited:
                        stack.append(vecino)

            subredes.append({
                "id": subred_id,
                "nodos": componente
            })
            subred_id += 1

    if len(subredes) == 0:
        return {"error": "No se identificó ninguna subred hídrica."}

    subredes.sort(key=lambda x: (-len(x["nodos"]), x["id"]))

    top5 = subredes[:5]

    respuesta = {
        "total_subredes": len(subredes),
        "subredes_top": []
    }

    for sub in top5:
        nodos = sub["nodos"]

        latitudes = []
        longitudes = []
        individuos = set()

        for n in nodos:
            nodo_info = graph[n]

            latitudes.append(nodo_info.get("lat", "Unknown"))
            longitudes.append(nodo_info.get("lon", "Unknown"))

            for g in nodo_info.get("cranes", []):
                individuos.add(g)

        primeros_3 = nodos[:3]
        ultimos_3 = nodos[-3:]

        coords_primeros_3 = [(graph[n]["lat"], graph[n]["lon"]) for n in primeros_3]
        coords_ultimos_3 = [(graph[n]["lat"], graph[n]["lon"]) for n in ultimos_3]

        # Grullas
        individuos = sorted(list(individuos))
        primeros_3_individuos = individuos[:3]
        ultimos_3_individuos = individuos[-3:]

        respuesta["subredes_top"].append({
            "id": sub["id"],
            "total_nodos": len(nodos),
            "lat_min": min(latitudes),
            "lat_max": max(latitudes),
            "lon_min": min(longitudes),
            "lon_max": max(longitudes),
            "primeros_3_nodos": primeros_3,
            "ultimos_3_nodos": ultimos_3,
            "coords_primeros_3": coords_primeros_3,
            "coords_ultimos_3": coords_ultimos_3,
            "total_individuos": len(individuos),
            "primeros_3_individuos": primeros_3_individuos,
            "ultimos_3_individuos": ultimos_3_individuos
        })

    return respuesta

# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
