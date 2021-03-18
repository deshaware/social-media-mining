from collections import deque

def BFS(G, src, dest):
	result = []
	dist = [999] * len(G)
	path = [0] * len(G)

	Q = deque()
	Q.append(src)

	dist[src] = 0
	path[src] = -1

	while len(Q) != 0:
		u = Q.popleft()
		if u == dest:
			result.append(path)
		
		edges = [i for (i,j) in enumerate(G[u]) if j > 0 and j < 999]

		for v in edges:
			# if dist[v] == 999:
			# 	dist[v] = dist[u] + 1
				path[v] = u
				Q.append(v)
			# if dist[v] < dist[u] + G[u][v]:
			# # 	dist[v] = dist[u] + G[u][v]
			# 	path[v] = u
			# 	Q.append(v)	

	return result
	
if __name__ == '__main__':
    	G = [ 
			[0, 2, 2, 999, 999, 999],
			[2, 0, 999, 2, 999, 999],
			[2, 999, 0, 999, 2, 999],
			[999, 2, 999, 0, 999, 2],
			[999, 999, 2, 999, 0, 999],
			[999, 999, 999, 2, 999, 0]
		]
    	print(BFS(G,0,5))
	

