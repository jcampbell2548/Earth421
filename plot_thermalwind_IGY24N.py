import numpy as np
from scipy.io import loadmat
import matplotlib
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


# ##### This script computes thermal wind from mid-ocean location in IGY 24N section.
# 
# ### Define constants

# Compute value of Coriolis parameter at 24N
f = 2 * (2*np.pi) * (1/86164) * np.sin(np.deg2rad(24)) # units 1/s

# Set value of gravitational acceleration g
g = 9.8 # units m/s^2

# Set value of rho_0 (average seawater density)
rho0 = 1035 # units kg/m^3

# Define radius of the Earth
R = 6371000 # m


# ### Load data

data = loadmat('igy24n_gVSpressure_gr.mat')
print(data.keys())

xax = np.squeeze(data['xax'])
yax = np.squeeze(data['yax'])
zz = data['zz'] # neutral density
print(xax.shape,yax.shape,zz.shape)


# ### Plot density contours

# Set the default fontsize
font = {'size'   : 18}
matplotlib.rc('font', **font)

plt.figure(figsize=(12,8))
plt.contourf(xax,yax,zz)
plt.gca().invert_yaxis()
plt.xlabel('Longitude (degrees)')
plt.ylabel('Pressure (db)')
plt.title('Neutral density along IGY 24N section')
plt.colorbar()

plt.savefig('Neutral_density_IGY24N.png')


# #### Find a location in the middle of the gyre to compute thermal wind

index = np.where(xax==-40)[0][0]
print(index)


# We will compute the thermal wind with a centered difference, using the gridpoints on either side of this (indices 69 and 71). 
# 
# #### Compute deltax, the distance between indices 70 and 72 on the grid xax

deltax_degrees = xax[index+1] - xax[index-1]
deltax = 2 * np.pi * R * (deltax_degrees/360) * np.cos(np.deg2rad(24)) # units: m


# ### Compute thermal wind

dvdz = -(g/(f * rho0)) * (zz[:,index+1] - zz[:,index-1]) / deltax # units: 1/s


# ### Plot the thermal wind

plt.figure(figsize=(12,8))
plt.plot(dvdz,yax)
plt.gca().invert_yaxis()
plt.xlabel('dv/dz (s$^{-1}$)')
plt.ticklabel_format(axis='x', style='sci', scilimits=(-2,2)) # set xticklabel to scientific notation
plt.ylabel('Pressure (db)')
plt.title('Thermal wind dv/dz at 40W, IGY 24N')

plt.savefig('Thermal_wind_IGY24N_40W.png')


# ### Compute velocity v, assuming a value of zero at the bottom

dz = 50 # 50 dbar grid spacing in vertical - as one can see by checking 'yax'

# We want to find the length of values of dvdz that are not nan (there are several nan values
# at the bottom of the seafloor)
length_good = (~np.isnan(dvdz)).sum()
print(length_good)


# Define v
v = np.zeros(length_good) # initialize the array
for m in np.arange(2,length_good+1):
    n = length_good - m
    v[n] = v[n+1] + dvdz[n] * dz


# ### Plot velocity v

plt.figure(figsize=(12,8))
plt.plot(v[:-1],yax[:length_good-1])
plt.gca().invert_yaxis()
plt.xlabel('v (ms$^{-1}$) offset from unknown bottom velocity')
plt.ylabel('Pressure (db)')
plt.title('v at 40W, IGY 24N')
plt.savefig('v_IGY24N.png')





