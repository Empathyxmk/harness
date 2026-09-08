package com.sam31415.timeseriescv.original;

import org.junit.jupiter.api.Test;

import java.util.Date;

import static org.junit.jupiter.api.Assertions.*;

public class TestCrossValidationErrors {

    static class DummyCV extends BaseTimeSeriesCrossValidator {
        public DummyCV(int nSplits) { super(nSplits); }
        @Override
        public Iterable<int[][]> split(Object X, Object y, Object predTimes, Object evalTimes) {
            return super.split(X, y, predTimes, evalTimes);
        }
    }

    @Test
    public void testNSplitsType() {
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            new BaseTimeSeriesCrossValidator("not_an_int");
        });
        assertTrue(exception.getMessage().contains("Integral"));
    }

    @Test
    public void testNSplitsTooLow() {
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            new BaseTimeSeriesCrossValidator(1);
        });
        assertTrue(exception.getMessage().contains("n_splits = 2 or more"));
    }

    @Test
    public void testSplitInvalidXType() {
        DummyCV cv = new DummyCV(2);
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            cv.split(new int[]{1,2,3}, null, null, null);
        });
        assertTrue(exception.getMessage().contains("DataFrame/Series"));
    }

    @Test
    public void testSplitInvalidYType() {
        DummyCV cv = new DummyCV(2);
        Object X = CrossValidationTestUtils.makeDataFrame(new int[][]{{1,2},{3,4}});
        Object predTimes = CrossValidationTestUtils.makeSeries(new int[]{1,2}, new int[]{0,1});
        Object evalTimes = CrossValidationTestUtils.makeSeries(new int[]{1,2}, new int[]{0,1});
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            cv.split(X, new int[]{1,2}, predTimes, evalTimes);
        });
        assertTrue(exception.getMessage().contains("y should be"));
    }

    @Test
    public void testSplitInvalidPredTimesType() {
        DummyCV cv = new DummyCV(2);
        Object X = CrossValidationTestUtils.makeDataFrame(new int[][]{{1,2}});
        Object y = CrossValidationTestUtils.makeSeries(new int[]{1,2}, new int[]{0,1});
        Object evalTimes = CrossValidationTestUtils.makeSeries(new int[]{1,2}, new int[]{0,1});
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            cv.split(X, y, new int[]{1,2}, evalTimes);
        });
        assertTrue(exception.getMessage().contains("pred_times should be"));
    }

    @Test
    public void testSplitInvalidEvalTimesType() {
        DummyCV cv = new DummyCV(2);
        Object X = CrossValidationTestUtils.makeDataFrame(new int[][]{{1,2}});
        Object y = CrossValidationTestUtils.makeSeries(new int[]{1,2}, new int[]{0,1});
        Object predTimes = CrossValidationTestUtils.makeSeries(new int[]{1,2}, new int[]{0,1});
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            cv.split(X, y, predTimes, new int[]{1,2});
        });
        assertTrue(exception.getMessage().contains("eval_times should be"));
    }

    @Test
    public void testSplitIndexMismatchY() {
        DummyCV cv = new DummyCV(2);
        Object X = CrossValidationTestUtils.makeDataFrame(new int[][]{{1},{2}}, new int[]{10,11});
        Object y = CrossValidationTestUtils.makeSeries(new int[]{1,2}, new int[]{99,98});
        Object predTimes = CrossValidationTestUtils.makeSeries(new int[]{1,2}, new int[]{10,11});
        Object evalTimes = CrossValidationTestUtils.makeSeries(new int[]{1,2}, new int[]{10,11});
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            cv.split(X, y, predTimes, evalTimes);
        });
        assertTrue(exception.getMessage().contains("same index"));
    }

    @Test
    public void testSplitIndexMismatchPredTimes() {
        DummyCV cv = new DummyCV(2);
        Object X = CrossValidationTestUtils.makeDataFrame(new int[][]{{1}, {2}}, new int[]{1,2});
        Object y = CrossValidationTestUtils.makeSeries(new int[]{1,2}, new int[]{1,2});
        Object predTimes = CrossValidationTestUtils.makeSeries(new int[]{1,2}, new int[]{3,4});
        Object evalTimes = CrossValidationTestUtils.makeSeries(new int[]{1,2}, new int[]{1,2});
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            cv.split(X, y, predTimes, evalTimes);
        });
        assertTrue(exception.getMessage().contains("pred_times must have the same index"));
    }

    @Test
    public void testSplitIndexMismatchEvalTimes() {
        DummyCV cv = new DummyCV(2);
        Object X = CrossValidationTestUtils.makeDataFrame(new int[][]{{1}, {2}}, new int[]{1,2});
        Object y = CrossValidationTestUtils.makeSeries(new int[]{1,2}, new int[]{1,2});
        Object predTimes = CrossValidationTestUtils.makeSeries(new int[]{1,2}, new int[]{1,2});
        Object evalTimes = CrossValidationTestUtils.makeSeries(new int[]{1,2}, new int[]{99,98});
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            cv.split(X, y, predTimes, evalTimes);
        });
        assertTrue(exception.getMessage().contains("eval_times must have the same index"));
    }

    @Test
    public void testSplitPredTimesNotSorted() {
        DummyCV cv = new DummyCV(2);
        Object X = CrossValidationTestUtils.makeDataFrame(new int[][]{{1},{2}}, new int[]{1,2});
        Object y = CrossValidationTestUtils.makeSeries(new int[]{1,2}, new int[]{1,2});
        Object predTimes = CrossValidationTestUtils.makeSeries(new int[]{2,1}, new int[]{1,2});
        Object evalTimes = CrossValidationTestUtils.makeSeries(new int[]{1,2}, new int[]{1,2});
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            cv.split(X, y, predTimes, evalTimes);
        });
        assertTrue(exception.getMessage().contains("pred_times should be sorted"));
    }

    @Test
    public void testSplitEvalTimesNotSorted() {
        DummyCV cv = new DummyCV(2);
        Object X = CrossValidationTestUtils.makeDataFrame(new int[][]{{1},{2}}, new int[]{1,2});
        Object y = CrossValidationTestUtils.makeSeries(new int[]{1,2}, new int[]{1,2});
        Object predTimes = CrossValidationTestUtils.makeSeries(new int[]{1,2}, new int[]{1,2});
        Object evalTimes = CrossValidationTestUtils.makeSeries(new int[]{2,1}, new int[]{1,2});
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            cv.split(X, y, predTimes, evalTimes);
        });
        assertTrue(exception.getMessage().contains("eval_times should be sorted"));
    }
}