
import numpy as np
import math
import pandas as pd
from sklearn.cluster import KMeans
from utils import plot_stores
from rp import RoutePlanner


#Optimal vehicle routing (MILP) combined with a clustering appraoch for local solvability
#Each vehicle starts at a pickup store and delivers customers with a set demand at set locations 

#Generate Data 
#fix pick up points
pick_ups = [[30,20], [75, 30], [20, 70], [80, 75]]
#total number of stores
N_full = 120
#Number of different clusters
N_clusters = len(pick_ups)
#capacity of truck
cap = 1000
#random location of stores
np.random.seed(0)
locs = [[np.random.uniform(0,100), np.random.uniform(0,100)] for i in range(1,N_full)]
locs_df = pd.DataFrame(data = locs, columns = ['x','y'])
pickups_df = pd.DataFrame(data = pick_ups, columns = ['x','y'])
#random demand at stores
np.random.seed(1)
d_full = list(np.random.randint(50,400, N_full))

#show map of stores (blue) and pickup points (red)
plot_stores(locs_df, pickups_df)


#Reduce problem to having only one pickup point by clusering stores to nearest pickup points
#If more time: More sophisticated approach
kmeans = KMeans(n_clusters=N_clusters)
kmeans.fit(pick_ups)
kmeans.cluster_centers_
clusters = kmeans.predict(locs)


#Iterate over cluster, solve optimization problem, visualize, and gather costs (time) for earch driven route.
#Optimization has a time limit set (per cluster), can be varied

LP_time_limit_seconds = 100
travel_cost = {}
plot_separate = False
for cl in range(N_clusters):
  #Generate required data within single cluster
  pick_up = list(kmeans.cluster_centers_[cl])
  pick_up_df = pd.DataFrame(data = [pick_up]+[pick_up], columns = ['x','y'])
  loc = []
  d = [0]
  for idx, l in enumerate(locs):
    if clusters[idx] == cl:
      loc = loc + [l]
      d.append(d_full[idx])
  loc   
  N=len(loc)+1
  loc = [pick_up] + loc
  loc_df = pd.DataFrame(data = loc, columns = ['x','y'])
  t = [[math.dist(loc[i],loc[j]) for i in range(len(loc))] for j in range(len(loc))]

  RP = RoutePlanner(N, cap, d, loc, t)
  RP.LP()
  RP.solve(solver = PULP_CBC_CMD(msg = False, maxSeconds = LP_time_limit_seconds))
  RP.trace()
  print(' ')
  print('vehicle paths, cluster: ',cl)
  print(RP.all_paths)
  print(' ')
  print('driving time / cost, cluster: ',cl)
  print(RP.d_travel)
  print(' ')

  if plot_separate:
    f = plt.figure(cl)
    f.set_figwidth(16)
    f.set_figheight(8)
    ftitle = 'cluster' + str(cl) 
  else:
    f = plt.figure(1)
    f.set_figwidth(25)
    f.set_figheight(13)
    ftitle = 'map'
  #Plot Stores
  travel_cost[cl] = RP.d_travel 
  plot_stores(loc_df, pick_up_df, fig_title = ftitle, d=d, plot_demand = True, RP=RP, plot_route = True)


