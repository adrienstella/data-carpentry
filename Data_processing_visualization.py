#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 15:22:17 2022

@author: Adrien
"""

import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import cmocean

def plot_pr_climatology(file_path, season, gridlines = True):
    """Plot the precipitation climatology.
    
    (note: what you write here shows up in the 'help' of the function!
     use it to describe general purpose and arguments. try with help(plot_pr_climatology))
    
    Args:
      file_path (str): Path to precipitation data file
      season (str): Season (3 letter abbreviation, e.g. JJA)
      gridlines (bool): Select whether to plot gridlines
    
    """
    
    
    dset = xr.open_dataset(file_path) #we just created an xarray! It's a high-level class of numpy ndarray.
    #print(dset) #basically an ncdump - prints all metadata in the ncdf file
    
    #print(dset.pr) #Only the precipitation variable
    
    clim = dset.pr.groupby('time.season').mean('time', keep_attrs=True)
    #print(clim)
    
    clim.data = clim.data * 86400
    clim.attrs['units'] = 'mm/day' #changing the units from kg/m2/s to mm/day
    
    #print(clim)
    
    #now you could plot with matplotlib but xarray devs have made life easier
    #they built upon pyplot to make it simple to plot stuff in xarrays
    
    fig = plt.figure(figsize=[12,5]) #create figure
    ax = fig.add_subplot(111, projection=ccrs.PlateCarree(central_longitude=180)) #add plot and choose projection
    
    clim.sel(season = season).plot.contourf(ax=ax,
                       levels=np.arange(0, 13.5, 1.5),
                       extend='max',
                       transform=ccrs.PlateCarree(),
                       cbar_kwargs={'label': clim.units},
                       cmap=cmocean.cm.haline_r) #use the plot method of the xarray class (I think?) and more specifically here the contour plot.
    ax.coastlines() # add a coastline layer I guess?
    if(gridlines):
        ax.gridlines()
    
    
    model = dset.attrs['source_id']
    
    title = f'{model} precipitation climatology {season}'
    plt.title(title)

plot_pr_climatology('data/pr_Amon_ACCESS-CM2_historical_r1i1p1f1_gn_201001-201412.nc', 'JJA')
plt.show()

plot_pr_climatology('data/pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412.nc', 'DJF')
plt.show()

plot_pr_climatology('data/pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412.nc',
                    'DJF', gridlines=True)
plt.show()

