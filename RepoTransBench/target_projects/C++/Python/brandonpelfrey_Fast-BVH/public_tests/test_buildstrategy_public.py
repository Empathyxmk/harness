import math
from fastbvh.vector3 import Vector3
from fastbvh.bbox import BBox
from fastbvh.build_strategy import BuildStrategy

class DummyPrimPublic:
    def __init__(self, c):
        self.centroid = Vector3(c.x, c.y, c.z)
        self.bounds = BBox()
        self.bounds.min = self.centroid - Vector3(0.1, 0.1, 0.1)
        self.bounds.max = self.centroid + Vector3(0.1, 0.1, 0.1)

    def Bound(self):
        return self.bounds

    def Centroid(self):
        return self.centroid

def test_BuildStrategyPublic_BBoxReducePublic():
    prims = [
        DummyPrimPublic(Vector3(5.5, 2.6, -7.1)),
        DummyPrimPublic(Vector3(6.0, 2.8, -8.5)),
        DummyPrimPublic(Vector3(4.4, 2.3, -6.3)),
    ]
    bbox = BuildStrategy.BBoxReduce(prims)
    assert bbox.min.x <= 4.3
    assert bbox.max.x >= 6.1
    assert bbox.min.y <= 2.2
    assert bbox.max.y >= 2.9
    assert bbox.min.z <= -8.6
    assert bbox.max.z >= -6.2

def test_BuildStrategyPublic_GetCentroidBBoxPublic():
    prims = [
        DummyPrimPublic(Vector3(4.0, 3.0, 2.0)),
        DummyPrimPublic(Vector3(7.0, 5.0, 2.5)),
        DummyPrimPublic(Vector3(3.0, 2.0, 4.4)),
    ]
    bbox = BuildStrategy.GetCentroidBBox(prims)
    assert math.isclose(bbox.min.x, 3.0)
    assert math.isclose(bbox.max.x, 7.0)
    assert math.isclose(bbox.min.y, 2.0)
    assert math.isclose(bbox.max.y, 5.0)
    assert math.isclose(bbox.min.z, 2.0)
    assert math.isclose(bbox.max.z, 4.4)

def test_BuildStrategyPublic_SAHBinPublic():
    bin = BuildStrategy.SAHBin()
    bin.count = 4
    bin.bbox.min = Vector3(12.4, 0, 0)
    bin.bbox.max = Vector3(13.5, -6.7, 1.1)
    bin.bbox.min.y = -8.7
    bin.bbox.min.z = 0.1
    bin.bbox.max.z = 1.1

    assert bin.count == 4
    assert math.isclose(bin.bbox.min.x, 12.4)
    assert math.isclose(bin.bbox.max.y, -6.7)
    assert math.isclose(bin.bbox.min.z, 0.1)
    assert math.isclose(bin.bbox.max.z, 1.1)