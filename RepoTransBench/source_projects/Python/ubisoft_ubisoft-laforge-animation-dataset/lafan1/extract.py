import numpy as np

def pad_and_concat(arrays, axis=0):
    # Pad a list of ndarrays so they have the same shape along all axes except the concat axis
    arr_shapes = [arr.shape for arr in arrays]
    max_shape = np.max(np.array(arr_shapes), axis=0)
    out = []
    for arr in arrays:
        pad_width = []
        for i, dim in enumerate(arr.shape):
            if i == axis:
                pad_width.append((0,0))
            else:
                pad_width.append((0, max_shape[i] - arr.shape[i]))
        while len(pad_width) < len(max_shape):
            pad_width.append((0, max_shape[len(pad_width)]))
        arr_padded = np.pad(arr, pad_width, mode='constant')
        out.append(arr_padded)
    return np.concatenate(out, axis=axis)

def flatten_dict(d):
    keys = list(d.keys())
    vals = [d[k] for k in keys]
    return keys, vals

def shape(arr):
    return arr.shape

def parse_bvh(lines):
    # Very basic and lenient parser for test/demo
    hierarchy = []
    motion = []
    channels = []
    in_hierarchy = False
    in_motion = False
    for idx, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        if line.startswith("HIERARCHY"):
            in_hierarchy = True
        elif line.startswith("MOTION"):
            in_hierarchy = False
            in_motion = True
        elif in_hierarchy:
            hierarchy.append(line)
            if "CHANNELS" in line:
                channels.extend(line.split()[2:])
        elif in_motion:
            if line.startswith("Frames:") or line.startswith("Frame Time:"):
                continue
            else:
                # Parse motion values for one frame
                motion.append([float(x) for x in line.strip().split()])
    if not hierarchy or not channels:
        raise Exception("Malformed BVH: missing hierarchy/channels")
    return {"hierarchy": hierarchy, "channels": channels, "motion": motion}