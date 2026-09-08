import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def roty(a):
    # Rotation matrix for rotation about Y axis (degrees)
    a = np.deg2rad(a)
    cosa = np.cos(a)
    sina = np.sin(a)
    return np.array([
        [cosa, 0, sina],
        [0, 1, 0],
        [-sina, 0, cosa]
    ])

def plot_landmarks(vertices, faces, idx):
    ax = plt.gca(projection='3d')
    # minimal patch plotting with trisurf equivalent
    tri_faces = faces
    ax.plot_trisurf(vertices[:,0], vertices[:,1], vertices[:,2], triangles=tri_faces, color='white', edgecolor='gray', linewidth=0.5, alpha=0.7)
    ax.scatter(vertices[idx,0], vertices[idx,1], vertices[idx,2], color='red', s=40)
    for i, (x,y,z) in enumerate(vertices[idx]):
        ax.text(x, y, z*2, str(i+1))
    ax.set_axis_off()
    # view handled by default

def test_landmarks_simple():
    """
    Tests simple 3D landmark plotting logic by generating random vertices/faces.
    """
    FV_vertices = np.random.rand(10,3)
    FV_faces = np.array([[0,1,2],[3,4,5],[6,7,8]])
    idx = np.array([0,2,4,6])
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    for i, rot in enumerate([-30, 0, 30]):
        ax = fig.add_subplot(1,3,i+1, projection='3d')
        V = FV_vertices @ roty(rot).T
        plot_landmarks(V, FV_faces, idx)
    plt.close(fig)