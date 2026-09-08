package com.trentb.public_tests;

import com.trentb.iterstrat.IterativeStratification;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.api.Test;

import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.*;

class TestPublicIterativeStratification {
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

    private DummyRandomStatePublic dummyRandom() {
        return new DummyRandomStatePublic();
    }

    static Stream<TestParams> paramsProvider() {
        return Stream.of(
                new TestParams(
                        new int[][]{{0,1,0},{0,0,1},{1,1,0},{0,1,1},{1,0,1}},
                        new double[]{0.7,0.3},
                        2, false),
                new TestParams(
                        new int[][]{{0}, {0}, {1}, {1}},
                        new double[]{0.4, 0.6},
                        2, true)
        );
    }

    @ParameterizedTest
    @MethodSource("paramsProvider")
    void testIterativeStratificationVariedPublic(TestParams param) {
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
            assertTrue(o >= 0 && o < param.expectedNumFolds, "Public: Value out of expected range");
        }
    }

    @Test
    void testIterativeStratificationAllOnesLabelPublic() {
        int[][] labels = new int[4][3];
        for (int[] row : labels) java.util.Arrays.fill(row, 1);
        double[] r = {0.2, 0.4, 0.4};
        int[] out = IterativeStratification.stratify(labels, r, dummyRandom());
        assertEquals(4, out.length);
    }

    @Test
    void testIterativeStratificationSingleFoldPublic() {
        int[][] labels = {
                {1,0,0,0,0},
                {0,1,0,0,0},
                {0,0,1,0,0},
                {0,0,0,1,0},
                {0,0,0,0,1}
        };
        double[] r = {1.0};
        int[] out = IterativeStratification.stratify(labels, r, dummyRandom());
        for (int i : out) assertEquals(0, i);
    }

    @Test
    void testIterativeStratificationRandomOutputTypesPublic() {
        int[][] labels = {{0, 1}, {1, 1}};
        double[] r = {0.7, 0.3};
        int[] out = IterativeStratification.stratify(labels, r, dummyRandom());
        assertNotNull(out);
        assertTrue(out instanceof int[]);
    }

    @Test
    void testIterativeStratificationAllZeroLabelsBranchPublic() {
        int[][] labels = new int[3][5];
        double[] r = {0.2, 0.2, 0.2, 0.2, 0.2};
        int[] out = IterativeStratification.stratify(labels, r, dummyRandom());
        assertEquals(3, out.length);
        for (int v : out)
            assertTrue(v >= 0 && v < 5);
    }
}