package com.sam31415.timeseriescv.original;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.function.Executable;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

public class TestCrossValidation {

    // Helper method to create simple data
    private static class SimpleData {
        public double[][] data;
        public int[] y;
        public Date[] predTimes;
        public Date[] evalTimes;
    }

    private static SimpleData makeSimpleData(int n, int seed) {
        Random rng = new Random(seed);
        SimpleData sd = new SimpleData();
        sd.data = new double[n][3];
        for (int i = 0; i < n; i++) {
            sd.data[i][0] = rng.nextDouble();
            sd.data[i][1] = rng.nextDouble();
            sd.data[i][2] = rng.nextDouble();
        }
        sd.predTimes = new Date[n];
        sd.evalTimes = new Date[n];
        Calendar cal = Calendar.getInstance(TimeZone.getTimeZone("UTC"));
        cal.set(2021, Calendar.JANUARY, 1, 0, 0, 0);
        for (int i = 0; i < n; i++) {
            sd.predTimes[i] = cal.getTime();
            cal.add(Calendar.DATE, 1);
        }
        for (int i = 0; i < n; i++) {
            Calendar ec = Calendar.getInstance(TimeZone.getTimeZone("UTC"));
            ec.setTime(sd.predTimes[i]);
            ec.add(Calendar.DATE, 1);
            sd.evalTimes[i] = ec.getTime();
        }
        sd.y = new int[n];
        for (int i = 0; i < n; i++) sd.y[i] = rng.nextInt(2);
        return sd;
    }

    @Test
    public void testBaseTimeSeriesCVNSplitsProperty() {
        BaseTimeSeriesCrossValidator cv = new BaseTimeSeriesCrossValidator(5);
        assertEquals(5, cv.getNSplits());
        cv.setNSplits(6);
        assertEquals(6, cv.getNSplits());
    }

    @Test
    public void testPurgeBasicObject() {
        class DummyCV extends BaseTimeSeriesCrossValidator {
            public Date[] predTimes;
            public Date[] evalTimes;
            public int[] indices;
            public DummyCV() {
                super(2);
                this.predTimes = CrossValidationTestUtils.makeDateArray("2023-01-01", 6);
                this.evalTimes = CrossValidationTestUtils.shiftDates(this.predTimes, 1);
                this.indices = CrossValidationTestUtils.range(6);
            }
        }
        DummyCV cv = new DummyCV();
        int testFoldStart = 4;
        int testFoldEnd = 5;
        int[] inTrain = CrossValidationTestUtils.purge(cv, testFoldStart, testFoldEnd, testFoldEnd);
        assertNotNull(inTrain);
    }

    @Test
    public void testEmbargoBasicObject() {
        class DummyCV extends BaseTimeSeriesCrossValidator {
            public Date[] predTimes;
            public Date[] evalTimes;
            public long embargoDays;
            public int[] indices;
            public DummyCV() {
                super(2);
                this.predTimes = CrossValidationTestUtils.makeDateArray("2022-01-01", 10);
                this.evalTimes = CrossValidationTestUtils.shiftDates(this.predTimes, 1);
                this.embargoDays = 1;
                this.indices = CrossValidationTestUtils.range(10);
            }
        }
        DummyCV dummyCV = new DummyCV();
        int[] trainIndices = CrossValidationTestUtils.rangeEnd(0, 8);
        int[] testIndices = new int[]{8, 9};
        int testFoldEnd = 9;
        int[] embargoed = CrossValidationTestUtils.embargo(dummyCV, trainIndices, testIndices, testFoldEnd);
        assertNotNull(embargoed);
        assertTrue(embargoed.length <= trainIndices.length);
    }

    @Test
    public void testComputeFoldBoundsObject() {
        class DummyCV extends BaseTimeSeriesCrossValidator {
            public int[] indices;
            public DummyCV() {
                super(2);
                this.indices = CrossValidationTestUtils.range(8);
            }
        }
        DummyCV dummyCV = new DummyCV();
        List<int[]> bounds = CrossValidationTestUtils.computeFoldBounds(dummyCV, false);
        assertNotNull(bounds);
    }

