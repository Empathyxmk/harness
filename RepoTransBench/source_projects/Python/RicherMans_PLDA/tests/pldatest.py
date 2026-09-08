import unittest
import numpy as np
from liblda import PLDA

class TestPLDA(unittest.TestCase):
    def setUp(self):
        self.X = np.array([[1,2],[3,4],[5,6]])
        self.y = np.array([0,1,0])
        self.plda = PLDA()

    def test_fit(self):
        out = self.plda.fit(self.X, self.y)
        self.assertTrue(self.plda.trained)
        self.assertIs(out, self.plda)

    def test_predict(self):
        self.plda.fit(self.X, self.y)
        pred = self.plda.predict(self.X)
        self.assertTrue((pred == 0).all())

    def test_predict_without_fit(self):
        p = PLDA()
        with self.assertRaises(ValueError):
            p.predict(self.X)