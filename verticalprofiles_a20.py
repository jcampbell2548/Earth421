import gsw
from scipy.io import loadmat
import matplotlib.pyplot as plt
import matplotlib


# Load data

data = loadmat('a20_station64.mat')
#print(data.keys()) # This prints the names of the variables in "data"

salinity = data['salinity']
pressure = data['pressure']
temperature = data['temperature']


# Compute potential temperature

potentialtemp = gsw.pt0_from_t(salinity,temperature,pressure)
#print('potentialtemp dimensions = ',potentialtemp.shape) # This prints the dimensions of the variable potentialtemp


# Plot vertical profiles of temperature and potential temperature

plt.figure(figsize=(12,8))
plt.plot(temperature,pressure,'k')
plt.plot(potentialtemp,pressure,'k--')
plt.gca().invert_yaxis() # Invert y-axis so that zero-pressure is at the top
plt.xlabel('Temperature (degrees Celsius)',fontsize=18)
plt.xticks(fontsize=14)
plt.ylabel('Pressure (db)',fontsize=18)
plt.yticks(fontsize=14)
plt.title('Temperature (solid line) versus potential temperature (dashed line)',fontsize=22)
plt.xlim(0,30)
plt.ylim(6000,0)
plt.savefig('temperature_verticalprofile.png')


# Plot vertical profile of salinity

plt.figure(figsize=(12,8))
plt.plot(salinity,pressure,'k')
plt.gca().invert_yaxis()
plt.xlabel('Salinity (psu)',fontsize=18)
plt.ylabel('Pressure (db)',fontsize=18)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.title('Vertical profile of salinity',fontsize=22)
plt.ylim(6000,0)
plt.xlim(34,38)
plt.savefig('salinity_verticalprofile.png')


# Plot potential temperature-salinity diagram

plt.figure(figsize=(12,8))
plt.plot(salinity,potentialtemp,'k.')
plt.xlim(34,38)
plt.ylim(0,30)
plt.xlabel('Salinity (psu)',fontsize=18)
plt.ylabel('Potential temperature (degrees C)',fontsize=18)
plt.title('Potential temperature-salinity diagram',fontsize=22)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.savefig('thetasalinity.png')


# Compute density and three flavors of potential density, referenced to three different depths

# First convert in situ temperature into conservative temperature (needed for inputs in the following functions)
cons_temperature = gsw.CT_from_t(salinity,temperature,pressure)

density = gsw.rho(salinity,cons_temperature,pressure)
sigma0 = gsw.sigma0(salinity,cons_temperature) + 1000 # Note: in the documentation, it explains that there is an offset by 1000 that we account for here
sigma2000 = gsw.sigma2(salinity,cons_temperature) + 1000
sigma4000 = gsw.sigma4(salinity,cons_temperature) + 1000


# Plot density versus potential densities

plt.figure(figsize=(12,8))
plt.plot(density,pressure,'k-')
plt.plot(sigma0,pressure,'k--') 
plt.plot(sigma2000,pressure,'k:')
plt.plot(sigma4000,pressure,'k-.')
plt.ylim(6000,0)
plt.xlim(1020,1060)
plt.xlabel('Density (kg m$^{-3}$)',fontsize=18)
plt.ylabel('Pressure (db)',fontsize=18)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.title('Density (solid) vs $\sigma_0$ (dashed), $\sigma_{2000}$ (dotted), and $\sigma_{4000}$ (dash-dotted)',fontsize=22)
plt.savefig('density_verticalprofile.png')





