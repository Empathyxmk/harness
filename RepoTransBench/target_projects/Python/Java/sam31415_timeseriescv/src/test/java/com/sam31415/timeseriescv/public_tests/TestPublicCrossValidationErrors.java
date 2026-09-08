package com.sam31415.timeseriescv.public_tests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestPublicCrossValidationErrors {

    @Test
    public void testErrorsNSplitsPublic() {
        double[][] df = new double[15][1];
        PurgedWalkForwardCV cv = new PurgedWalkForwardCV(16, 1, 1, 0);
        assertThrows(IllegalArgumentException.class, () -> {
            cv.split(df).get(0);
        });
    }

    @Test
    public void testErrorsTrainLengthPublic() {
        double[][] df = new double[12][1];
        PurgedWalkForwardCV cv = new PurgedWalkForwardCV(3, 11, 2, 0);
        assertThrows(IllegalArgumentException.class, () -> {
            cv.split(df).get(0);
        });
    }

    @Test
    public void testErrorsTestLengthPublic() {
        double[][] df = new double[10][1];
        PurgedWalkForwardCV cv = new PurgedWalkForwardCV(2, 2, 9, 0);
        assertThrows(IllegalArgumentException.class, () -> {
            cv.split(df).get(0);
        });
    }

    @Test
    public void testErrorsLookaheadNegativePublic() {
        assertThrows(IllegalArgumentException.class, () -> {
            new PurgedWalkForwardCV(2, 2, 2, -4);
        });
    }

    @Test
    public void testBaseCVSplitSignaturePublic() {
        class DummyCV extends BaseTimeSeriesCrossValidator {
            @Override
            public int getNSplits(Object X, Object y, Object predTimes, Object evalTimes) { return 1; }
        }
        double[][] df = new double[4][1];
        DummyCV cv = new DummyCV();
        assertThrows(UnsupportedOperationException.class, () -> {
            cv.split(df).get(0);
        });
    }
}