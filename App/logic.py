import csv
import math
import os
import sys
from datetime import datetime
from DataStructures.List import array_list as lt
from DataStructures.Map import map_linear_probing as mp
import DataStructures.Graph.digraph as G

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def new_logic():
    sys.setrecursionlimit(20000)
    grafo_dist = G.new_graph(3000)
    grafo_agua = G.new_graph(3000)
    mapa_eventos = mp.new_map(25000, 0.5)
    return {
        "grafo_distancia": grafo_dist,
        "grafo_agua": grafo_agua,
        "mapa_eventos": mapa_eventos,
        "lista_eventos": lt.new_list(),
        "total_grullas": 0,
        "total_eventos": 0            
    }

def comparar_fecha(evento_a, evento_b):
    return evento_a["timestamp"] < evento_b["timestamp"]

def compara_tag(e1, e2):
    if e1["tag_id"] < e2["tag_id"]:
        return True
    elif e1["tag_id"] > e2["tag_id"]:
        return False
    return e1["timestamp"] < e2["timestamp"]


def load_data(catalog, filename):
    filepath = os.path.join("Data", filename)
    lista = catalog["lista_eventos"]

    mapa_tags = mp.new_map(100, 0.5)

    with open(filepath, mode="r", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row = {k.strip(): v for k, v in row.items() if k is not None}

            fecha_str = row["timestamp"].strip()
            try:
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S.%f")
            except:
                fecha = datetime.strptime(
                    row["timestamp"].split('.')[0], "%Y-%m-%d %H:%M:%S"
                )

            dist_agua = 0.0
            comment = row.get("comments", "")
            if comment:
                limpiar_str = comment.replace('"', '').replace("'", "").strip()
                if limpiar_str:
                    try:
                        dist_agua = float(limpiar_str)
                    except ValueError:
                        dist_agua = 0.0

            tag = row["tag-local-identifier"].strip()

            evento = {
                "id": row["event-id"],
                "lat": float(row["location-lat"]),
                "lon": float(row["location-long"]),
                "timestamp": fecha,
                "tag_id": tag,
                "water_dist": dist_agua,
            }

            lt.add_last(lista, evento)

            if mp.get(mapa_tags, tag) is None:
                mp.put(mapa_tags, tag, True)
                catalog["total_grullas"] += 1

    catalog["total_eventos"] = lt.size(lista)

    lt.quick_sort(lista, comparar_fecha)

    last_nodes = mp.new_map(1000, 0.5)

    lista_tamano = lt.size(lista)

    for i in range(lista_tamano):
        evento = lt.get_element(lista, i)
        tag = evento["tag_id"]

        entry = mp.get(last_nodes, tag)
        crear = True

        if entry is not None:
            node_id = entry["node_id"]
            node_info = G.get_vertex_information(catalog["grafo_distancia"], node_id)

            dist = haversine(
                evento["lat"], evento["lon"], node_info["lat"], node_info["lon"]
            )

            time_dif = abs(
                (evento["timestamp"] - node_info["last_event_time"]).total_seconds()
            ) / 3600.0

            if dist < 3.0 and time_dif < 3.0:
                crear = False
                node_info["event_count"] += 1
                node_info["water_sum"] += evento["water_dist"]
                node_info["last_event_time"] = evento["timestamp"]
                mp.put(catalog["mapa_eventos"], evento["id"], node_id)

        if crear:
            node_id = evento["id"]
            node_info = {
                "id": node_id,
                "lat": evento["lat"],
                "lon": evento["lon"],
                "creation_time": evento["timestamp"],
                "last_event_time": evento["timestamp"],
                "event_count": 1,
                "water_sum": evento["water_dist"],
            }

            G.insert_vertex(catalog["grafo_distancia"], node_id, node_info)
            G.insert_vertex(catalog["grafo_agua"], node_id, node_info)

            mp.put(catalog["mapa_eventos"], evento["id"], node_id)
            mp.put(last_nodes, tag, {"node_id": node_id})

    lt.quick_sort(lista, compara_tag)

    for i in range(1, lista_tamano):
        prev = lt.get_element(lista, i - 1)
        curr = lt.get_element(lista, i)

        if prev["tag_id"] == curr["tag_id"]:
            ori = mp.get(catalog["mapa_eventos"], prev["id"])
            dest = mp.get(catalog["mapa_eventos"], curr["id"])

            if ori != dest:
                info_o = G.get_vertex_information(catalog["grafo_distancia"], ori)
                info_d = G.get_vertex_information(catalog["grafo_distancia"], dest)

                w_distancia = haversine(
                    info_o["lat"], info_o["lon"], info_d["lat"], info_d["lon"]
                )
                G.add_edge(catalog["grafo_distancia"], ori, dest, w_distancia)

                w_agua = info_d["water_sum"] / info_d["event_count"]
                G.add_edge(catalog["grafo_agua"], ori, dest, w_agua)

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