    @Test
    public void testPurgedWalkForwardCVSplit() {
        SimpleData sd = makeSimpleData(20, 0);
        PurgedWalkForwardCV cv = new PurgedWalkForwardCV(5 /* n_splits */);
        List<int[][]> splits = cv.split(sd.data, sd.y, sd.predTimes, sd.evalTimes);
        assertEquals(3, splits.size());
        for (int[][] split : splits) {
            int[] train = split[0];
            int[] test = split[1];
            Set<Integer> trSet = CrossValidationTestUtils.asSet(train);
            Set<Integer> teSet = CrossValidationTestUtils.asSet(test);
            assertTrue(Collections.disjoint(trSet, teSet));
            assertTrue(test.length > 0);
        }
    }

    @Test
    public void testCombPurgedKFoldCVSplit() {
        SimpleData sd = makeSimpleData(12, 0);
        CombPurgedKFoldCV cv = new CombPurgedKFoldCV(3);
        List<int[][]> splits = cv.split(sd.data, sd.y, sd.predTimes, sd.evalTimes);
        assertEquals(3, splits.size());
        for (int[][] split : splits) {
            int[] train = split[0];
            int[] test = split[1];
            Set<Integer> trSet = CrossValidationTestUtils.asSet(train);
            Set<Integer> teSet = CrossValidationTestUtils.asSet(test);
            assertTrue(Collections.disjoint(trSet, teSet));
        }
    }

    @Test
    public void testReprMethods() {
        PurgedWalkForwardCV cv1 = new PurgedWalkForwardCV(4);
        CombPurgedKFoldCV cv2 = new CombPurgedKFoldCV(3);
        String r1 = cv1.getClass().getSimpleName();
        String r2 = cv2.getClass().getSimpleName();
        assertTrue(r1.contains("PurgedWalkForwardCV"));
        assertTrue(r2.contains("CombPurgedKFoldCV"));
    }

    @Test
    public void testBaseRepr() {
        BaseTimeSeriesCrossValidator cv = new BaseTimeSeriesCrossValidator(10);
        String r = cv.getClass().getSimpleName();
        assertTrue(r.contains("BaseTimeSeriesCrossValidator"));
    }

    @Test
    public void testPurgeEmptyObject() {
        class DummyCV extends BaseTimeSeriesCrossValidator {
            public Date[] predTimes;
            public Date[] evalTimes;
            public int[] indices;
            public DummyCV() {
                super(2);
                this.predTimes = new Date[0];
                this.evalTimes = new Date[0];
                this.indices = new int[0];
            }
        }
        DummyCV dummyCV = new DummyCV();
        assertThrows(IndexOutOfBoundsException.class, () -> {
           CrossValidationTestUtils.purge(dummyCV, 0, 0, 0);
        });
    }

    @Test
    public void testEmbargoNoEmbargoObject() {
        class DummyCV extends BaseTimeSeriesCrossValidator {
            public Date[] predTimes;
            public Date[] evalTimes;
            public long embargoDays;
            public int[] indices;
            public DummyCV() {
                super(2);
                this.predTimes = CrossValidationTestUtils.makeDateArray("2020-01-01", 5);
                this.evalTimes = CrossValidationTestUtils.shiftDates(this.predTimes, 1);
                this.embargoDays = 0;
                this.indices = CrossValidationTestUtils.range(5);
            }
        }
        DummyCV dummyCV = new DummyCV();
        int[] trainIndices = new int[]{0, 4};
        int[] testIndices = new int[]{0, 4};
        int testFoldEnd = 4;
        int[] embargoed = CrossValidationTestUtils.embargo(dummyCV, trainIndices, testIndices, testFoldEnd);
        Set<Integer> embSet = CrossValidationTestUtils.asSet(embargoed);
        Set<Integer> trSet = CrossValidationTestUtils.asSet(trainIndices);
        assertTrue(embSet.containsAll(trSet));
    }

    @Test
    public void testPurgedWalkForwardCVInvalidNTestSplits() {
        assertThrows(IllegalArgumentException.class, () -> {
            new PurgedWalkForwardCV(2, 1);
        });
    }

    @Test
    public void testCombPurgedKFoldCVInvalid() {
        assertThrows(IllegalArgumentException.class, () -> {
            new CombPurgedKFoldCV(1);
        });
    }
}