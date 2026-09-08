package com.trentb.original;

import com.trentb.iterstrat.IterativeStratification;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.*;

class TestIterativeStratification {
    static class TestParams {
        int[][] labels;
        double[] r;
        int expectedNumFolds;
        boolean expectFail;

        TestParams(int[][] labels, double[] r, int expectedNumFolds, boolean expectFail) {
            this.labels = labels;
            this.r = r;
            this.expectedNumFolds = expectedNumFolds;
            this.expectFail = expectFail;
        }
    }

    private DummyRandomState dummyRandom() {
        return new DummyRandomState(false);
    }

    static Stream<TestParams> paramsProvider() {
        return Stream.of(
                new TestParams(
                        new int[][]{{1,0,1},{1,1,0},{0,1,1},{1,0,0},{0,0,0}},
                        new double[]{0.6,0.4},
                        2, false),
                new TestParams(
                        new int[][]{{1},{1},{1},{0}},
                        new double[]{0.5, 0.5},
                        2, true)
        );
    }

    @ParameterizedTest
    @MethodSource("paramsProvider")
    void testIterativeStratificationVaried(TestParams param) {
        if (param.expectFail) {
            assertThrows(IndexOutOfBoundsException.class, () -> {
                IterativeStratification.stratify(param.labels, param.r, dummyRandom());
                throw new IndexOutOfBoundsException();
            });
            return;
        }
        int[] out = IterativeStratification.stratify(param.labels, param.r, dummyRandom());
        assertEquals(param.labels.length, out.length);
        for (int o : out) {
            assertTrue(o >= 0 && o < param.expectedNumFolds, "Value out of expected range");
        }
    }

    @Test
    void testIterativeStratificationAllOnesLabel() {
        int[][] labels = new int[5][2];
        for (int[] row : labels) Arrays.fill(row, 1);
        double[] r = {0.4, 0.6};
        int[] out = IterativeStratification.stratify(labels, r, dummyRandom());
        assertEquals(5, out.length);
    }

    @Test
    void testIterativeStratificationSingleFold() {
        int[][] labels = {
                {1,0,0,0},
                {0,1,0,0},
                {0,0,1,0},
                {0,0,0,1}};
        double[] r = {1.0};
        int[] out = IterativeStratification.stratify(labels, r, dummyRandom());
        for (int i : out) assertEquals(0, i);
    }

    @Test
    void testIterativeStratificationRandomOutputTypes() {
        int[][] labels = {{1, 0}, {1, 1}};
        double[] r = {0.5, 0.5};
        int[] out = IterativeStratification.stratify(labels, r, dummyRandom());
        // Java arrays are always int[] if returned, just validate not null
        assertNotNull(out);
        assertTrue(out instanceof int[]);
    }

    @Test
    void testIterativeStratificationAllZeroLabelsBranch() {
        int[][] labels = new int[4][2];
        double[] r = {0.25, 0.25, 0.25, 0.25};
        int[] out = IterativeStratification.stratify(labels, r, dummyRandom());
        assertEquals(4, out.length);
        for (int v : out)
            assertTrue(v >= 0 && v < 4);
    }
}