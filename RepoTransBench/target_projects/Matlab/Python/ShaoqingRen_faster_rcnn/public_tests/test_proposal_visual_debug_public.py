import numpy as np
import pytest

def proposal_locate_anchors(conf, im_size, scale):
    return np.tile(np.array([1,1,3,3]), (2,1))

def fast_rcnn_bbox_transform_inv(rois, bbox_targets):
    return rois + bbox_targets + 0.5

def RectLTRB2LTWH(x):
    return [x[1], x[2], x[3]-x[1]+2, x[2]-x[0]+2]

def proposal_visual_debug(conf, image_roidb, input_blobs, bbox_means, bbox_stds, classes, scale_inds):
    # Stub, simulate logic, don't display or plot
    assert "anchors" in conf
    assert "scales" in conf
    assert "im_size" in image_roidb

def test_minimal_call_public():
    np.random.seed(11)
    conf = {"anchors": np.array([[5,5,10,10],[7,7,14,14]]), "scales": [3,4]}
    image_roidb = {"im_size": [48,35]}

    im_blob = np.zeros((48,35,3,1), dtype=np.uint8)
    labels_blob = np.ones((1,1,2), dtype=np.float32)
    label_weights_blob = 2*np.ones((1,1,2), dtype=np.float32)
    bbox_targets_blob = np.ones((4,1,2), dtype=np.float32)
    bbox_loss_weights_blob = np.ones((4,1,2), dtype=np.float32)
    input_blobs = [im_blob, labels_blob, label_weights_blob, bbox_targets_blob, bbox_loss_weights_blob]

    bbox_means = np.array([1,2,3,4])
    bbox_stds = np.array([2,2,2,2])
    classes = ['background','object']
    scale_inds = 2

    try:
        proposal_visual_debug(conf, image_roidb, input_blobs, bbox_means, bbox_stds, classes, scale_inds)
    except Exception as err:
        pytest.fail(f'proposal_visual_debug_public errored: {err}')