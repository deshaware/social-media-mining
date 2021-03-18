import heapq
from typing import List


class MaxHeap:
    def __init__(self):
        self.data = []

    def top(self):
        return -self.data[0]

    def push(self, val):
        heapq.heappush(self.data, (val[0],-val[1]))

    def pop(self):
        pop = heapq.heappop(self.data)
        print(pop)

if __name__ == '__main__':
    heap = MaxHeap()
    heap.push(("A",0))
    heap.push(("B",3))
    heap.push(("C",5))
    print(heap)
    print(heap.pop())
    