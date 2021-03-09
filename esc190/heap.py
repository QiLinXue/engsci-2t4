import heapq 
heap = [5, 7, 9, 1, 3] 
heapq.heapify(heap) 
print(heap) # [1, 3, 9, 7, 5]

heapq.heappush(heap,4) 
print(heap) # [1, 3, 4, 7, 5, 9]

heapq.heappop(heap)
print(heap) # [3, 5, 4, 7, 9]