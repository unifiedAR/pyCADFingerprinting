#%%
import json
import numpy as np
from scipy.spatial.transform import Rotation as R


#%%

item = "success=true;rotation= 1.000,-0.000, 0.000, 0.000, 1.000, 0.000, 0.000, 0.000, 1.000;translation=0.000, 0.000, 0.000;"
obj = {}
#obj['success'] = 
item.find("success")


idx = 0
lastidx = 0
for ltr in item:
    idx+=1
    if ltr == ";":
        sub = item[lastidx:idx]
        a,b,c, = str.partition(sub, "=")
        lastidx = idx
        print(a,c[:-1])
        obj[a] = c[:-1].replace(" ", "")


        if(a == "rotation"):
            rotmatrix = np.fromstring(c[:-1], sep=',').reshape(3,3)
            quaternion = R.from_rotvec(rotmatrix).as_quat()
           # print(quaternion)
            obj[a] = quaternion.tolist()

        if(a == "translation"):
            obj[a] = np.fromstring(c[:-1], sep=',').tolist()

js = print(json.dumps(obj))







#%%
