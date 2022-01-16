from Models import ComOffers
from geopy.distance import distance

from Models import User, DriverOffers, ComOffers, Rating
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import distance
from extensions import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData


metadata = MetaData()
db = SQLAlchemy(metadata=metadata)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_knock_knock.db'
db = SQLAlchemy(app)


#
# h = 14
#
# pi = [] # the noodes that lead to the current path
# pi_dist = 0 # the distance of the current path
# viable_routes = []
# viable_dist = []
#
# def DFS_VISIT(adj, u, e):
#     global pi
#     global pi_dist
#     global viable_routes
#     global viable_dist
#
#     adj[u][0][2] = 1
#
#     i = 0
#     for v in adj[u][1]: # durchlaufe adjazenzliste
#
#         # print(adj[u][0][2])
#         # print(pi_dist + v)
#         # print(i)
#
#         if (adj[i][0][2] == 0) and (pi_dist + v <= e):
#             pi.append(i)
#             pi_dist += v
#             # print(i)
#             DFS_VISIT(adj, i, e)
#
#
#         if (i == 14) and (pi_dist + v <= e):
#             pi.append(i)
#             viable_routes.append(pi)
#             viable_dist.append(pi_dist + v)
#         i += 1


#  ############ Initialisierung #####################
e = 200
com_offers = db.session.query(ComOffers).all()
coordinates = []
for offer in com_offers:
    coordinates.append([offer.id, [offer.start_lat, offer.start_long], [offer.end_lat, offer.end_long]])

graph = []
for own_coordinate in coordinates:
    node = {
        "id": own_coordinate[0],
        "visited": False,
        "parent": "NIL",
        "route_dist": distance(own_coordinate[1], own_coordinate[2]).km
    }

    adj = []
    for successor_coordinate in coordinates:
        if own_coordinate[0] != 24:
            adj.append({
                "id": successor_coordinate[0],
                "cost": distance(own_coordinate[2], successor_coordinate[1]).km
            })
        else:
            adj.append({
                "id": successor_coordinate[0],
                "cost": distance(own_coordinate[1], successor_coordinate[1]).km
            })
    node["adj"] = adj
    graph.append(node)
# print(graph)



def maximal_home_routes(G, s, e):
    # for u in graph:
        # if not u["visited"]:
            # print(len(u["adj"]))
    dfs_visit(G[s - 1], s, e)

    # print(graph)

pi_dist = 0
pi = []
viable_routes = []
def dfs_visit(u, s, e):
    global pi_dist
    global viable_routes
    global pi

        # if (adj[i][0][2] == 0) and (pi_dist + v <= e):
        #     pi.append(i)
        #     pi_dist += v
        #     # print(i)
        #     DFS_VISIT(adj, i, e)
        #
        #
        # if (i == 14) and (pi_dist + v <= e):
        #     pi.append(i)
        #     viable_routes.append(pi)
        #     viable_dist.append(pi_dist + v)
        # i += 1
    #
    # if G[s-1]["id"] != s:
    u["visited"] = True

    for v in u["adj"]:
        dist= 0

        # [print(f"route_dist: {pi[node]}") for node in range(len(pi))]
        dist = sum([ graph[pi[node] -1]["route_dist"] + graph[pi[node] -1]["adj"][node]["cost"] for node in range(len(pi)) ])

        # print(dist)

        # node_weight =

        if (graph[v["id"] -1]["visited"] == False) and dist <= e: # first iteration cost
            # print("enter if case")
            pi.append(v["id"])
            dfs_visit(graph[v["id"] -1], s, e)

        if v["id"] == s and dist <= e:
            print(f"home route found ! dist {dist}")
            viable_routes.append(pi)




            # print(pi)

        # print(f"v: {v['id']} s: {s} dist: {dist}")
        # if v["id"] == s and dist <= e:
        #     print(f"home route found ! dist {dist}")
        #     viable_routes.append(pi)
            # print(viable_routes)
            # pi.pop()
            # print(pi)
            # pi.pop()

        # if dist > e:
        #     pi.pop()




def check_result():
    distanz = graph[14]["adj"][0]["cost"] +  graph[0]["route_dist"] + graph[0]["adj"][1]["cost"] + \
        graph[1]["route_dist"] + graph[1]["adj"][2]["cost"] + graph[2]["route_dist"] + \
         graph[2]["adj"][3]["cost"] + graph[3]["route_dist"] + graph[3]["adj"][4]["cost"] + \
         graph[4]["route_dist"] + graph[4]["adj"][14]["cost"]
    print(distanz)





    #     # time += 1
    #     u["visited"] = True
    #     for v in u["adj"]:
    #         # print(v)
    #         if not graph[v]["visited"]:
    #              graph[v]["parent"] = u
    #              print(f"{u['id']} -> {graph[v]['id']}")
    #              dfs_visit(graph[v])
    #
    #              # return graph[v]["parent"]

maximal_home_routes(graph, 24, 50)

check_result()

# for node in graph:
#     print(node["id"])



    # for coordinate in coordinates:
    #     coordinate.append(distance(coordinate[1], coordinate[2]).km)


    # print(f"adjazenzliste: {adjazenzliste[1][0][0]}")

    # node = routendistanz, cost, id, adj, visited, parent

    # ########### Ende Initialisierung #######################

    # print(adjazenzliste[1][1])
    # viable_routes = []
    # viable_dist = []

    # for item in adjazenzliste:
    #     # print(f"start node has not been visited {adjazenzliste[24][0][1]}")
    #     DFS_VISIT(adjazenzliste, item[0][0] -1, e)



# print(f"viable_routes {viable_routes}")
#
# list_1 = [2,3]
# list_2 = [0,2,3]
# list_3 = [0,1,3]
# list_4 = [0,1,2]
#
# adj = []
# adj.append(list_1)
# adj.append(list_2)
# adj.append(list_3)
# adj.append(list_4)
#
#
# i = 0
# graph = []
# for list in adj:
#     graph.append({"id":i, "adj": list})
#     i += 1
#
#
# def dfs():
#     for u in graph:
#         u["visited"] = False
#         u["parent"] = "nil"
#
#     time = 0
#     for u in graph:
#         if not u["visited"]:
#             dfs_visit(u)
#
# def dfs_visit(u):
#     # time += 1
#     u["visited"] = True
#     for v in u["adj"]:
#         # print(v)
#         if not graph[v]["visited"]:
#              graph[v]["parent"] = u
#              print(f"{u['id']} -> {graph[v]['id']}")
#              dfs_visit(graph[v])
#
#              # return graph[v]["parent"]
#
#
# dfs()
#
#




# def DFS_VISIT(adjazenzliste, e):







    # print(f"coordinates {coordinates}")
    # print(f"own_coordinate {own_coordinate[1]}\nsuccessor_coordinate {successor_coordinate[2]}")

        # adjazenzliste.append(distance(own_coordinate, successor_coordinate))


    # print(adjazenzliste)


# maximal_home_routes()
