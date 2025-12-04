import csv
import math
import os
import sys
from datetime import datetime
from DataStructures.List import array_list as lt
from DataStructures.Map import map_linear_probing as mp
import DataStructures.Graph.digraph as G
from DataStructures.Graph import dfs as dfs
from DataStructures.Graph import dfo as df
from DataStructures.Graph import dijkstra as dih
import time
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


def req_1(catalog, lat_origen, lon_origen, lat_destino, lon_destino, individuo_id):
    """
    REQ 1: Detectar el camino usado por un individuo entre dos puntos migratorios.
    DFS + aproximación geográfica con Haversine.
    """

    grafo = catalog.get("grafo_distancia")
    if not grafo:
        return {"error": "Grafo vacío o no encontrado."}

    vertices_grafo = G.vertices(grafo)
    if not vertices_grafo or "elements" not in vertices_grafo:
        return {"error": "No hay vértices en el grafo."}


    # ------------------------------
    nodo_origen = None
    min_dist_origen = float('inf')
    for v in vertices_grafo["elements"]:
        info = G.get_vertex_information(grafo, v) or {}
        lat_v = info.get("lat", None)
        lon_v = info.get("lon", None)
        if lat_v is None or lon_v is None:
            continue
        d = haversine(lat_origen, lon_origen, lat_v, lon_v)
        if d < min_dist_origen:
            min_dist_origen = d
            nodo_origen = v

    nodo_destino = None
    min_dist_destino = float('inf')
    for v in vertices_grafo["elements"]:
        info = G.get_vertex_information(grafo, v) or {}
        lat_v = info.get("lat", None)
        lon_v = info.get("lon", None)
        if lat_v is None or lon_v is None:
            continue
        d = haversine(lat_destino, lon_destino, lat_v, lon_v)
        if d < min_dist_destino:
            min_dist_destino = d
            nodo_destino = v

    if nodo_origen is None or nodo_destino is None:
        return {"error": "No se pudo determinar nodo origen o destino."}

    # ------------------------------
    # DFS
    # ------------------------------
    visitados = mp.new_map(num_elements=G.order(grafo) or 1, load_factor=0.5)
    stack = lt.new_list()
    lt.add_last(stack, nodo_origen)
    mp.put(visitados, nodo_origen, {'marked': True, 'edge_from': None})

    while lt.size(stack) > 0:
        actual = lt.get_element(stack, lt.size(stack)-1)
        lt.delete_element(stack, lt.size(stack)-1)

        if actual == nodo_destino:
            break

        adjs = G.adjacents(grafo, actual) or {"elements": []}
        for w in adjs["elements"]:
            if not mp.contains(visitados, w):
                mp.put(visitados, w, {'marked': True, 'edge_from': actual})
                lt.add_last(stack, w)

    # Si destino no fue alcanzado
    if not mp.contains(visitados, nodo_destino):
        return {"error": "No existe un camino viable entre los puntos."}

    camino = lt.new_list()
    v = nodo_destino
    while v is not None:
        lt.add_first(camino, v)
        info_v = mp.get(visitados, v)
        if not info_v:
            break
        v = info_v.get('edge_from')

    primer_nodo_individuo = "Desconocido"

    n_camino = lt.size(camino)
    detalles = lt.new_list()
    distancia_total = 0.0

    for i in range(n_camino):
        vid = lt.get_element(camino, i)
        info = G.get_vertex_information(grafo, vid) or {}

        lat_v = info.get("lat", "Desconocido")
        lon_v = info.get("lon", "Desconocido")
        tags = info.get("tags", None)

        if tags is None:
            tags_list = lt.new_list()
            tags_size = 0
        else:
            tags_list = tags
            tags_size = lt.size(tags)

        if primer_nodo_individuo == "Desconocido":
            for t in tags_list["elements"]:
                if t == individuo_id:
                    primer_nodo_individuo = vid
                    break

        punto = {
            "id": vid,
            "lat": lat_v,
            "lon": lon_v,
            "num_individuos": tags_size,
            "tags_prim": lt.new_list(),
            "tags_ult": lt.new_list(),
            "dist_next": "Desconocido"
        }

        lim_prim = min(3, tags_size)
        for k in range(lim_prim):
            lt.add_last(punto["tags_prim"], lt.get_element(tags_list, k))

        ini_ult = tags_size - 3 if tags_size > 3 else 0
        for k in range(ini_ult, tags_size):
            lt.add_last(punto["tags_ult"], lt.get_element(tags_list, k))

        if i < n_camino - 1:
            sig_vid = lt.get_element(camino, i+1)
            info_sig = G.get_vertex_information(grafo, sig_vid) or {}
            lat_s = info_sig.get("lat", None)
            lon_s = info_sig.get("lon", None)
            if lat_v != "Desconocido" and lon_v != "Desconocido" and lat_s is not None and lon_s is not None:
                dnext = haversine(lat_v, lon_v, lat_s, lon_s)
                punto["dist_next"] = dnext
                distancia_total += dnext

        lt.add_last(detalles, punto)

    # ------------------------------
    limite_mostrar = 5 if n_camino >= 5 else n_camino
    primeros = lt.sub_list(detalles, 0, limite_mostrar)
    ultimos = lt.sub_list(detalles, n_camino - limite_mostrar, limite_mostrar)

    # ------------------------------
    return {
        "primer_nodo_individuo": primer_nodo_individuo,
        "distancia_total": distancia_total,
        "total_puntos": n_camino,
        "primeros_5": primeros,
        "ultimos_5": ultimos
    }


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass

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
def req_4(catalog):
    
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass
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

    # Tomar las 5 más grandes
    top5 = subredes[:5]

    respuesta = {
        "total_subredes": len(subredes),
        "subredes_top": []
    }

    for sub in top5:
        nodos = sub["nodos"]

        # Extracción de datos geográficos
        latitudes = []
        longitudes = []
        individuos = set()

        for n in nodos:
            nodo_info = graph[n]

            latitudes.append(nodo_info.get("lat", "Unknown"))
            longitudes.append(nodo_info.get("lon", "Unknown"))

            # Agregar grullas (evitar duplicados)
            for g in nodo_info.get("cranes", []):
                individuos.add(g)

        # Primeros y últimos 3 nodos
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
