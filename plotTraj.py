from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap, cm
import numpy as np


f=Dataset('traj2b.4','r')

x=f['lon'][:,:,:]
y=f['lat'][:,:,:]
p=f['p'][:,:,:]
q=f['Q'][:,:,:]
import glob
files=sorted(glob.glob("P2015*"))[0:42]
import sys
sys.path.append("/home/grecu/lagranto/lagranto.ecmwf/cdo")
#from getpress import getP
#qL,tL=getP(files[::-1])


import matplotlib.pyplot as plt
from numpy import *
a=nonzero(p[0,0,0,:]-p[1,0,0,:]<-30)
b=nonzero(p[4,0,0,:][a]>100)
c=nonzero(p[20,0,0,:][a][b]>100)

dqdt=zeros((40,20),float)
count=zeros((40,20),float)
for i in a[0][b][c]:
    for j in range(40):
        ip=int(((p[j:j+2,0,0,i]).mean()-50)/50.)
        if ip>=0 and ip<20:
            dqdt[j,ip]+=(q[j,0,0,i]-q[j+1,0,0,i])
            count[j,ip]+=1

a=nonzero(count>0)
dqdt[a]=dqdt[a]/count[a]
dqdtm=ma.array(dqdt,mask=abs(dqdt)<0.05)
matplotlib.rcParams.update({'font.size': 20})
plt.pcolormesh(-236+arange(40)*6,25+arange(20)*50,dqdtm[::-1,:].T,cmap='RdBu_r',\
               vmin=-1,vmax=1)
plt.ylim(975,400)
plt.xlabel('Hours')
plt.ylabel('Pressure (mPa)')
plt.title('6 Hourly delta Q (g/kg)')
plt.colorbar()
plt.savefig('composite_dqdt.png')


m = Basemap(projection='npstere',boundinglat=20,lon_0=0,resolution='l')
#for it in range(4):
plt.figure()
it=1
m.drawcountries()
m.drawcoastlines()
m.drawparallels(np.arange(-80.,81.,20.),labels=[True,False,False,False])
m.drawmeridians(np.arange(-180.,181.,20.),labels=[False,False,True,True])
plt.title('Backward trajectories - 2 December 2015',y=1.08)

for i in a[0][b][c][::4]:
    xt,yt=m(x[:50,0,0,i],y[:50,0,0,i])
    m.plot(xt,yt,'-',color='black',linewidth=0.25)

xi,yi=m(x[0,0,0,a[0][b][c]],y[0,0,0,a[0][b][c]])

m.scatter(xi,yi,s=5,color='red')
plt.tight_layout()
plt.savefig('backwardTrajs.png')

