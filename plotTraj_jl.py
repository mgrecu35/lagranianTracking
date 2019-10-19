from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap, cm
import numpy as np


f=Dataset('traj2b_d.4','r')

x=f['lon'][:,:,:]
y=f['lat'][:,:,:]
p=f['p'][:,:,:]
q=f['Q'][:,:,:]
rho=f['RHO'][:,:,:]

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
layerS=zeros((40,360,90,20),float)
ilayerS=zeros((40,360,90,20),float)

import julia
jl=julia.Julia()

jl.include("gridDQ.jl")
ind=a[0][b][c]
print(ind[0:3])
layerS,ilayerS=jl.gridDQ(ind,p,x,y,q,rho)
import pickle
a=nonzero(ilayerS>0)
layerS[a]/=ilayerS[a]
pickle.dump([layerS,ilayerS],open('layerS3.pklz','wb'))
