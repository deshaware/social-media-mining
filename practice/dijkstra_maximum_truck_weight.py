import heapq


def dijkstra(G,s):
    #Copy the graph and calculate G
    dist = [0] * len(G)
    visited = [False] * len(G)
    pathlength = [0] * len(G)
    prev = [-1] * len(G)
    
    dist[s] = 999
    #Add into queue
    H = [] #Heap
    heapq.heappush(H,(-999,s))

    while len(H) != 0:
        u = heapq.heappop(H)[1]
        # mark it visited
        visited[u] = True
        edges = [i for (i,j) in enumerate(G[u]) if j > 0 and j < 999]
        # print(edges)
        for v in edges:
            if dist[v] < max(dist[v], min(dist[u], G[u][v])) and visited[v] == False:
                dist[v] = max(dist[v], min(dist[u], G[u][v]))
                pathlength[v] += 1
                prev[v] = u
                heapq.heappush(H,(-dist[v],v))
            # print(G[u][v])
    
    print("dist",dist)

    # print(visited)
    # print(pathlength)
    return dist

if __name__ == '__main__':
    # G = [
    # [999, 40, 20, 30, 0, 0, 0],
    # [40, 999, 25, 0, 40, 0, 0],
    # [20, 25, 999, 30, 0, 20, 0],
    # [30, 0, 30, 999, 0, 10, 0],
    # [0, 40, 0, 0, 999, 35, 10],
    # [0, 0, 20, 10, 35, 999, 30],
    # [0, 0, 0, 0, 10, 30, 999]
    # ]
    G = [
        [999, 40, 30, 0, 0],
        [40, 999, 30, 20, 0],
        [30, 30, 999, 35, 0],
        [0, 20, 35, 999, 30],
        [0, 0, 0, 30, 999]
        ]

    print(dijkstra(G,0))
