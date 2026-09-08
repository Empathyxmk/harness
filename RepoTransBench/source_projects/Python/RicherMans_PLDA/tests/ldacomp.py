import unittest
import numpy as np
from liblda import LDA

class TestLDAComp(unittest.TestCase):
    def setUp(self):
        self.X = np.array([[5,3,1],[8,5,2],[7,3,3]])
        self.y = np.array([0,1,1])

    def test_lda_fit_and_transform(self):
        lda = LDA(n_components=2)
        lda.fit(self.X, self.y)
        X_trans = lda.transform(self.X)
        self.assertEqual(X_trans.shape, (3,2))