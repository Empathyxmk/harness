import numpy as np

def quat_inv_unit(q):
    q = np.asarray(q)
    if q.shape[-1] != 4:
        raise ValueError("Quaternions must have 4 components.")
    inv = q.copy()
    inv[..., 1:] *= -1
    # assume unit quaternion; otherwise, should divide by norm squared
    return inv

def quat_mult_unit(q1, q2):
    q1 = np.asarray(q1)
    q2 = np.asarray(q2)
    # Only accept last dimension = 4
    if q1.shape[-1] != 4 or q2.shape[-1] != 4:
        raise ValueError("Quaternion multiplication requires arrays of shape (...,4)")

    # Supports both shape (4,) and (...,4)
    if q1.ndim == 1 and q2.ndim == 1:
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2
        return np.array([
            w1*w2 - x1*x2 - y1*y2 - z1*z2,
            w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2,
            w1*z2 + x1*y2 - y1*x2 + z1*w2
        ])
    else:
        # Now supports shape (...,4)
        w1,x1,y1,z1 = np.split(q1, 4, axis=-1)
        w2,x2,y2,z2 = np.split(q2, 4, axis=-1)
        ww = w1*w2 - x1*x2 - y1*y2 - z1*z2
        xx = w1*x2 + x1*w2 + y1*z2 - z1*y2
        yy = w1*y2 - x1*z2 + y1*w2 + z1*x2
        zz = w1*z2 + x1*y2 - y1*x2 + z1*w2
        out = np.concatenate([ww, xx, yy, zz], axis=-1)
        return np.squeeze(out, axis=-2) if out.ndim > 1 and out.shape[-2]==1 else out # Safe squeeze

def quat_fk(lrot, lpos, parents):
    lrot = np.asarray(lrot)
    lpos = np.asarray(lpos)
    if lrot.shape[:-1] != lpos.shape[:-1]:
        raise ValueError("Shape mismatch between lrot and lpos")
    if lrot.shape[-2] != len(parents):
        raise ValueError("Parents length differs from num joints")
    n_batch = lrot.shape[:-2]
    n_frames = lrot.shape[-3] if len(lrot.shape) > 2 else 1
    njoints = lrot.shape[-2]
    gpos = np.zeros(lpos.shape)
    grot = np.zeros(lrot.shape)
    for j in range(njoints):
        if parents[j] == -1:
            grot[...,j,:] = lrot[...,j,:]
            gpos[...,j,:] = lpos[...,j,:]
        else:
            grot[...,j,:] = quat_mult_unit(grot[...,parents[j],:], lrot[...,j,:])
            gpos[...,j,:] = gpos[...,parents[j],:] + lpos[...,j,:]
    return grot, gpos