import unittest
import numpy as np

from liblda import LDA

class TestLDA(unittest.TestCase):
    def setUp(self):
        self.X = np.array([[1,2,3],[4,5,6],[7,8,9],[2,3,4]])
        self.y = np.array([0,1,0,1])
        self.lda = LDA(n_components=2)

    def test_fit(self):
        model = self.lda.fit(self.X, self.y)
        self.assertIsInstance(model, LDA)
        self.assertEqual(self.lda.model[0][0], 4)  # n_samples

    def test_transform(self):
        self.lda.fit(self.X, self.y)
        X_new = self.lda.transform(self.X)
        self.assertEqual(X_new.shape[1], 2)

    def test_fit_transform(self):
        X_new = self.lda.fit_transform(self.X, self.y)
        self.assertEqual(X_new.shape[1], 2)

    def test_transform_n_components_none(self):
        lda2 = LDA(n_components=None)
        lda2.fit(self.X, self.y)
        X_new = lda2.transform(self.X)
        self.assertEqual(X_new.shape, self.X.shape)