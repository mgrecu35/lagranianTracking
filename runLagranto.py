import os
os.environ['LAGRANTO']='/home/grecu/lagranto/lagranto.ecmwf'
os.environ['LD_LIBRARY_PATH']='/home/grecu/netcdf3/lib'

cmd='../bin/create_startf 20151202_12 startf_20151202_12 "region.eqd(2,30) @ profile(100,800,15) @hPa,agl"'
os.system(cmd)
cmd='../bin/caltra 20151202_12 20151122_12 startf_20151202_12 traj2b.4   -o 360 -j'
#os.system(cmd)
#cmd='../bin/trace traj2b.4 trajQ2.4 -f Q 1000. 0 P'
#os.system(cmd)

