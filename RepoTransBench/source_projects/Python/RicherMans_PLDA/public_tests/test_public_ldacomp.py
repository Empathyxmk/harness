import unittest
import numpy as np
from liblda import LDA

class TestPublicLDAComp(unittest.TestCase):
    def setUp(self):
        self.X = np.array([[2,6,4],[1,5,8],[4,2,9]])
        self.y = np.array([1,0,0])

    def test_lda_fit_and_transform_public(self):
        lda = LDA(n_components=2)
        lda.fit(self.X, self.y)
        X_trans = lda.transform(self.X)
        self.assertEqual(X_trans.shape, (3,2))