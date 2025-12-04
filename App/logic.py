import csv
import math
import os
from datetime import datetime, time
import time 
from DataStructures.List import array_list as lt
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import digraph as G
from DataStructures.Graph import dfo as df
from DataStructures.Graph import dijkstra as dih
from DataStructures.Graph import dfs 
def haversine(lat1, lon1, lat2, lon2):
    """
    Distancia Haversine en km entre dos puntos (lat, lon).
    """
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def comparar_fecha(e1, e2):
    """
    Criterio de ordenamiento por timestamp ascendente.
    """
    return e1["timestamp"] < e2["timestamp"]


def compara_tag(e1, e2):
    """
    Criterio de ordenamiento por tag y luego por timestamp.
    """
    if e1["tag_id"] < e2["tag_id"]:
        return True
    elif e1["tag_id"] > e2["tag_id"]:
        return False
    return e1["timestamp"] < e2["timestamp"]



def new_logic():
    """
    Crea el catálogo para almacenar las estructuras de datos.
    """
    grafo_dist = G.new_graph(2000)   
    grafo_agua = G.new_graph(2000)   
    catalog = {
        "grafo_distancia": grafo_dist,
        "grafo_agua": grafo_agua,
        "mapa_eventos": mp.new_map(25000, 0.5),  
        "lista_eventos": lt.new_list(),        
        "total_grullas": 0,
        "total_eventos": 0
    }
    return catalog


