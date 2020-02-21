from numpy import *
dat=loadtxt('ncepstorms_2016.txt')
jday=dat[:,0]
lat=dat[:,-7]
lon=dat[:,-6]
recn=dat[:,1]
press=dat[:,-11]
a=nonzero(jday<58)
jday=jday[a]
lat=lat[a]
lon=lon[a]
recn=recn[a]

lon[lon>180]-=360

a1=nonzero(abs(lon+30)<30)
press=press[a]

lStorms=[]
for i in a1[0]:
    if recn[i] not in lStorms:
        lStorms.append(recn[i])
        a=nonzero(recn==recn[i])
        b=nonzero(abs(lat[a]-60)<10)
        #print(press[a][b].min())
        ind=argmin(press[a][b])
        st_fmt='%6.2f %8.3f %6.2f %6.2f'%(jday[a][b][ind],lon[a][b][ind],lat[a][b][ind],press[a][b][ind])
        if abs(lon[a][b][ind]+30)<30:
            print(st_fmt)
        #print(lon[a][b])
        #print(lat[a][b])
        #print(recn[a][b])
        #print(lat[a][b])
        #print(jday[i])
