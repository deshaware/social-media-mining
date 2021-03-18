import heapq

def dijkstra(G,s):
    #Copy the graph and calculate G
    dist = [999] * len(G)
    visited = [False] * len(G)
    pathlength = [0] * len(G)
    prev = [-1] * len(G)
    
    dist[s] = 0
    #Add into queue
    H = [] #Heap
    heapq.heappush(H,(0,s))
    # for i in range(len(G) - 1):
    #     heapq.heappush(H,(999,i+1))

    # print(H)
    # print(heapq.heappop(H))
    # print(heapq.heappop(H))
    # print(heapq.heappop(H))
    # print(len(H))
    

    while len(H) != 0:
        u = heapq.heappop(H)[1]
        # mark it visited
        visited[u] = True
        edges = [i for (i,j) in enumerate(G[u]) if j > 0 and j < 999]
        # print(edges)
        for v in edges:
            if dist[v] > dist[u] + G[u][v] and visited[v] == False:
                dist[v] = dist[u] + G[u][v]
                pathlength[v] += 1
                prev[v] = u
                heapq.heappush(H,(dist[v],v))
            # print(G[u][v])
    
    print("dist",dist)

    return dist

if __name__ == '__main__':
    G = [
        [0,7,3,999,3,999],
        [7,0,1,2,999,6],
        [3,1,0,5,2,999],
        [999,2,5,0,0.5,999],
        [3,999,2,0.5,0,999],
        [999,6,999,999,999,0]
    ]
    print(dijkstra(G,1))
    