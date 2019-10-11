function getPress(am,bm,ai,bi,ps)
    P=zeros(60,241,480)
    Pi=zeros(61,241,480)
    for i=1:241
        for j=1:480
            P[:,i,j]=am/100+bm*ps[i,j]
            Pi[:,i,j]=ai/100+bi*ps[i,j]
        end
    end
    return P,Pi
end
