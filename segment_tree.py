class BIT:
  def __init__(self, n):
    self.tree = [0]*(n+1)
    self.len = n
  
  def sum(self, i):
    ret = 0
    while i > 0:
      ret += self.tree[i]
      i -= i & -i
    return ret

  def add(self, i, x):
    while i <= self.len:
      self.tree[i] += x
      i += i & -i

# class SegmentTree:
#   __all__ = ['setval', 'pointupdate', 'segquery', 'segsearch_right', 'pointgetval']
#   def __init__(self, n=10**6, idetify_elt=-10**9, func=max):
#     assert (func(idetify_elt, idetify_elt) == idetify_elt)
#     self._n = n
#     self._seg_length_half = 2**(n-1).bit_length()
#     self._idetify_elt = idetify_elt
#     self._seg = [idetify_elt]*(2*self._seg_length_half)
#     self._func = func

#   def setval(self, x_list):
#     '''Set value : A = x_list'''
#     assert (len(x_list) == self._n)
#     # Set value at the bottom
#     for i in range(self._n):
#       self._seg[i+self._seg_length_half-1] = x_list[i]    
#     # Build value
#     for i in range(self._seg_length_half-2, -1, -1):
#       self._seg[i] = self._func(self._seg[2*i+1], self._seg[2*i+2])

#   def pointupdate(self, k, x):
#     '''Update : A[k] = x '''
#     pos = k + self._seg_length_half - 1
#     # Set value at k-th
#     self._seg[pos] = x
#     # Build bottom-up
#     while pos:
#       pos = (pos-1)//2
#       self._seg[pos] = self._func(self._seg[pos*2+1], self._seg[pos*2+2])

#   def pointgetval(self, k):
#     ''' Return A[k] '''
#     return self._seg[k + self._seg_length_half - 1]

#   def segquery(self, left, right):
#     ''' Return func(A[left], ... , A[right-1]) '''
#     # if not left < right
#     if right <= left:
#       return self._idetify_elt
      
#     func_value = self._idetify_elt
#     leftpos = left + self._seg_length_half - 1 # leftmost segment
#     rightpos = right + self._seg_length_half - 2 # rightmost segment

#     while leftpos < rightpos-1:
#       if leftpos&1 == 0:
#         # if leftpos is right-child
#         func_value = self._func(func_value, self._seg[leftpos])
#       if rightpos&1 == 1:
#         # if rightpos is leftchild
#         func_value = self._func(func_value, self._seg[rightpos])
#         rightpos -= 1
#       # move up
#       leftpos = leftpos//2
#       rightpos = (rightpos-1)//2
    
#     func_value = self._func(func_value, self._seg[leftpos])
#     if leftpos != rightpos:
#       func_value = self._func(func_value, self._seg[rightpos])
#     return func_value

#   def segsearch_right(self, condfunc, left=0):
#     ''' Return min_i satisfying condfunc( func( A[left], ... , A[i])) 
#     if impossible : return n
#     '''
#     # if impossible (ie. condfunc( func( A[left], ... , A[-1])) is False)
#     if not condfunc(self.segquery(left, self._n)):
#       return self._n
    
#     # possible
#     func_value = self._idetify_elt
#     rightpos = left + self._seg_length_half - 1
#     while True: 
#       # while rightpos is the left-child, move bottom-up
#       while rightpos&1 == 1:
#         rightpos //= 2
#       # try
#       up_value_trial = self._func(func_value, self._seg[rightpos])
#       if not condfunc(up_value_trial):
#         # move up and right
#         func_value = up_value_trial
#         rightpos = (rightpos-1)//2 + 1
#       else:
#         # move top-down
#         while rightpos < self._seg_length_half-1:
#           down_value_trial = self._func(func_value, self._seg[rightpos*2 + 1])
#           if condfunc(down_value_trial):
#             # move left-child
#             rightpos = rightpos*2 + 1
#           else:
#             # move right-child
#             func_value = down_value_trial
#             rightpos = rightpos*2 + 2
#         return rightpos - self._seg_length_half + 1

