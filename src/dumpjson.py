# %%
import json
import numpy as np
from scipy.spatial.transform import Rotation as R


# %%

def cg_to_json(cg_output):
    """
    Converts the correspondence grouping output to euler angles.

    :param cg_output: string output of the correspondence grouping code
    :returns json string: string of the euler angles
    """

    obj = {}
    idx = 0
    lastidx = 0
    for ltr in cg_output:
        idx += 1
        if ltr == ";":
            sub = cg_output[lastidx:idx]
            a, b, c, = str.partition(sub, "=")
            lastidx = idx
            obj[a] = c[:-1].replace(" ", "")


            if(a == "rotation"):
                #print(c[:-1])
                rotmatrix = np.fromstring(c[:-1], sep=',').reshape(3,3)
                quaternion = R.from_rotvec(rotmatrix)
                diags = np.diag(quaternion.as_euler('xyz'))
                print(diags)
                obj[a] = diags.tolist()
                obj["x_rot"] = obj[a][0]
                obj["y_rot"] = obj[a][1]
                obj["z_rot"] = obj[a][2]

            if (a == "translation"):
                obj[a] = np.fromstring(c[:-1], sep=',').tolist()
                obj["x"] = np.fromstring(c[:-1], sep=',').tolist()[0]
                obj["y"] = np.fromstring(c[:-1], sep=',').tolist()[1]
                obj["z"] = np.fromstring(c[:-1], sep=',').tolist()[2]

    return json.dumps(obj)

# %%
# cg_to_json("success=true;rotation= 1.000,-0.000, 0.000, 0.000, 1.000, 0.000, 0.000, 0.000, 1.000;translation=0.000, 0.000, 0.000;")

# %%