def load_data(catalog, filename):
    """
    Carga los datos desde el CSV, construye:
      - lista de eventos
      - nodos (vértices) en grafo_distancia y grafo_agua
      - arcos entre nodos para cada grulla

    No imprime nada: solo llena el catálogo.
    """

    filepath = os.path.join("Data", filename)
    lista = catalog["lista_eventos"]

    mapa_tags = mp.new_map(10, 0.5)
    total_grullas = 0
    x=1
    with open(filepath, mode="r", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            row = {k.strip(): v for k, v in row.items() if k is not None}

            fecha_str = row["timestamp"].strip()
            try:
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S.%f")
            except Exception:
                fecha = datetime.strptime(
                    fecha_str.split('.')[0], "%Y-%m-%d %H:%M:%S"
                )

        
            dist_agua = 0.0
            raw_comment = row.get("comments", "")
            if raw_comment:
                clean = raw_comment.replace('"', "").replace("'", "").strip()
                if clean:
                    try:
                        dist_agua = float(clean)
                    except ValueError:
                        dist_agua = 0.0

            tag = row["tag-local-identifier"].strip()
            evento = {
                "id": row["event-id"],
                "lat": float(row["location-lat"]),
                "lon": float(row["location-long"]),
                "timestamp": fecha,
                "tag_id": tag,
                "water_dist": dist_agua
            }

            lt.add_last(lista, evento)


            if not mp.contains(mapa_tags, tag):
                mp.put(mapa_tags, tag, True)
                total_grullas += 1

    catalog["total_grullas"] = total_grullas
    catalog["total_eventos"] = lt.size(lista)

    lt.quick_sort(lista, comparar_fecha)

    grafo_dist = catalog["grafo_distancia"]
    grafo_agua = catalog["grafo_agua"]
    mapa_eventos = catalog["mapa_eventos"]



    last_node_per_tag = {} 

    n = lt.size(lista)
    for i in range(n):
        evento = lt.get_element(lista, i)
        tag = evento["tag_id"]

        crear_nodo = True
        nodo_actual = None

        if tag in last_node_per_tag:
            nodo_actual = last_node_per_tag[tag]
            base_lat = nodo_actual["lat"]
            base_lon = nodo_actual["lon"]
            base_time = nodo_actual["creation_time"]

            dist = haversine(evento["lat"], evento["lon"], base_lat, base_lon)
            dt_h = abs(
                (evento["timestamp"] - base_time).total_seconds()
            ) / 3600.0

            if dist < 3.0 and dt_h < 3.0:
                crear_nodo = False

        if crear_nodo:
            node_id = evento["id"]

            nodo_info = {
                "id": node_id,
                "lat": evento["lat"],
                "lon": evento["lon"],
                "creation_time": evento["timestamp"],

                # info acumulada
                "events": lt.new_list(),  
                "tags": lt.new_list(),    
                "tags_set": set(),        
                "event_count": 0,
                "water_sum": 0.0
            }


            lt.add_last(nodo_info["events"], evento["id"])
            nodo_info["event_count"] = 1
            nodo_info["water_sum"] = evento["water_dist"]
            nodo_info["tags_set"].add(tag)
            lt.add_last(nodo_info["tags"], tag)

            G.insert_vertex(grafo_dist, node_id, nodo_info)
            G.insert_vertex(grafo_agua, node_id, nodo_info)

            last_node_per_tag[tag] = nodo_info
            nodo_actual = nodo_info

        else:

            lt.add_last(nodo_actual["events"], evento["id"])
            nodo_actual["event_count"] += 1
            nodo_actual["water_sum"] += evento["water_dist"]

            if tag not in nodo_actual["tags_set"]:
                nodo_actual["tags_set"].add(tag)
                lt.add_last(nodo_actual["tags"], tag)

        mp.put(mapa_eventos, evento["id"], nodo_actual["id"])



    lt.quick_sort(lista, compara_tag)

    for i in range(1, n):
        prev = lt.get_element(lista, i - 1)
        curr = lt.get_element(lista, i)

        if prev["tag_id"] == curr["tag_id"]:
            origen_id = mp.get(mapa_eventos, prev["id"])
            destino_id = mp.get(mapa_eventos, curr["id"])

            if origen_id is None or destino_id is None:
                continue
            if origen_id == destino_id:
                continue

            info_o = G.get_vertex_information(grafo_dist, origen_id)
            info_d = G.get_vertex_information(grafo_dist, destino_id)


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
    # Encontrar nodos más cercanos
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
    # DFS desde el nodo origen
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

    # ------------------------------
    # Reconstruir camino origen → destino
    # ------------------------------
    camino = lt.new_list()
    v = nodo_destino
    while v is not None:
        lt.add_first(camino, v)
        info_v = mp.get(visitados, v)
        if not info_v:
            break
        v = info_v.get('edge_from')

    # ------------------------------
    # Identificar primer nodo donde aparece el individuo
    # ------------------------------
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

        # Revisar si individuo está en este vértice
        if primer_nodo_individuo == "Desconocido":
            for t in tags_list["elements"]:
                if t == individuo_id:
                    primer_nodo_individuo = vid
                    break

        # Construir punto
        punto = {
            "id": vid,
            "lat": lat_v,
            "lon": lon_v,
            "num_individuos": tags_size,
            "tags_prim": lt.new_list(),
            "tags_ult": lt.new_list(),
            "dist_next": "Desconocido"
        }

        # primeros 3 tags
        lim_prim = min(3, tags_size)
        for k in range(lim_prim):
            lt.add_last(punto["tags_prim"], lt.get_element(tags_list, k))

        # últimos 3 tags
        ini_ult = tags_size - 3 if tags_size > 3 else 0
        for k in range(ini_ult, tags_size):
            lt.add_last(punto["tags_ult"], lt.get_element(tags_list, k))

        # distancia al siguiente punto
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
    # primeros 5 / últimos 5
    # ------------------------------
    limite_mostrar = 5 if n_camino >= 5 else n_camino
    primeros = lt.sub_list(detalles, 0, limite_mostrar)
    ultimos = lt.sub_list(detalles, n_camino - limite_mostrar, limite_mostrar)

    # ------------------------------
    # respuesta final
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
        punto["dist_next"] = haversine(
            info["lat"], info["lon"],
            info_next["lat"], info_next["lon"]
        )
        
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
    REQ 6: Identificar subredes hídricas aisladas (componentes conectados) dentro del nicho biológico.
    Retorna un diccionario con toda la información requerida para impresión.
    """

    grafo = control["graph"]  # grafo ya construido con puntos migratorios

    visitados = set()
    subredes = []
    id_subred = 1

    # ---------------------------------------------------------------------
    # 1. Identificación de subredes usando DFS (componentes conectados)
    # ---------------------------------------------------------------------
    for nodo in grafo.vertices():

        if nodo in visitados:
            continue

        # DFS desde nodo no visitado
        dfa = dfs (grafo, nodo)
        componente = dfs.vertices_reachable()  # conjunto/lista de nodos alcanzables

        # Marcar nodos visitados
        for n in componente:
            visitados.add(n)

        # Registrar subred
        subredes.append({
            "id": id_subred,
            "nodos": list(componente)
        })

        id_subred += 1

    # Si no hay subredes
    if len(subredes) == 0:
        return {"error": "No se identificaron subredes hídricas en el nicho biológico."}

    # ---------------------------------------------------------------------
    # 2. Enriquecer datos de cada subred (latitudes, longitudes, individuos)
    # ---------------------------------------------------------------------
    for sub in subredes:

        nodos = sub["nodos"]

        lats, lons = [], []
        individuos = set()

        # extraer datos de cada nodo
        for n in nodos:
            data = grafo.get_vertex_data(n)

            if data is not None:

                lat = data.get("lat", "Unknown")
                lon = data.get("lon", "Unknown")

                if lat != "Unknown" and lon != "Unknown":
                    lats.append(lat)
                    lons.append(lon)

                # Lista de grullas en este punto
                tags = data.get("tags", [])
                for t in tags:
                    individuos.add(t)

        # Ordenar nodos para primeros y últimos
        nodos_ordenados = sorted(nodos)

        # Guardar valores enriquecidos
        sub["lat_min"] = min(lats) if lats else "Unknown"
        sub["lat_max"] = max(lats) if lats else "Unknown"
        sub["lon_min"] = min(lons) if lons else "Unknown"
        sub["lon_max"] = max(lons) if lons else "Unknown"

        sub["total_nodos"] = len(nodos)
        sub["primeros_3_nodos"] = nodos_ordenados[:3]
        sub["ultimos_3_nodos"] = nodos_ordenados[-3:]

        # Obtener lat/lon de nodos requeridos
        def coords(n):
            d = grafo.get_vertex_data(n)
            if d:
                return d.get("lat", "Unknown"), d.get("lon", "Unknown")
            return ("Unknown", "Unknown")

        sub["coords_primeros_3"] = [coords(n) for n in sub["primeros_3_nodos"]]

        # Grullas en la subred
        sub["total_individuos"] = len(individuos)
        indiv_sorted = sorted(individuos)
        sub["primeros_3_individuos"] = indiv_sorted[:3]
        sub["ultimos_3_individuos"] = indiv_sorted[-3:]

    # ---------------------------------------------------------------------
    # 3. Ordenar subredes por tamaño y después por ID
    # ---------------------------------------------------------------------
    subredes_ordenadas = sorted(subredes, key=lambda s: (-s["total_nodos"], s["id"]))

    # ---------------------------------------------------------------------
    # 4. Retornar sólo top 5 (o todas si hay <5)
    # ---------------------------------------------------------------------
    return {
        "total_subredes": len(subredes),
        "subredes_top": subredes_ordenadas[:5]
    }


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
