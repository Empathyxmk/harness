package com.sam31415.timeseriescv.public_tests;

import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class TestPublicCrossValidation {

    @Test
    public void testPurgedWalkForwardCVNondefaultPublic() {
        // Using 'train_length' and 'test_length' as in the source, with different values than private
        int[] arr = new int[30];
        for (int i = 0; i < 30; i++) arr[i] = 40+i;
        double[][] data = new double[30][1];
        for (int i = 0; i < arr.length; i++) data[i][0] = arr[i];
        PurgedWalkForwardCV cv = new PurgedWalkForwardCV(5, 6, 2, 1);
        List<int[][]> splits = new ArrayList<>();
        for (int[][] split : cv.split(data)) {
            splits.add(new int[][]{Arrays.copyOf(split[0], split[0].length), Arrays.copyOf(split[1], split[1].length)});
        }
        assertEquals(5, splits.size());
        assertEquals(0, splits.get(0)[0][0]);
        assertEquals(data.length-1, splits.get(splits.size()-1)[1][splits.get(splits.size()-1)[1].length-1]);
    }

    @Test
    public void testEmbargoPublic() {
        boolean[] arr = new boolean[20];
        CrossValidationTestUtils.embargo(arr, 6, 13, 4);
        // 13,14,15,16 should be embargoed
        for (int i = 13; i < 17; i++) {
            assertTrue(arr[i]);
        }
        assertFalse(arr[12]);
    }

    @Test
    public void testWalkforwardLengthPublic() {
        double[][] X = new double[34][1];
        for (int i = 0; i < X.length; i++)
            X[i][0] = 30 + i;
        PurgedWalkForwardCV cv = new PurgedWalkForwardCV(2, 12, 9, 2);
        List<int[][]> splits = cv.split(X);
        assertEquals(2, splits.size());
        int last = -1;
        for (int[][] split : splits) {
            assertTrue(split[1][0] > last);
            last = split[1][split[1].length-1];
        }
    }

    @Test
    public void testReprPublic() {
        PurgedWalkForwardCV cv = new PurgedWalkForwardCV(3, 8, 3, 3);
        String rp = cv.toString();
        assertTrue(rp.contains("PurgedWalkForwardCV") && rp.contains("nSplits=3"));
    }

    @Test
    public void testCrossValidatorBasePublic() {
        class DummyCV extends BaseTimeSeriesCrossValidator {
            @Override
            public Iterable<int[][]> split(Object X, Object y, Object predTimes, Object evalTimes) {
                int n = 0;
                if (X instanceof double[][]) n = ((double[][])X).length;
                else if (X instanceof int[][]) n = ((int[][])X).length;
                else if (X instanceof Object[]) n = ((Object[])X).length;
                int n3 = n/3, n2 = n/2;
                int[] t1 = CrossValidationTestUtils.rangeEnd(0, n3);
                int[] t2 = CrossValidationTestUtils.rangeEnd(n3, n2);
                return Collections.singletonList(new int[][]{t1, t2});
            }
            @Override
            public int getNSplits(Object X, Object y, Object predTimes, Object evalTimes) { return 1; }
        }
        double[][] X = new double[10][1];
        for (int i = 0; i < 10; i++) X[i][0] = i;
        List<int[][]> splits = new ArrayList<>();
        for (int[][] split : new DummyCV().split(X)) {
            splits.add(split);
        }
        assertEquals(1, splits.size());
        int[] trainIdx = splits.get(0)[0];
        int[] testIdx = splits.get(0)[1];
        assertTrue(trainIdx.length > 0);
        assertTrue(testIdx.length > 0);
        Set<Integer> tr = CrossValidationTestUtils.asSet(trainIdx);
        Set<Integer> te = CrossValidationTestUtils.asSet(testIdx);
        assertTrue(Collections.disjoint(tr, te));
    }

    @Test
    public void testPurgedWalkForwardCVGetNSplitsPublic() {
        double[][] df = new double[29][1];
        for (int i = 0; i < 29; i++) df[i][0] = 30 + i;
        PurgedWalkForwardCV cv = new PurgedWalkForwardCV(3, 7, 2, 2);
        assertEquals(3, cv.getNSplits(df));
    }

    @Test
    public void testSplitIndicesNonOverlapPublic() {
        double[][] df = new double[24][1];
        for (int i = 0; i < 24; i++) df[i][0] = 70 + i;
        PurgedWalkForwardCV cv = new PurgedWalkForwardCV(4, 5, 5, 3);
        for (int[][] split : cv.split(df)) {
            Set<Integer> tr = CrossValidationTestUtils.asSet(split[0]);
            Set<Integer> te = CrossValidationTestUtils.asSet(split[1]);
            assertTrue(Collections.disjoint(tr, te));
        }
    }

    @Test
    public void testLargeEmbargoEdgePublic() {
        boolean[] mask = new boolean[12];
        CrossValidationTestUtils.embargo(mask, 8, 10, 4);
        for (int i = 10; i < 12; i++) {
            assertTrue(mask[i]);
        }
    }
}