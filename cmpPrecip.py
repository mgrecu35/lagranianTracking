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
tp=fe['tp'][:,:,:]#+fe['e'][:,:,:]
x=fe['longitude'][:]
y=fe['latitude'][:]

lonsE,latsE=np.meshgrid(x,y[1:-1])
tp2=tp[6+1:46+1:2,:,:].sum(axis=0)

m.drawcoastlines()
m.drawparallels(np.arange(-80.,81.,20.))
m.drawmeridians(np.arange(-180.,181.,20.))
xx,yy=area_def.get_lonlats()
x2,y2=m(lonsE,latsE)
str_ct=st.strftime('%Y-%m-%d %H:%M')
tpm=ma.array(tp2,mask=1000*tp2<0.01)
m.pcolormesh(x2,y2,tpm[1:-1,:]*1000.,cmap='jet',
             vmin=0,vmax=100)
plt.title('ERA-I Precipitation \nNov 22 to Dec 02')
c=plt.colorbar()
c.ax.set_title('mm')
plt.savefig('ERAINov22_Dec02.png')
f=Dataset('imergNov22_Dec02_075.nc','r')
imerg=f['imergPrecip'][0:160,:,:]
tp2=imerg.sum(axis=0)[:,:]*6
plt.figure()
m.drawcoastlines()
m.drawparallels(np.arange(-80.,81.,20.))
m.drawmeridians(np.arange(-180.,181.,20.))
xI=-180+arange(480)*0.75+0.75/2
yI=-90+arange(240)*0.75+0.75/2
lonsE1,latsE1=np.meshgrid(xI,yI)
x21,y21=m(lonsE1,latsE1)
str_ct=st.strftime('%Y-%m-%d %H:%M')
tpm=ma.array(tp2,mask=tp2<0.1)
m.pcolormesh(x21,y21,tpm[:,:].T,cmap='jet',
             vmin=0,vmax=100)
plt.title('IMERG Precipitation \nNov 22 to Dec 02')
c=plt.colorbar()
c.ax.set_title('mm')
plt.savefig('IMERGNov22_Dec02.png')
rL1=[]
rL2=[]
yL=[]
for i in range(39):
    ilays=ilayerS[i,:,:,:].sum(axis=2)
    a=nonzero(ilays>5)
    for i1,j1 in zip(a[0],a[1]):
        x1=i1-179.5
        y1=j1#-89.5
        ix1=int((x1+180.-0.75/2.)/0.75)
        iy1=int((y1+90-0.75/2.)/0.75)
        x11=x1
        if x11<0:
            x11+=360
        ix2=int(x11/0.75)
        iy2=int((90-y1)/0.75)
        if imerg[i+2,ix1,iy1]>-10:
            rL1.append(6*imerg[i+2,ix1,iy1])
            if i%2==0:
                rL2.append(1000*tp[i+6,iy2,ix2])
            else:
                rL2.append(1000*tp[i+6,iy2,ix2]-1000*tp[i+5,iy2,ix2])
            yL.append(y1)
    if 1==-1:
        plt.figure()
        plt.subplot(211)
        imergm=ma.array(imerg[i+2,:,:],mask=imerg[i+2,:,:]<0)
        plt.pcolormesh(xI,yI,imergm.T,norm=matplotlib.colors.LogNorm(),\
                               cmap='jet',vmin=0.1,vmax=2)
        plt.xlim(-50,50)
        plt.ylim(20,60)
        plt.colorbar()
        plt.subplot(212)
        if i%2==0:
            etp=tp[i+6,:,:]
        else:
            etp=tp[i+6,:,:]-tp[i+5,:,:]
        etpm=ma.array(etp,mask=etp[:,:]<0)
        xroll=roll(x,240)
        xroll[xroll>=180]-=360.
        plt.pcolormesh(xroll,y,1000/6.*roll(etpm,240),norm=matplotlib.colors.LogNorm(),
                       cmap='jet',vmin=0.1,vmax=2)
        plt.xlim(-50,50)
        plt.ylim(20,60)
        plt.colorbar()
        retmp=roll(etpm,240)
        a=nonzero(imerg[i+2,:,:]>-1)
        print(corrcoef(imerg[i+2,:,:][a],retmp[:-1,:][::-1,:].T[a]))
        
yL=array(yL)
rL1=array(rL1)
rL2=array(rL2)
rL=[]
for i in range(10,80):
    a=nonzero(yL==i)
    rL.append([rL1[a].mean(),rL2[a].mean()])

rL=array(rL)
plt.figure()

plt.plot(arange(10,80),rL[:,0])
plt.plot(arange(10,80),rL[:,1])
plt.title('Conditional precipitation')
plt.xlabel('Latitude')
plt.ylabel('mm/h')
plt.legend(['IMERG','ERA-I'])
plt.savefig('condPrec.png')
