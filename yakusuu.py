import math
def eratosthenes(n):
  if not isinstance(n, int):
    raise TypeError('n is int type.')
  if n < 2:
    raise ValueError('n is more than 2')
  prime = []
  limit = math.sqrt(n)
  data = list(range(2, n+1))
  while True:
    p = data[0]
    if limit < p:
      return prime + data
    prime.append(p)
    data = [e for e in data if e % p != 0]

# 素因数分解の前準備
def sieve(n):
  data = [2, 0]*(n//2+5)
  for x in range(3, n+1, 2):
    if data[x] == 0:
      data[x] = x
      if x**2 > n: continue
      for y in range(x**2, n+5, 2*x):
        if data[y] == 0:
          data[y] = x
  return data
 
# 素因数分解
def pfct(data, n): # O(log(n))
  ret = []
  while n > 1:
    if ret and data[n] == ret[-1][0]:
      ret[-1][1] += 1
    else:
      ret.append([data[n], 1])
    n //= data[n]
  return ret

# 素因数分解
def factorization(n): # O(rt(n))
  ret = {}
  temp = n
  for i in range(2, int(-(-n**0.5//1))+1):
    if temp%i==0:
      cnt=0
      while temp%i==0:
        cnt+=1
        temp //= i
      ret[i] = cnt
  if temp!=1:
    ret[temp] = 1
  if ret == {} and n != 1:
    ret[n] = 1
  return ret

# 約数全列挙
def yakusuu(n): # O(sqrt(n))
  ret = []
  for i in range(1, n+1):
    if i * i > n:
      break
    if n % i == 0:
      ret.append(i)
      if i * i != n:
        ret.append(n // i)
  ret.sort()
  return ret

print(yakusuu(10))
# print(eratosthenes(4))
print(factorization(72))