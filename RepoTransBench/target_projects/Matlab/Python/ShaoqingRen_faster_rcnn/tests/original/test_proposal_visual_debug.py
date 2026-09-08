import numpy as np
import pytest

def proposal_locate_anchors(conf, im_size, scale):
    # Stub: returns 2 anchors
    return np.tile(np.array([0,0,1,1]), (2,1))

def fast_rcnn_bbox_transform_inv(rois, bbox_targets):
    return rois + bbox_targets

def RectLTRB2LTWH(x):
    return [x[0], x[1], x[2]-x[0]+1, x[3]-x[1]+1]

def proposal_visual_debug(conf, image_roidb, input_blobs, bbox_means, bbox_stds, classes, scale_inds):
    # Stub: simulate main logic, do not display
    assert "anchors" in conf
    assert "scales" in conf
    assert "im_size" in image_roidb
    # No exception thrown = pass

def test_minimal_call():
    np.random.seed(1)
    conf = {"anchors": np.array([[0, 0, 1, 1], [0, 0, 2, 2]]), "scales": [1,2]}
    image_roidb = {"im_size": [32,32]}

    im_blob = np.zeros((32,32,3,1), dtype=np.uint8)
    labels_blob = np.zeros((1,1,2), dtype=np.float32)
    label_weights_blob = np.ones((1,1,2), dtype=np.float32)
    bbox_targets_blob = np.zeros((4,1,2), dtype=np.float32)
    bbox_loss_weights_blob = np.zeros((4,1,2), dtype=np.float32)
    input_blobs = [im_blob, labels_blob, label_weights_blob, bbox_targets_blob, bbox_loss_weights_blob]

    bbox_means = np.zeros((4,))
    bbox_stds = np.ones((4,))
    classes = ['bg','fg']
    scale_inds = 1

    try:
        proposal_visual_debug(conf, image_roidb, input_blobs, bbox_means, bbox_stds, classes, scale_inds)
    except Exception as err:
        pytest.fail(f'proposal_visual_debug errored: {err}')