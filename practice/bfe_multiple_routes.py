def BFS(G, src, dest):
    dist = [0] * len(G)
    path = [0] * len(G)
    path_info = dict()

    dist[src] = -1

    queue = []

    queue.append(src)

    while len(queue) != 0:
        u = queue.pop(0)
        #take edges from the queue
        edges = [i for (i,j) in enumerate(G[u]) if j > 0 and j < 999]
        

if __name__ == '__main__':
    G = [[]]
    BFS(G,1,2)
    