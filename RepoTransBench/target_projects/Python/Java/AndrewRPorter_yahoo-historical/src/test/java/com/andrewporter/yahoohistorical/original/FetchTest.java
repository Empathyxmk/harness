package com.andrewporter.yahoohistorical.original;

import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.lang.reflect.Method;
import java.time.LocalDateTime;
import java.time.ZoneId;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class FetchTest {

    private static Class<?> fetcherClass;
    private static final String TEST_TICKER = "AAPL";
    private static final long TIME_START = LocalDateTime.of(2017, 1, 1, 0, 0).atZone(ZoneId.systemDefault()).toEpochSecond();
    private static final long TIME_END = LocalDateTime.of(2017, 1, 4, 0, 0).atZone(ZoneId.systemDefault()).toEpochSecond();

    static {
        try {
            fetcherClass = Class.forName("com.andrewporter.yahoohistorical.fetch.Fetcher");
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    /**
     * Helper mock for _get method according to as_dataframe
     */
    private Object mockGetHistorical(Object fetcher, boolean asDataFrame) {
        if (asDataFrame) {
            // Fake a 'DataFrame' which in Java we simulate as a List
            return new DummyDataFrame();
        } else {
            // Simulate CSV data string
            return "col1,col2\n1,2\n3,4";
        }
    }

    public static class DummyDataFrame {
        public int[] get(String colName) { return new int[]{1,2,3}; }
    }

    @Test
    public void testGetNoDataFrame() throws Exception {
        Object fetcher = getFetcher(TEST_TICKER, TIME_START, TIME_END);
        Object proxy = Mockito.spy(fetcher);
        // Patch _get to return data string
        doReturn("col1,col2\n1,2\n3,4").when(proxy)._get(any(String.class), anyBoolean());

        Method getHistorical = fetcherClass.getMethod("getHistorical", boolean.class);
        String result = (String) getHistorical.invoke(proxy, false);
        assertTrue(result.contains("col1"));
    }

    @Test
    public void testGetWithLowercase() throws Exception {
        Object fetcher = getFetcher(TEST_TICKER.toLowerCase(), TIME_START, TIME_END);
        Object proxy = Mockito.spy(fetcher);
        doReturn(new DummyDataFrame()).when(proxy)._get(any(String.class), anyBoolean());
        Method getHistorical = fetcherClass.getMethod("getHistorical");
        Object df = getHistorical.invoke(proxy);
        assertNotNull(df);
        assertTrue(df instanceof DummyDataFrame);
    }

    @Test
    public void testGetHistorical() throws Exception {
        Object fetcher = getFetcher(TEST_TICKER, TIME_START, TIME_END);
        Object proxy = Mockito.spy(fetcher);
        doReturn(new DummyDataFrame()).when(proxy)._get(any(String.class), anyBoolean());
        Method getHistorical = fetcherClass.getMethod("getHistorical");
        Object df = getHistorical.invoke(proxy);
        assertNotNull(df);
        assertTrue(df instanceof DummyDataFrame);
    }

    @Test
    public void testInvalidDate() throws Exception {
        // Simulates passing wrong type for date -- in Java, this would be compile-time, so we simulate runtime error.
        // We'll use reflection and force an exception by passing a string instead of long
        assertThrows(Exception.class, () -> {
            fetcherClass.getConstructor(String.class, Object.class, long.class)
                    .newInstance(TEST_TICKER, "invalid_date", TIME_END);
        });
    }

    @Test
    public void testFetcherWithFloatDates() throws Exception {
        double start = (double) TIME_START;
        double end = (double) TIME_END;
        Object fetcher = fetcherClass.getConstructor(String.class, double.class, double.class)
                .newInstance(TEST_TICKER, start, end);
        Object proxy = Mockito.spy(fetcher);
        doReturn(new DummyDataFrame()).when(proxy)._get(any(String.class), anyBoolean());
        Method getHistorical = fetcherClass.getMethod("getHistorical");
        Object df = getHistorical.invoke(proxy);
        assertNotNull(df);
        assertTrue(df instanceof DummyDataFrame);
    }

    private Object getFetcher(String ticker, long start, long end) throws Exception {
        return fetcherClass.getConstructor(String.class, long.class, long.class)
                .newInstance(ticker, start, end);
    }
}