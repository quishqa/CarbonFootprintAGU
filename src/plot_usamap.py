import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from cmocean import cm as cmo
import cartopy.io.shapereader as shpreader
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection

## read data
path = "git/CarbonFootprintAGU/data/"
df = pd.read_csv(path+"locations_geolocated.csv")
n = len(df)

## Great circle, equi-distant projection
# higher resolution for great circles

SFOloc = (37.622452, -122.384071607814)

##
fig = plt.figure(figsize=(7.3,6))
#ax = fig.add_subplot(1, 1, 1, projection=ccrs.LambertConformal())
#ax.set_extent([-120, -75, 20, 52], crs=ccrs.Geodetic())

proj = ccrs.AzimuthalEquidistant(central_latitude=SFOloc[0],central_longitude=SFOloc[1])
ax = fig.add_subplot(1,1,1,projection=proj)

ax.set_xlim(-7e5,4.7e6)
ax.set_ylim(-2e6,2.6e6)

ax.add_feature(cfeature.OCEAN,facecolor="#97BACD",zorder=-2)
ax.add_feature(cfeature.LAND)
#ax.add_feature(cfeature.COASTLINE,lw=1,alpha=0.2)
ax.coastlines(resolution="50m")
ax.add_feature(cfeature.BORDERS,lw=0.5,alpha=1)
ax.add_feature(cfeature.LAKES,facecolor="#97BACD",zorder=0.1)

states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='110m',
        facecolor='none')

ax.add_feature(states_provinces, edgecolor='gray',zorder=0)


# circles
patches = []
patches.append(Circle((0, 0), 2e6))     # 2000km 
patches.append(Circle((0, 0), 4e6))     # 4000km
p = PatchCollection(patches, alpha=.5, facecolor="none",edgecolor="k",lw=0.5)
#p.set_array(np.array(colors))
ax.add_collection(p)

# text of circles
alignment = {'ha': 'center', 'va': 'center'}
ax.text(1.6e6,-1.05e6,"2000km",**alignment,alpha=0.5,rotation=55)
ax.text(3.8e6,-8.628e5,"4000km",**alignment,alpha=0.5,rotation=78)

colr = "#D71455"
ax.scatter(df["lon"],df["lat"],0.2+7*np.sqrt(df["N"]),c=df["N"]**(1/6), transform=ccrs.Geodetic(), cmap=cmo.thermal,alpha=.9,edgecolor="k",lw=0.1)

# for legend
nums = [1,50,250,1000]
for num in nums:
    ax.scatter(0,0,0.2+7*np.sqrt(num),c=[cmo.thermal(256*num**(1/6)/800)],label="{:d}".format(num),transform=ccrs.Geodetic(),alpha=.6,edgecolor="k",lw=0.5)
    
ax.scatter(SFOloc[1],SFOloc[0],100,c="lightgreen",marker="*",label="San Francisco",zorder=10,edgecolor="k",lw=0.7,transform=ccrs.Geodetic())

ax.set_title("Attendees of AGU Fall Meeting 2019",loc="left",fontweight="bold")
plt.legend(loc=3,title="# of attendees")

#plt.tight_layout()
plt.show()