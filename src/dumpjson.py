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

            if (a == "rotation"):
                print(c[:-1])
                rotmatrix = np.fromstring(c[:-1], sep=',').reshape(3, 3)
                quaternion = R.from_rotvec(rotmatrix).as_euler('xyz')
                # print(quaternion)
                obj[a] = quaternion.tolist()

            if (a == "translation"):
                obj[a] = np.fromstring(c[:-1], sep=',').tolist()

    return json.dumps(obj)

# %%
# cg_to_json("success=true;rotation= 1.000,-0.000, 0.000, 0.000, 1.000, 0.000, 0.000, 0.000, 1.000;translation=0.000, 0.000, 0.000;")

# %%
