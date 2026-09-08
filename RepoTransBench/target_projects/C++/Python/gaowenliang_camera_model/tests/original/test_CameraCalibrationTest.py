import pytest
import numpy as np

class DummyCamera:
    """
    A minimal mock camera class to simulate relevant interface for calibration testing.
    """
    def __init__(self):
        self.name = "DummyCamera"
        self.intrinsic_params = np.eye(3)
        self.parameters = np.ones(5)
    
    def cameraName(self):
        return self.name
    
    def parametersToString(self):
        # Simulates the string representation of parameters for debugging
        return f"Parameters: {self.parameters}"
    
    def estimateExtrinsics(self, scene_points, image_points, rvec, tvec):
        # Assign trivial extrinsics
        rvec[:] = np.zeros(3)
        tvec[:] = np.zeros(3)
    
    def projectPoints(self, scene_points, rvec, tvec, out_points):
        # Simple orthographic projection for test dummy
        out_points.clear()
        for pt in scene_points:
            # Just drop the Z and "project" for test logic purposes
            out_points.append(np.array([pt[0], pt[1]], dtype=float))
    
    def estimateIntrinsics(self, board_size, scene_points, image_points):
        # NOP for dummy
        pass

    def reprojectionRMSError(self, scene_points, image_points, rvecs, tvecs):
        return 0.0

def generate_chessboard_corners(board_size, square_size):
    """
    Generate chessboard world points (scene points), as a list of (x, y, z) for a given board
    """
    return [[float(i) * square_size, float(j) * square_size, 0.0]
            for i in range(board_size[1]) for j in range(board_size[0])]

@pytest.mark.original
def test_addChessboardData_and_scene_points():
    # Simulate addChessboardData logic: push back corners and generate correct scene points
    board_size = (8, 6)  # (width, height)
    square_size = 25.0
    # Simulate observed corners: dummy as grid for test
    corners = [np.array([float(i), float(j)], dtype=float)
               for i in range(board_size[0]) for j in range(board_size[1])]
    # Class under test
    class CameraCalibrationTestDummy:
        def __init__(self, board_size, square_size):
            self.m_boardSize = board_size
            self.m_squareSize = square_size
            self.m_imagePoints = []
            self.m_scenePoints = []
        def addChessboardData(self, corners):
            self.m_imagePoints.append(corners)
            scene = []
            for i in range(self.m_boardSize[1]):
                for j in range(self.m_boardSize[0]):
                    scene.append(np.array([i * self.m_squareSize, j * self.m_squareSize, 0.0]))
            self.m_scenePoints.append(scene)
    cc = CameraCalibrationTestDummy(board_size, square_size)
    cc.addChessboardData(corners)
    assert len(cc.m_imagePoints) == 1
    assert len(cc.m_scenePoints) == 1
    # The scene points generation order matches test logic
    scene = cc.m_scenePoints[0]
    expected_scene = generate_chessboard_corners(board_size, square_size)
    assert len(scene) == len(expected_scene)
    for s1, s2 in zip(scene, expected_scene):
        assert np.allclose(s1, s2)

