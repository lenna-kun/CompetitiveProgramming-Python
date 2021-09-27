MOD = ??

# 組合せ計算用前準備
def init(n): # O(n)
  fact = [1]*(n+1)
  rfact = [1]*(n+1)
  r = 1
  for i in range(1, n+1):
    fact[i] = r = r * i % MOD
  rfact[n] = r = pow(fact[n], MOD-2, MOD)
  for i in range(n, 0, -1):
    rfact[i-1] = r = r * i % MOD
  return fact, rfact

# nPk (mod MOD)
def perm(fact, rfact, n, k):
  return fact[n] * rfact[n-k] % MOD

# nCk (mod MOD)
def comb(fact, rfact, n, k):
  return fact[n] * rfact[k] * rfact[n-k] % MOD

# nHk (mod MOD)
def homb(fact, rfact, n, k):
  return comb(fact, rfact, n+k-1, k)