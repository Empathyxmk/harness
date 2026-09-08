import unittest
import numpy as np

from liblda import LDA

class TestPublicLDA(unittest.TestCase):
    def setUp(self):
        self.X = np.array([[3, 8, 1], [6, 2, 7], [5, 4, 0], [9, 1, 2]])
        self.y = np.array([2, 2, 1, 1])
        self.lda = LDA(n_components=2)

    def test_fit_public(self):
        model = self.lda.fit(self.X, self.y)
        self.assertIsInstance(model, LDA)
        # Test another property: the model[0][0] is n_samples
        self.assertEqual(self.lda.model[0][0], 4)

    def test_transform_public(self):
        self.lda.fit(self.X, self.y)
        X_new = self.lda.transform(self.X)
        self.assertEqual(X_new.shape[1], 2)

    def test_fit_transform_public(self):
        X_new = self.lda.fit_transform(self.X, self.y)
        self.assertEqual(X_new.shape[1], 2)

    def test_transform_n_components_none_public(self):
        lda2 = LDA(n_components=None)
        lda2.fit(self.X, self.y)
        X_new = lda2.transform(self.X)
        self.assertEqual(X_new.shape, self.X.shape)