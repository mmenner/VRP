import seaborn 
import matplotlib.pyplot as plt
import numpy as np

def plot_stores(location_df, pickup_df, fig_title = 'map', d=[], plot_demand = False, RP=None, plot_route = False):
  ax = seaborn.scatterplot(x="x", y="y", data=location_df)
  ax = seaborn.scatterplot(x="x", y="y", data=pickup_df, color = 'r')
  ax.set_title(fig_title)

  if plot_route:
    for vehicle in RP.all_paths:
      col = (np.random.randint(0,100)/100,np.random.randint(0,100)/100,np.random.randint(0,100)/100)
      paths = [0] + RP.all_paths[vehicle] 
      for i in range(len(paths)-1):
        v1 = loc[paths[i]]
        v2 = loc[paths[i+1]]
        plt.plot([v1[0], v2[0]], [v1[1], v2[1]], linewidth=2, color = col) 

  if plot_demand:
    for i, dmd in enumerate(d):
      if i>0:
        plt.text(location_df.x.values[i]+0.2, location_df.y.values[i]+0.2, dmd)
    return 0
