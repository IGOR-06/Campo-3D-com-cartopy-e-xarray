"""
https://cloud.tencent.com/developer/article/1821571
@author: igor
"""
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.collections import LineCollection , PolyCollection
from cartopy.mpl.patch import geos_to_path
import itertools

from cartopy.feature import ShapelyFeature # importando leitor para shape
from cartopy.io.shapereader import Reader

from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
# =============================================================================
# ######## abrir arquivo nc
# =============================================================================
dataset = xr.open_dataset('arquivo.nc')
# =============================================================================
# # Select the extent [min. lon, max. lon, min. lat, max. lat]
# =============================================================================
extent = [-50.0, -20.0, -30.0, -15.0] 
data = '2020-10-24T12:00:00'
# =============================================================================
# #selecionando o variaveis
# =============================================================================
field1 = dataset['vo'].sel(time=data,level=1000,
                           longitude=np.arange(extent[0],extent[1],0.25),
                           latitude=np.arange(extent[2],extent[3],0.25)
                           )*100000

field2 = dataset['vo'].sel(time=data,level=500,
                           longitude=np.arange(extent[0],extent[1],0.25),
                           latitude=np.arange(extent[2],extent[3],0.25)
                           )*100000

field3 = dataset['vo'].sel(time=data,level=200,
                           longitude=np.arange(extent[0],extent[1],0.25),
                           latitude=np.arange(extent[2],extent[3],0.25)
                           )*100000

x = dataset['longitude'].sel(longitude=np.arange(extent[0],extent[1],0.25)).values
y = dataset['latitude'].sel(latitude=np.arange(extent[2],extent[3],0.25)).values
z = dataset['level'].values
# =============================================================================
# # Create meshgrid for latitude, longitude, and depth
# =============================================================================
lons,lats = np.meshgrid(x,y)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_box_aspect(aspect = (2,2,4))

# =============================================================================
# # Field 1
# =============================================================================
C = ax.contourf(lons, lats, field1,cmap='RdBu_r', zdir='z',offset=1000, 
            extend='both',levels=np.arange(-10,10,1),zorder=0)

# Field 2
ax.contourf(lons, lats, field2,cmap='RdBu_r',zdir='z',offset=600,
            extend='both',levels=np.arange(-10,10,1))
# Field 3
ax.contourf(lons, lats, field3,cmap='RdBu_r',zdir='z',offset=200, 
                  extend='both',levels=np.arange(-10,10,1),zorder=3)

fig.colorbar(C, ax=ax, fraction=0.02, orientation='horizontal',pad=0.1, label='vorticidade relativa (1/s)')
# =============================================================================
# # Set axis labels
# =============================================================================
ax.xaxis.set_major_formatter(LongitudeFormatter())
ax.yaxis.set_major_formatter(LatitudeFormatter())

# ax.set_xlabel('Longitude')
# ax.set_ylabel('Latitude')
# ax.set_zlabel('Altitude(hPa)')

ax.set_xlim(extent[0],extent[1])
ax.set_ylim(extent[2],extent[3])
ax.set_zlim3d(1000,0)

# =============================================================================
# # Add coastlines
# =============================================================================
proj_ax=plt.figure().add_subplot(111,projection=ccrs.PlateCarree())
proj_ax.set_extent([extent[0],extent[1],extent[2],extent[3]],crs=ccrs.PlateCarree())
proj_ax.autoscale_view()

concat = lambda iterable: list(itertools.chain.from_iterable(iterable))
target_projection = proj_ax.projection
# =============================================================================
# # ----------------------------- add shapefile
# =============================================================================
###############################################################################
feature = cfeature.COASTLINE
# feature = mapa_amsul
geoms = feature.geometries()

boundary = proj_ax._get_extent_geom()
geoms = [target_projection.project_geometry(geom, feature.crs)
         for geom in geoms]
geoms2=[]
for i in range(len(geoms)):
    if geoms[i].is_valid:
        geoms2.append(geoms[i])
geoms=geoms2

geoms = [boundary.intersection(geom) for geom in geoms]
# =============================================================================
# # Convert the geometries to paths so we can use them in matplotlib.
# =============================================================================
paths = concat(geos_to_path(geom) for geom in geoms)
polys = concat(path.to_polygons() for path in paths)

# lc = LineCollection(polys, color='black')
# lc2 = LineCollection(polys, color='black')
lc = PolyCollection(polys, edgecolor='black',facecolor=None, closed=True)
lc2 = PolyCollection(polys, edgecolor='black',facecolor=None, closed=True)
lc3 = PolyCollection(polys, edgecolor='black',facecolor=None, closed=True)

ax.add_collection3d(lc, zs=1000)
ax.add_collection3d(lc2, zs=600)
ax.add_collection3d(lc3, zs = 200)
# =============================================================================
# # # Adjust the layout if necessary
plt.tight_layout()
# # # Show the plot
# =============================================================================
plt.close(proj_ax.figure)
plt.show()