@pytest.mark.original
def test_camera_calibration_workflow_smoke():
    """
    This will cover methods and workflow of 'calibrate' logic and matrix builds.
    We use dummies for images and chessboards, we're not running true computer vision.
    """
    # Board and data setup
    board_size = (8, 6)  # cols (width), rows (height)
    square_size = 25.0
    dummy_camera = DummyCamera()
    m_imagePoints = []
    m_scenePoints = []
    n_images = 2
    for img_i in range(n_images):
        # Simulate a chessboard in order for corners
        corners2d = [np.array([float(i), float(j)], dtype=float)
                     for i in range(board_size[0]) for j in range(board_size[1])]
        corners3d = [[float(i) * square_size, float(j) * square_size, 0.0]
                     for i in range(board_size[1]) for j in range(board_size[0])]
        m_imagePoints.append(corners2d)
        m_scenePoints.append(corners3d)
    # Workspace for extrinsics (rotational and translational vectors)
    rvecs = [np.zeros(3, dtype=float) for _ in range(n_images)]
    tvecs = [np.zeros(3, dtype=float) for _ in range(n_images)]

    # STEP 1: Estimate intrinsics and print parameters (dummy)
    # (In true C++/OpenCV: camera->estimateIntrinsics(boardSize, scenePoints, imagePoints))
    # Printout/logic dummy
    intr_message = f"[{dummy_camera.cameraName()}] # INFO: Initialization intrinsic parameters\n" \
                   f"# INFO: {dummy_camera.parametersToString()}\n-----------------------------------------------"
    assert "Parameters" in intr_message

    # STEP 2: Estimate extrinsics for each image
    for i in range(n_images):
        dummy_camera.estimateExtrinsics(m_scenePoints[i], m_imagePoints[i], rvecs[i], tvecs[i])
        # All should remain zeros for dummy
        assert np.allclose(rvecs[i], 0)
        assert np.allclose(tvecs[i], 0)

    # Simulate STEP 3: Optimization (N/A for dummy) and error stats
    # Dummy error accumulation
    errCount = 0
    numOfInlinerPoints = 0
    numOfOutlinerPoints = 0
    errSum = np.zeros(2)
    # Calculate errors as (obs - est), with dummy camera projecting perfectly
    for img_idx in range(n_images):
        obs = m_imagePoints[img_idx]
        scene = m_scenePoints[img_idx]
        estImagePoints = []
        dummy_camera.projectPoints(scene, rvecs[img_idx], tvecs[img_idx], estImagePoints)
        # Should reproduce the world points in dummy
        for obs_pt, est_pt in zip(obs, estImagePoints):
            err = obs_pt - est_pt
            assert np.allclose(err, 0)
            errSum += err
            # If error < 1.5, count as inlier
            if np.dot(err, err) < 1.5:
                numOfInlinerPoints += 1
            else:
                numOfOutlinerPoints += 1
            errCount += 1
    # All points should be inliers
    assert numOfInlinerPoints == len(m_imagePoints[0]) * n_images
    assert errCount == len(m_imagePoints[0]) * n_images
    # "Measurement covariance" is always zero here
    measurementCovariance = np.zeros((2,2))
    errMean = errSum / errCount
    for img_idx in range(n_images):
        obs = m_imagePoints[img_idx]
        scene = m_scenePoints[img_idx]
        estImagePoints = []
        dummy_camera.projectPoints(scene, rvecs[img_idx], tvecs[img_idx], estImagePoints)
        for obs_pt, est_pt in zip(obs, estImagePoints):
            d0 = (obs_pt[0] - est_pt[0]) - errMean[0]
            d1 = (obs_pt[1] - est_pt[1]) - errMean[1]
            measurementCovariance[0,0] += d0*d0
            measurementCovariance[0,1] += d0*d1
            measurementCovariance[1,1] += d1*d1
    measurementCovariance[1,0] = measurementCovariance[0,1]
    measurementCovariance /= errCount
    # Should be zero
    assert np.allclose(measurementCovariance, 0)

@pytest.mark.original
def test_reprojection_error_dummy():
    # Simulate the reprojectionError logic with dummy camera
    n_images = 2
    board_size = (8, 6)
    square_size = 25.0
    dummy_camera = DummyCamera()
    rvecs = [np.zeros(3) for _ in range(n_images)]
    tvecs = [np.zeros(3) for _ in range(n_images)]
    m_imagePoints = []
    m_scenePoints = []
    for img_i in range(n_images):
        corners2d = [np.array([float(i), float(j)], dtype=float)
                     for i in range(board_size[0]) for j in range(board_size[1])]
        corners3d = [[float(i) * square_size, float(j) * square_size, 0.0]
                     for i in range(board_size[1]) for j in range(board_size[0])]
        m_imagePoints.append(corners2d)
        m_scenePoints.append(corners3d)
    total_err = 0.0
    total_points = 0
    for i in range(n_images):
        estImagePoints = []
        dummy_camera.projectPoints(m_scenePoints[i], rvecs[i], tvecs[i], estImagePoints)
        err = 0.0
        for obs_pt, est_pt in zip(m_imagePoints[i], estImagePoints):
            err += np.linalg.norm(obs_pt - est_pt)
        total_points += len(m_imagePoints[i])
        # all errors should be exactly zero with dummy
        assert err == 0.0
        total_err += err
    avg_err = total_err / total_points
    assert avg_err == 0.0