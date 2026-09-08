import unittest

from greedypacker import skyline
from greedypacker import item

class PublicSkylineMethods(unittest.TestCase):
    def setUp(self):
        self.S = skyline.Skyline(10, 6, heuristic='best_fit')

    def tearDown(self):
        del self.S

    def test_clip_segment_full_overlap(self):
        I = item.Item(5, 2, CornerPoint=[0, 0])
        S = skyline.SkylineSegment(0, 0, 5)
        res = self.S._clip_segment(S, I)
        self.assertEqual(res, [])

    def test_clip_segment_extends_left(self):
        I = item.Item(3, 1, CornerPoint=[4, 0])
        S = skyline.SkylineSegment(0, 0, 6)
        res = self.S._clip_segment(S, I)
        self.assertEqual(res, [skyline.SkylineSegment(0, 0, 4)])

    def test_clip_segment_extends_right(self):
        I = item.Item(3, 2, CornerPoint=[0, 0])
        S = skyline.SkylineSegment(3, 0, 5)
        res = self.S._clip_segment(S, I)
        self.assertEqual(res, [skyline.SkylineSegment(3, 0, 2)])

    def test_clip_segment_extends_both(self):
        I = item.Item(2, 1, CornerPoint=[3, 0])
        S = skyline.SkylineSegment(0, 0, 8)
        res = self.S._clip_segment(S, I)
        self.assertCountEqual(
            res,
            [skyline.SkylineSegment(0, 0, 3), skyline.SkylineSegment(5, 0, 3)]
        )

    def test_update_segment(self):
        I = item.Item(3, 3, CornerPoint=[0, 0])
        S1 = skyline.SkylineSegment(0, 3, 3)
        S2 = skyline.SkylineSegment(3, 0, 7)
        res = self.S._update_segment(self.S.skyline[0], 0, I)
        self.assertCountEqual(res, [S1, S2])

    def test_merge_segments(self):
        S1 = skyline.SkylineSegment(0, 0, 3)
        S2 = skyline.SkylineSegment(3, 0, 7)
        S3 = skyline.SkylineSegment(0, 0, 10)
        self.S.skyline.pop()
        self.S.skyline.update([S1, S2])
        self.S._merge_segments()
        self.assertEqual(self.S.skyline, [S3])

    def test_merge_three_segments(self):
        S1 = skyline.SkylineSegment(0, 0, 2)
        S2 = skyline.SkylineSegment(2, 0, 3)
        S3 = skyline.SkylineSegment(5, 0, 5)
        S4 = skyline.SkylineSegment(0, 0, 10)
        self.S.skyline.pop()
        self.S.skyline.update([S1, S2, S3])
        self.S._merge_segments()
        self.assertEqual(self.S.skyline, [S4])

    def test_check_fit_true(self):
        I = item.Item(4, 2, CornerPoint=[0, 0])
        S1 = skyline.SkylineSegment(0, 1, 4)
        S2 = skyline.SkylineSegment(4, 0, 6)
        self.S.skyline.pop()
        self.S.skyline.update([S1, S2])
        self.assertEqual(self.S._check_fit(I.width, I.height, 0), (True, 1))

    def test_check_fit_false(self):
        I = item.Item(3, 4, CornerPoint=[0, 0])
        S1 = skyline.SkylineSegment(0, 0, 2)
        S2 = skyline.SkylineSegment(2, 5, 8)
        self.S.skyline.pop()
        self.S.skyline.update([S1, S2])
        self.assertEqual(self.S._check_fit(I.width, I.height, 1), (False, None))

    def test_calc_waste(self):
        I0 = item.Item(3, 2)
        I1 = item.Item(1, 3)
        I2 = item.Item(5, 4)
        I3 = item.Item(2, 3)
        I4 = item.Item(6, 2)
        self.S.insert(I0, 'bottom_left')
        self.S.insert(I1, 'bottom_left')
        self.S.insert(I2, 'bottom_left')
        self.S.insert(I3, 'bottom_left')
        wasted_area = skyline.calc_waste(self.S.skyline, I4, 5, 0)
        self.assertEqual(wasted_area, 2)

    def test_calc_waste2(self):
        I0 = item.Item(4, 3)
        I1 = item.Item(2, 2)
        I2 = item.Item(3, 4)
        I3 = item.Item(3, 2)
        self.S.insert(I0)
        self.S.insert(I1)
        self.S.insert(I2)
        wasted_area = skyline.calc_waste(self.S.skyline, I3, 3, 0)
        self.assertEqual(wasted_area, 0)

class PublicBottomLeft(unittest.TestCase):
    def setUp(self):
        self.S = skyline.Skyline(10, 6, heuristic='bottom_left')

    def tearDown(self):
        del self.S

    def test_one_item_insert(self):
        I = item.Item(4, 3)
        self.S.insert(I)
        S1 = skyline.SkylineSegment(0, 3, 4)
        S2 = skyline.SkylineSegment(4, 0, 6)
        self.assertCountEqual(self.S.skyline, [S1, S2])