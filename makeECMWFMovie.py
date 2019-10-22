import pickle
from numpy import *
import numpy as np
layerS,ilayerS=pickle.load(open('layerS3.pklz','rb'))


import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
#from skimage.restoration import inpaint

#from pyresample import geometry, utils, image
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import matplotlib.colors as col

from pyresample import geometry, utils, image


area_id = 'ease_nh'
description = 'Arctic EASE grid'
proj_id = 'ease_nh'
x_size = 125
y_size = 125
area_extent = (-5326849.0625,-5326849.0625,5326849.0625,5326849.0625)
proj_dict = {'a': '6371228.0', 'units': 'm', 'lon_0': '0', \
             'proj': 'laea', 'lat_0': '90'}
area_def = geometry.AreaDefinition(area_id, description, proj_id, \
                                   proj_dict, x_size, y_size, area_extent)

x=-179.5+arange(360)
y=0.5+arange(90)
lons,lats=np.meshgrid(x,y)
grid_def = geometry.GridDefinition(lons=lons, lats=lats)


row_indices, \
    col_indices = \
                  utils.generate_nearest_neighbour_linesample_arrays(grid_def, area_def, 75000)




m = Basemap(projection='npstere',boundinglat=30,lon_0=-30,resolution='l')
import os
import matplotlib
matplotlib.rcParams.update({'font.size': 15})
dp=50
rhow=1000.
xfact=100.*dp/9.81/rhow
import datetime
st=datetime.datetime(2015,11,22,12,0)
fe=Dataset('2015Nov11_2015Dec3E_P.nc')
tp=fe['tp'][:,:,:]+fe['e'][:,:,:]
x=fe['longitude'][:]
y=fe['latitude'][:]
lonsE,latsE=np.meshgrid(x,y[1:-1])
ifig=1
x2,y2=m(lonsE,latsE)
for i in range(38,0,-1):
    ct=st+datetime.timedelta(hours=(38-i)*6)
    plt.figure(figsize=(10,10))
    #msg_con = image.ImageContainer(layerS[-i,:,:,2].T, grid_def)
    #result1 = msg_con.get_array_from_linesample(row_indices , col_indices )
    m.drawcoastlines()
    m.drawparallels(np.arange(-80.,81.,20.))
    m.drawmeridians(np.arange(-180.,181.,20.))
    xx,yy=area_def.get_lonlats()
  
    str_ct=ct.strftime('%Y-%m-%d %H:%M')
    i1=38-i
    if i%2==1:
        mLayer=tp[6+i1,:,:]-tp[6+i1-1,:,:]
    else:
        mLayer=tp[6+i1,:,:]
    print(mLayer.sum())
    mLayerm=ma.array(mLayer,mask=abs(1000*mLayer)<0.01)
    m.pcolormesh(x2,y2,-1000.*mLayer[1:-1,:],cmap='RdBu_r',
                 vmin=-10,vmax=10 )
    plt.title('ECMWF 6 hourly E-P\n'+str_ct)
    c=plt.colorbar()
    c.ax.set_title('mm')
    plt.savefig('eprecip%2.2i.png'%(40-i))
    cmd='convert eprecip%2.2i.png eprecip2_%2.2i.gif'%(40-i,40-i)
    os.system(cmd)
    if ifig==50:
        stop
    ifig+=1

    #plt.show()
    plt.close()
    