class SegmentTree:
  def __init__(self, n, identity_elt, op):
    self._n = n
    self._height = (n-1).bit_length() + 1
    self._size = 1<<(self._height - 1)
    self._identity_elt = identity_elt
    self._op = op
    self._data = [identity_elt]*(2*self._size)

  def getval(self, k):
    ''' Return A[k] '''
    return self._data[k+self._size]

  def setval(self, k, x):
    ''' Set value : A[k] = x '''
    k += self._size
    self._data[k] = x
    for i in range(1, self._height):
      p = k>>i
      self._data[p] = self._op(self._data[2*p], self._data[2*p+1])

  def setvals(self, x_list):
    ''' Set value : A = x_list '''
    for i in range(self._n):
      self._data[i+self._size] = x_list[i]
    for i in range(self._size-1, 0, -1):
      self._data[i] = self._op(self._data[2*i], self._data[2*i+1])

  def query(self, left, right):
    ''' Return op(A[left], ... , A[right-1]) '''
    if right <= left:
      return self._identity_elt
    left += self._size; right += self._size
    accl = self._identity_elt; accr = self._identity_elt
    while left < right:
      if left & 1:
        # if left is right-child
        accl = self._op(accl, self._data[left])
        left += 1
      if right & 1:
        # if right is left-child
        right -= 1
        accr = self._op(self._data[right], accr)

      left >>= 1; right >>= 1
    return self._op(accl, accr)

  def max_right(self, condfn, left=0):
    ''' Binary search maximum i satisfying condfn( op( A[left], ... , A[i-1])) '''
    assert condfn(self._identity_elt)
    acc = self._identity_elt
    pos = left + self._size

    while True:
      while not (pos & 1):
        pos >>= 1

      # pos is right-child
      if not condfn(self._op(acc, self._data[pos])):
        while pos < self._size:
          pos <<= 1
          if condfn(self._op(acc, self._data[pos])):
            acc = self._op(acc, self._data[pos])
            pos += 1
        return pos - self._size
      acc = self._op(acc, self._data[pos])
      pos += 1
      if pos & (pos-1) == 0:
        break

    return self._n

  def min_right(self, condfn, left=0):
    ''' Binary search minimum i satisfying condfn( op( A[left], ... , A[i]))
    if impossible : return n
    '''
    return self.max_right(lambda e: not condfn(e), left)
  
  def min_left(self, condfn, right):
    ''' Binary search maximum i satisfying condfn( op( A[i], ... , A[right-1])) '''
    assert condfn(self._identity_elt)
    acc = self._identity_elt
    pos = right + self._size

    while True:
      pos -= 1
      while pos > 1 and (pos & 1):
        pos >>= 1

      # pos is right-child
      if not condfn(self._op(self._data[pos], acc)):
        while pos < self._size:
          pos = 2 * pos + 1
          if condfn(self._op(self._data[pos], acc)):
            acc = self._op(self._data[pos], acc)
            pos -= 1
        return pos + 1 - self._size
      acc = self._op(self._data[pos], acc)
      if pos & (pos-1) == 0:
        break

    return 0

  def max_left(self, condfn, right):
    ''' Binary search maximum i satisfying condfn( op( A[i], ... , A[right]))
    if impossible : return -1
    '''
    return self.min_left(lambda e: not condfn(e), right) - 1

class F:
  def __init__(self):
    ''' Return identity mapping '''

  def mapping(self, x):
    ''' Return f(x) '''

  def composition(self, g):
    ''' Return h = fg '''
    h = F()
    return h

