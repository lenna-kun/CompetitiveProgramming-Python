class UnionFind():
  def __init__(self, n):
    self.groups = n
    self.parents = [-1]*n

  def find(self, x):
    if self.parents[x] < 0:
      return x
    else:
      self.parents[x] = self.find(self.parents[x])
      return self.parents[x]

  def unite(self, x, y):
    x = self.find(x)
    y = self.find(y)

    # already united
    if x == y:
      return

    self.groups -= 1

    if self.parents[x] > self.parents[y]:
      x, y = y, x

    self.parents[x] += self.parents[y]
    self.parents[y] = x

  def size(self, x):
    return -self.parents[self.find(x)]

  def issame(self, x, y):
    return self.find(x) == self.find(y)

  def roots(self):
    return [i for i, x in enumerate(self.parents) if x < 0]

  def group_count(self):
    return self.groups