from pulp import *
import numpy as np

#LP problem class to be reused multiple times for each cluster
class RoutePlanner:

  def __init__(self, N, cap, d, loc, t):
    self.N = N
    self.cap = cap
    self.loc = loc
    self.d = d
np    self.t = t
    self.loc_df = pd.DataFrame(data = loc, columns = ['x','y'])
    self.t_df = pd.DataFrame(data = t)


  def LP(self):
    x = pulp.LpVariable.dicts('travel', (range(self.N), range(self.N)), lowBound=0, upBound=1, cat='Binary')
    goods = pulp.LpVariable.dicts('goods', (range(self.N), range(self.N)), lowBound=0, cat = LpInteger)
    #Formulate problem and constraints
    prob = LpProblem("opt_route", LpMinimize)
    prob += lpSum([x[i][j] * self.t[i][j] for i in range(self.N) for j in range(self.N)])

    for i in range(1,self.N):
        prob += lpSum([x[i][j] for j in range(self.N)]) == 1
        prob += lpSum([x[j][i] for j in range(self.N)]) == 1
        prob += lpSum([goods[j][i] for j in range(self.N)]) - lpSum([goods[i][j] for j in range(self.N)]) == self.d[i] 

    for i in range(self.N):
      for j in range(self.N):
        prob += goods[i][j] <= x[i][j]*self.cap    
    self.x = x
    self.goods = goods
    self.prob = prob

  #Solve
  def solve(self, solver):
    self.solver = solver
    self.prob.solve(solver)
    self.x_map = [[self.x[i][j].varValue for i in range(self.N)] for j in range(self.N)]
    self.x_map[0][0] = 0
    self.goods_map = [[self.goods[i][j].varValue for i in range(self.N)] for j in range(self.N)]
    self.x_df = pd.DataFrame(data = self.x_map)
    self.goods_df = pd.DataFrame(data = self.goods_map)

  #Optimal paths and costs per route
  def trace(self):
    start = list(np.where(self.x_df.iloc[0] ==1)[0])
    self.d_travel = []
    self.all_paths = {}
    idx = 0
    for s in start:
      dist = 0
      iter = True
      path = [s]
      current = s
      while iter:
        next = np.where(self.x_df.iloc[current] ==1)[0][0]
        dist += self.t[current][next]
        path.append(next)
        current = next
        if next == 0:
          iter = False
          idx += 1
          self.all_paths[idx] = path
          self.d_travel.append(dist)
