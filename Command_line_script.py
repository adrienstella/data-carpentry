#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 15:22:17 2022

A program to plot precipitation climatology

@author: Adrien
"""


# A call example from command line:
# python Command_line_script.py data/pr_Amon_ACCESS-CM2_historical_r1i1p1f1_gn_201001-201412.nc MAM pr_ACCESS-CM2_MAM_test.png --gridlines


# import packages
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import cmocean
import argparse

# import local modules
import unit_conversion


def create_plot(clim, model, season, gridlines = False):
    """
    plot the precipitation climatology

    Args
    ----------
    clim : xarray.DataArray
        the climatology data.
    model : str
        the name of the model/data source.
    season : str
        the season used to compute clim - 3 letter code.
    
    Kwargs
    ----------
    gridlines : bool
        do you want to display gridlines?

    Returns
    -------
    None.

    """
    
    fig = plt.figure(figsize=[12,5]) #create figure
    ax = fig.add_subplot(111, projection=ccrs.PlateCarree(central_longitude=180)) #add plot and choose projection
    
    clim.sel(season = season).plot.contourf(ax=ax,
                       levels=np.arange(0, 13.5, 1.5),
                       extend='max',
                       transform=ccrs.PlateCarree(),
                       cbar_kwargs={'label': clim.units},
                       cmap=cmocean.cm.haline_r) 
    ax.coastlines()
    if(gridlines):
        ax.gridlines()
    
    title = f'{model} precipitation climatology {season}'
    plt.title(title)
    
def main(inargs):
    """Run the program"""
    
    dset = xr.open_dataset(inargs.pr_file) # create an xarray
    clim = dset['pr'].groupby('time.season').mean('time', keep_attrs=True)
    clim = unit_conversion.convert_pr_units(clim) # I defined this function in a scripts that collects all unit conversions and then imported it.
    create_plot(clim, dset.attrs['source_id'], inargs.season, gridlines=inargs.gridlines)
    plt.savefig(inargs.output_file, dpi=72)
    
if __name__ == '__main__':
    description='Plot the precipitation climatology.'
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument("pr_file", type=str, help="Precipitation data file")
    parser.add_argument("season", type=str, choices=['JJA','SON','DJF','MAM'], help="Season to plot")
    parser.add_argument("output_file", type=str, help="Output file name")
    parser.add_argument("-g", "--gridlines", action = "store_true", default = False, help = "Toggles gridlines on plot")

    args = parser.parse_args()
    
    main(args)    