class LazySegmentTree:
  def __init__(self, n, identity_elt, op, F):
    self._n = n
    self._height = (n-1).bit_length() + 1
    self._size = 1<<(self._height - 1)
    self._identity_elt = identity_elt
    self._op = op
    self._F = F
    self._data = [identity_elt for _ in range(2*self._size)]
    self._lazy = [F() for _ in range(self._size)]

  def setvals_init(self, x_list):
    ''' Set value : A = x_list
    Note: You can call this function only at first !!!!
    '''
    for i in range(self._n):
      self._data[i+self._size] = x_list[i]
    for i in range(self._size-1, 0, -1):
      self._data[i] = self._op(self._data[2*i], self._data[2*i+1])

  def _mapping_and_composition(self, k, f):
    self._data[k] = f.mapping(self._data[k])
    if k < self._size:
      self._lazy[k] = f.composition(self._lazy[k])

  def _composition_childs(self, k):
    self._mapping_and_composition(2*k, self._lazy[k])
    self._mapping_and_composition(2*k+1, self._lazy[k])
    self._lazy[k] = self._F()

  def getval(self, k):
    ''' Return A[k] '''
    k += self._size
    for i in range(self._height-1, 0, -1):
      self._composition_childs(k >> i)
    return self._data[k]

  def setval(self, k, x):
    ''' Set value : A[k] = x '''
    k += self._size
    for i in range(self._height-1, 0, -1):
      self._composition_childs(k >> i)
    self._data[k] = x
    for i in range(1, self._height):
      p = k>>i
      self._data[p] = self._op(self._data[2*p], self._data[2*p+1])

  def query(self, left, right):
    ''' Return op(A[left], ... , A[right-1]) '''
    if right <= left:
      return self._identity_elt
    left += self._size; right += self._size

    ####################################################
    for i in range(self._height-1, 0, -1):
      if ((left >> i) << i) != left:
        self._composition_childs(left >> i)
      if ((right >> i) << i) != right:
        self._composition_childs((right - 1) >> i)
    ####################################################

    accl = self._identity_elt; accr = self._identity_elt
    while left < right:
      if left & 1:
        # if left is right-child
        accl = self._op(accl, self._data[left])
        left += 1
      if right & 1:
        # if left is left-child
        right -= 1
        accr = self._op(self._data[right], accr)

      left >>= 1; right >>= 1
    return self._op(accl, accr)

  ####################################################
  def apply_to(self, k, f):
    k += self._size
    for i in range(self._height-1, 0, -1):
      self._composition_childs(k >> i)
    self._data[k] = f.mapping(self._data[k])
    for i in range(1, self._height):
      p = k>>i
      self._data[p] = self._op(self._data[2*p], self._data[2*p+1])

  def apply(self, left, right, f):
    if right <= left:
      return
    left += self._size; right += self._size

    for i in range(self._height-1, 0, -1):
      if ((left >> i) << i) != left:
        self._composition_childs(left >> i)
      if ((right >> i) << i) != right:
        self._composition_childs((right - 1) >> i)

    l = left; r = right
    while l < r:
      if l & 1:
        # if left is right-child
        self._mapping_and_composition(l, f)
        l += 1
      if r & 1:
        # if right is left-child
        r -= 1
        self._mapping_and_composition(r, f)
      l >>= 1; r >>= 1

    for i in range(1, self._height):
      if ((left >> i) << i) != left:
        p = left >> i
        self._data[p] = self._op(self._data[2*p], self._data[2*p+1])
      if ((right >> i) << i) != right:
        p = (right-1) >> i
        self._data[p] = self._op(self._data[2*p], self._data[2*p+1])
  ####################################################

  def max_right(self, condfn, left=0):
    ''' Binary search maximum i satisfying condfn( op( A[left], ... , A[i-1])) '''
    assert condfn(self._identity_elt)
    acc = self._identity_elt
    pos = left + self._size

    ####################################################
    for i in range(self._height-1, 0, -1):
      self._composition_childs(pos >> i)
    ####################################################

    while True:
      while not (pos & 1):
        pos >>= 1

      # pos is right-child
      if not condfn(self._op(acc, self._data[pos])):
        while pos < self._size:
          ####################################################
          self._composition_childs(pos)
          ####################################################
          pos <<= 1
          if condfn(self._op(acc, self._data[pos])):
            acc = self._op(acc, self._data[pos])
            pos += 1
        return pos - self._size
      acc = self._op(acc, self._data[pos])
      pos += 1
      if pos & (pos-1) == 0:
        break

    return self._n

  def min_right(self, condfn, left=0):
    ''' Binary search minimum i satisfying condfn( op( A[left], ... , A[i]))
    if impossible : return n
    '''
    return self.max_right(lambda e: not condfn(e), left)
  
  def min_left(self, condfn, right):
    ''' Binary search maximum i satisfying condfn( op( A[i], ... , A[right-1])) '''
    assert condfn(self._identity_elt)
    acc = self._identity_elt
    pos = right + self._size

    ####################################################
    for i in range(self._height-1, 0, -1):
      self._composition_childs((pos-1) >> i)
    ####################################################

    while True:
      pos -= 1
      while pos > 1 and (pos & 1):
        pos >>= 1

      # pos is right-child
      if not condfn(self._op(self._data[pos], acc)):
        while pos < self._size:
          ####################################################
          self._composition_childs(pos)
          ####################################################
          pos = 2 * pos + 1
          if condfn(self._op(self._data[pos], acc)):
            acc = self._op(self._data[pos], acc)
            pos -= 1
        return pos + 1 - self._size
      acc = self._op(self._data[pos], acc)
      if pos & (pos-1) == 0:
        break

    return 0

  def max_left(self, condfn, right):
    ''' Binary search maximum i satisfying condfn( op( A[i], ... , A[right]))
    if impossible : return -1
    '''
    return self.min_left(lambda e: not condfn(e), right) - 1