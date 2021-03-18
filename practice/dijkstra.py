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
    # G = [[0,7,3,0,3],
    # [7,0,1,2,0],
    # [3,1,0,5,2],
    # [0,2,5,0,3],
    # [3,0,2,3,0],
    # ]
    # G = [
    #     [0,10,4,999,3],
    #     [10,0,1,2,999],
    #     [4,1,0,5,2],
    #     [999,2,5,0,999],
    #     [3,999,2,999,0],
    # ]

    # G = [
    #     [0, 4, 3, 6, 3, 10], 
    #     [4, 0, 1, 2, 3, 6], 
    #     [3, 1, 0, 3, 2, 7], 
    #     [6, 2, 3, 0, 5, 8], 
    #     [3, 3, 2, 5, 0, 9], 
    #     [10, 6, 7, 8, 9, 0]
    #     ]
    # dijkstra(G,1)
    # G2 = [[0] * len(G)] * len(G)
    # for i in range(len(G)):
    #     G2[i] = dijkstra(G,i)
    
    print(dijkstra(G,0))