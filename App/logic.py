import csv
import math
import os
from datetime import datetime

from DataStructures.List import array_list as lt
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import digraph as G


# ---------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# Creación del catálogo
# ---------------------------------------------------------

def new_logic():
    """
    Crea el catálogo para almacenar las estructuras de datos.
    """
    grafo_dist = G.new_graph(2000)   # grafo de migración (distancia)
    grafo_agua = G.new_graph(2000)   # grafo hídrico (agua promedio)

    catalog = {
        "grafo_distancia": grafo_dist,
        "grafo_agua": grafo_agua,
        "mapa_eventos": mp.new_map(25000, 0.5),  # event-id -> id del nodo
        "lista_eventos": lt.new_list(),          # lista de eventos crudos
        "total_grullas": 0,
        "total_eventos": 0
    }
    return catalog


# ---------------------------------------------------------
# Carga de datos
# ---------------------------------------------------------

def load_data(catalog, filename):
    """
    Carga los datos desde el CSV, construye:
      - lista de eventos
      - nodos (vértices) en grafo_distancia y grafo_agua
      - arcos entre nodos para cada grulla

    No imprime nada: solo llena el catálogo.
    """
    # -------- 1. Leer CSV y llenar lista_eventos --------
    filepath = os.path.join("Data", filename)
    lista = catalog["lista_eventos"]

    # Para contar cuántas grullas distintas hay
    mapa_tags = mp.new_map(10, 0.5)
    total_grullas = 0

    with open(filepath, mode="r", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # limpiar llaves con espacios
            row = {k.strip(): v for k, v in row.items() if k is not None}

            # timestamp
            fecha_str = row["timestamp"].strip()
            try:
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S.%f")
            except Exception:
                fecha = datetime.strptime(
                    fecha_str.split('.')[0], "%Y-%m-%d %H:%M:%S"
                )

            # distancia al agua (comments)
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

            # contar grullas distintAS
            if not mp.contains(mapa_tags, tag):
                mp.put(mapa_tags, tag, True)
                total_grullas += 1

    catalog["total_grullas"] = total_grullas
    catalog["total_eventos"] = lt.size(lista)

    # ordenar eventos globalmente por tiempo
    lt.quick_sort(lista, comparar_fecha)

    grafo_dist = catalog["grafo_distancia"]
    grafo_agua = catalog["grafo_agua"]
    mapa_eventos = catalog["mapa_eventos"]

    # -------- 2. Construir nodos (puntos migratorios) --------
    # Regla: por CADA grulla (tag) independiente:
    #   - recorro sus eventos en orden temporal (lista ya está ordenada globalmente)
    #   - si el evento está a menos de 3km y 3h del PRIMER evento del nodo actual
    #     de esa grulla, lo agrupo en el mismo nodo.
    #   - si no, creo un nuevo nodo.
    #
    # El id del nodo es el id del primer evento que cayó en ese nodo.

    last_node_per_tag = {}  # tag_id -> dict con info del nodo actual

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

            # misma "estancia" si cumple ambas condiciones
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
                "events": lt.new_list(),   # lista de event-id
                "tags": lt.new_list(),     # lista de tags que pasaron por este nodo
                "tags_set": set(),         # auxiliar para no repetir tags
                "event_count": 0,
                "water_sum": 0.0
            }

            # primer evento del nodo
            lt.add_last(nodo_info["events"], evento["id"])
            nodo_info["event_count"] = 1
            nodo_info["water_sum"] = evento["water_dist"]
            nodo_info["tags_set"].add(tag)
            lt.add_last(nodo_info["tags"], tag)

            # insertar vértice en ambos grafos
            G.insert_vertex(grafo_dist, node_id, nodo_info)
            G.insert_vertex(grafo_agua, node_id, nodo_info)

            last_node_per_tag[tag] = nodo_info
            nodo_actual = nodo_info

        else:
            # acumular evento en el nodo existente
            lt.add_last(nodo_actual["events"], evento["id"])
            nodo_actual["event_count"] += 1
            nodo_actual["water_sum"] += evento["water_dist"]

            if tag not in nodo_actual["tags_set"]:
                nodo_actual["tags_set"].add(tag)
                lt.add_last(nodo_actual["tags"], tag)

        # mapear event-id -> id del nodo
        mp.put(mapa_eventos, evento["id"], nodo_actual["id"])

    # -------- 3. Construir arcos (migración e hídrico) --------
    # Reordenamos los eventos por (tag, timestamp) para recorrer
    # cada grulla en orden temporal y conectar los nodos que visita.

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

            # peso por distancia (grafo de migración)
            w_dist = haversine(
                info_o["lat"], info_o["lon"],
                info_d["lat"], info_d["lon"]
            )
            G.add_edge(grafo_dist, origen_id, destino_id, w_dist)

            # peso por agua promedio en el nodo destino (grafo hídrico)
            if info_d["event_count"] > 0:
                w_water = info_d["water_sum"] / info_d["event_count"]
            else:
                w_water = 0.0
            G.add_edge(grafo_agua, origen_id, destino_id, w_water)

def req_1(catalog):

    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


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
