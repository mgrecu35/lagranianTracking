using Statistics
function gridDQ(ind,p,x,y,q,rho)
    layerS=zeros(40,360,90,20)
    ilayerS=zeros(40,360,90,20)
    #print(ind)
    #return
    print(size(p))
    for i in ind
        for j=1:39
            i1=i+1
            dp=mean(p[j:j+1,1,1,i1].-50)/50.0
            ip=1+Int(trunc(dp))
            if (ip>0) & (ip<21)
                ix=Int(trunc(mean(x[j:j+1,1,1,i1])+180))+1
                jx=Int(trunc(mean(y[j:j+1,1,1,i1])))+1
                #println(ip,ix,jx)
                if (ix>0) & (ix<360) & (jx>0) & (jx<90)
                    layerS[j,ix,jx,ip]= layerS[j,ix,jx,ip]+(rho[j,1,1,i1]*q[j,1,1,i1]-
                                                            rho[j,1,1,i1]*q[j+1,1,1,i1])/rho[j,1,1,i1]
                    ilayerS[j,ix,jx,ip]=ilayerS[j,ix,jx,ip]+1
                end
            end
        end
    end
    return layerS,ilayerS
end
