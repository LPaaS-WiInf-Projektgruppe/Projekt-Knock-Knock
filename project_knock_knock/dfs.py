list_1 = [2,3]
list_2 = [0,2,3]
list_3 = [0,1,3]
list_4 = [0,1,2]

adj = []
adj.append(list_1)
adj.append(list_2)
adj.append(list_3)
adj.append(list_4)

for i in range(25):
    for j in range(25):
        if i%5 == 0 and j == 1 or j == 6:
            adj[i][j] = 1
        if i%5 == 1 and j == 2 or j == 7:
            adj[i][j] = 1
        if i%5 == 2 and j == 3 or j == 8:
            adj[i][j] = 1
        if i%5 == 3 and j == 3 or j == 8:
            adj[i][j] = 1

i = 0
graph = []
for list in adj:
    graph.append({"id":i, "adj": list})
    i += 1


def dfs():
    for u in graph:
        u["visited"] = False
        u["parent"] = "nil"

    time = 0
    for u in graph:
        if not u["visited"]:
            dfs_visit_modified(u)

def dfs_visit(u):
    # time += 1
    u["visited"] = True
    for v in u["adj"]:
        # print(v)
        if not graph[v]["visited"]:
             graph[v]["parent"] = u
             print(f"{u['id']} -> {graph[v]['id']}")
             dfs_visit(graph[v])

             # return graph[v]["parent"]


# dfs()
# print(dfs())

# if graph[1]["parent"] != "nil":
#     print(graph[1]["parent"])

# print(graph

# def dfs_modified():
#     for u in graph:
#         u["visited"] = False
#         u["parent"] = "nil"
#
#     time = 0
#     for u in graph:
#         if not u["visited"]:
#             dfs_visit_modified(u)
#
# def dfs_visit_modified(u, s, e):
#     for v in u["adj"]:
#         if not graph[v["id"] -1]["visited"]: # first iteration cost
#             # print("enter if case")
#             pi.append(v["id"])
#             dfs_visit(graph[v["id"] -1], s, e)
#
#         if v["id"] == s and dist <= e:
#             print(f"home route found ! dist {dist}")
#             viable_routes.append(pi)
