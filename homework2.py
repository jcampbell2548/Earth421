from scipy.io import loadmat
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from mpl_toolkits.basemap import Basemap
import warnings
warnings.filterwarnings('ignore')


# Load data

data = loadmat('nogapswinds.mat')
print(data.keys())

lons = data['lons']
lats = data['lats']
ujanuary = data['ujanuary']
vjanuary = data['vjanuary']
ujuly = data['ujuly']
vjuly = data['vjuly']


# Define variables to plot

x,y = np.meshgrid(lons,lats)
#print(x.shape,y.shape)

# "Decimate" the variables
xdecimate = x[::8,::8]
ydecimate = y[::8,::8]
ujanuarydecimate = ujanuary[::8,::8]
vjanuarydecimate = vjanuary[::8,::8]
ujulydecimate = ujuly[::8,::8]
vjulydecimate = vjuly[::8,::8]


# Plot 1: January winds

# First set the default fontsize
font = {'size'   : 18}
matplotlib.rc('font', **font)

plt.figure(figsize=(12,12))
m = Basemap(projection='cyl',llcrnrlat=-80,llcrnrlon=0,urcrnrlat=80,urcrnrlon=360)
m.drawcoastlines()
m.quiver(xdecimate,ydecimate,ujanuarydecimate,vjanuarydecimate,color='b')
meridians = np.arange(0,360,50)
m.drawmeridians(meridians,labels=[1,0,0,1],linewidth=0.5);
parallels = np.arange(-90,90,30)
m.drawparallels(parallels,labels=[1,0,0,1],linewidth=0.5);
plt.title('January winds (m/s)');


# Plot 2: July winds

plt.figure(figsize=(12,12))
m = Basemap(projection='cyl',llcrnrlat=-90,llcrnrlon=0,urcrnrlat=90,urcrnrlon=360,lat_ts=20,resolution='l')
m.drawcoastlines()
m.quiver(xdecimate,ydecimate,ujulydecimate,vjulydecimate,color='b')
meridians = np.arange(0,360,50)
m.drawmeridians(meridians,labels=[1,0,0,1],linewidth=0.5);
parallels = np.arange(-90,90,30)
m.drawparallels(parallels,labels=[1,0,0,1],linewidth=0.5);
plt.title('July winds (m/s)');


# Plot 3: Zonal kinetic energy average of January winds

plt.figure(figsize=(12,8))
#print(lats.shape,ujanuary.shape,vjanuary.shape)
plt.plot(lats,np.mean((ujanuary**2 + vjanuary**2),axis=1))
plt.xlabel('Latitude (degrees)')
plt.ylabel('Kinetic energy ($m^2 s^{-2}$)')
plt.title('Zonal KE average of January winds')


# Create array dA of cell areas for the grid the winds are on

# Specify the size of dA
dA = np.zeros((576,1152))

# Radius of the Earth
r_Earth = 6371000 # meters

# Define dy
dy = 2*np.pi*r_Earth*0.3125/360

for m in np.arange(576):
    dA[m,:] = dy*dy*np.cos(np.deg2rad(lats[m]))




