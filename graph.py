INF = 10**18

# O(E log V)
from heapq import heappush, heappop
def dijkstra(s, n, g): # (始点, ノード数, グラフ情報) g: [[(to, cost), ...], ...]
  d = [INF] * n
  d[s] = 0
  hq = [(0, s)]
  while hq:
    p = heappop(hq)
    v = p[1]
    if d[v] < p[0]:
      continue
    for to, cost in g[v]:
      if d[to] > d[v] + cost:
        d[to] = d[v] + cost
        heappush(hq, (d[to], to))
  return d

# O(EV)
def belman_ford(s, n, g): # (始点, ノード数, グラフ情報) g: [[(to, cost), ...], ...]
  d = [INF] * n
  d[s] = 0
  update = 1
  for _ in range(n):
    update = 0
    for v, e in enumerate(g):
      for to, cost in e:
        if d[v] != INF and d[v] + cost < d[to]:
          d[to] = d[v] + cost
          update = 1
    if not update:
      break
  else:
    return None
  return d

# O(V^3)
def warshall_floyd(n, cost): # cost[i][j]: 頂点iから頂点jへ到達するための辺の重み(ただし，辺が存在しない場合はINF，cost[i][i]=0)
  for k in range(n):
    for i in range(n):
      for j in range(n):
        if cost[i][k] != INF and cost[k][j] != INF:
          cost[i][j] = min(cost[i][j], cost[i][k] + cost[k][j])
  # cost[i][j]: 頂点iから頂点jへ到達するための辺コストの和
  for i in range(n):
    if cost[i][i] < 0:
      return False
  return True