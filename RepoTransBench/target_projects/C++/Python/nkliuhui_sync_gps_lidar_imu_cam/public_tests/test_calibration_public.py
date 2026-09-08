import os
import pytest
from src.velodyne_pointcloud.calibration import Calibration

def test_load_calibration_new_data(tmp_path):
    xml = '''
    <boost_serialization>
        <db:count>2</db:count>
        <item_version>0</item_version>
        <item>
            <id>0</id>
            <rotCorrection>-0.012</rotCorrection>
            <vertCorrection>0.99</vertCorrection>
            <distCorrection>2.22</distCorrection>
            <vertOffsetCorrection>0.890</vertOffsetCorrection>
            <horizOffsetCorrection>0.002</horizOffsetCorrection>
            <focalDistance>12.1</focalDistance>
            <focalSlope>0.21</focalSlope>
            <laserRing>0</laserRing>
        </item>
        <item>
            <id>1</id>
            <rotCorrection>0.017</rotCorrection>
            <vertCorrection>-1.02</vertCorrection>
            <distCorrection>1.99</distCorrection>
            <vertOffsetCorrection>0.951</vertOffsetCorrection>
            <horizOffsetCorrection>0.003</horizOffsetCorrection>
            <focalDistance>13.3</focalDistance>
            <focalSlope>0.23</focalSlope>
            <laserRing>1</laserRing>
        </item>
    </boost_serialization>
    '''
    xmlfile = tmp_path / "test_public_calib.xml"
    with open(xmlfile, "w") as outf:
        outf.write(xml)
    cal = Calibration()
    assert cal.read(str(xmlfile))
    assert cal.num_lasers() == 2
    assert abs(cal.laser_corrections_[0].rot_correction + 0.012) < 1e-6
    assert abs(cal.laser_corrections_[0].vert_correction - 0.99) < 1e-6
    assert abs(cal.laser_corrections_[1].focal_distance - 13.3) < 1e-6

def test_invalid_calibration_returns_false(tmp_path):
    xmlfile = tmp_path / "broken_public_calib.xml"
    with open(xmlfile, "w") as outf:
        outf.write("<not a valid xml>")
    cal = Calibration()
    assert not cal.read(str(xmlfile))