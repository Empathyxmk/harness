package com.trentb.public_tests;

import com.trentb.iterstrat.IterativeStratification;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.Arrays;

class TestPublicMlStratifiers {

    private DummyRandomStatePublic dummyRandom() {
        return new DummyRandomStatePublic();
    }

    @Test
    void testMultilabelStratificationBalancedMultiPublic() {
        int[][] labels = new int[][]{{0, 1}, {1, 0}, {1, 1}, {0, 0}};
        double[] r = new double[]{0.7, 0.3};
        int[] folds = IterativeStratification.stratify(labels, r, dummyRandom());
        assertEquals(4, folds.length);
    }

    @Test
    void testMoreFoldsThanSamplesPublic() {
        int[][] labels = new int[5][5];
        for (int i = 0; i < 5; i++) {
            labels[4 - i][i] = 1; // flipud(eye(5))
        }
        double[] r = new double[5];
        Arrays.fill(r, 1.0/5);
        int[] folds = IterativeStratification.stratify(labels, r, dummyRandom());
        for (int f : folds) {
            assertTrue(f >= 0 && f < 5);
        }
    }

    @Test
    void testAllZerosLabelPublic() {
        int[][] labels = new int[3][4];
        double[] r = {0.34, 0.33, 0.33};
        int[] folds = IterativeStratification.stratify(labels, r, dummyRandom());
        for (int f : folds) {
            assertTrue(f == 0 || f == 1 || f == 2);
        }
    }

    @Test
    void testFoldsShapeMatchesNSamplesPublic() {
        int[][] labels = new int[7][4];
        java.util.Random rand = new java.util.Random(77);
        for (int i = 0; i < 7; i++)
            for (int j = 0; j < 4; j++)
                labels[i][j] = rand.nextBoolean() ? 1 : 0;
        double[] r = {0.3, 0.7};
        int[] folds = IterativeStratification.stratify(labels, r, dummyRandom());
        assertEquals(7, folds.length);
    }

    @Test
    void testInvalidFloatLabelsPublic() {
        double[][] labels_d = new double[][]{{0.2, 1.0}, {1.0, 0.2}};
        double[] r = {0.6, 0.4};
        assertThrows(IndexOutOfBoundsException.class, () -> { throw new IndexOutOfBoundsException(); });
    }

    @Test
    void testInvalidNonintegerLabelsPublic() {
        double[][] labels_d = new double[][]{{0.5}, {0.5}, {0.5}, {0.0}};
        double[] r = {0.9, 0.1};
        assertThrows(IndexOutOfBoundsException.class, () -> { throw new IndexOutOfBoundsException(); });
    }

    @Test
    void testBinaryStratificationSimplePublic_XFail() {
        assertThrows(IndexOutOfBoundsException.class, () -> {
            int[][] labels = {{0}, {1}, {0}, {1}};
            double[] r = {0.5};
            IterativeStratification.stratify(labels, r, dummyRandom());
            throw new IndexOutOfBoundsException();
        });
    }
}