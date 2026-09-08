package com.andrewporter.yahoohistorical.original;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.function.Executable;
import org.mockito.Mockito;

import java.lang.reflect.*;
import java.time.*;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class FetcherCoreTest {

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

    @Test
    public void testGetHistorical() throws Exception {
        Object fetcher = getFetcher(TEST_TICKER, TIME_START, TIME_END);

        // Patch _get method to return CSV string
        Method _get = fetcherClass.getDeclaredMethod("_get", String.class, boolean.class);

        Object proxy = Mockito.spy(fetcher);
        doReturn("col1,col2\n1,2\n3,4").when(proxy)._get(any(String.class), anyBoolean());

        // Directly invoke getHistorical
        Method getHistorical = fetcherClass.getMethod("getHistorical", boolean.class);
        String result = (String) getHistorical.invoke(proxy, false);
        assertTrue(result.contains("col1"));
    }

    @Test
    public void testReprStr() throws Exception {
        Object fetcher = getFetcher(TEST_TICKER, TIME_START, TIME_END);
        String repr = fetcher.toString();
        assertNotNull(repr);
        assertTrue(repr.contains("Fetcher"));
    }

    @Test
    public void testGetHistoryWithKwargs() throws Exception {
        Object fetcher = getFetcher(TEST_TICKER, TIME_START, TIME_END);
        Method _get = fetcherClass.getDeclaredMethod("_get", String.class, boolean.class);

        Object proxy = Mockito.spy(fetcher);
        doReturn("test").when(proxy)._get(any(String.class), anyBoolean());

        Method getHistorical = fetcherClass.getMethod("getHistorical", boolean.class);
        String result = (String) getHistorical.invoke(proxy, false);
        assertEquals("test", result);
    }

    @Test
    public void testGetDividendAndSplit() throws Exception {
        Object fetcher = getFetcher(TEST_TICKER, TIME_START, TIME_END);
        assertThrows(NoSuchMethodException.class, () -> fetcherClass.getMethod("getDividend"));
        assertThrows(NoSuchMethodException.class, () -> fetcherClass.getMethod("getSplit"));
    }

    @Test
    public void testKeyError() throws Exception {
        Object fetcher = getFetcher(TEST_TICKER, TIME_START, TIME_END);
        Object proxy = Mockito.spy(fetcher);
        doThrow(new KeyException("fail")).when(proxy)._get(any(String.class), anyBoolean());
        Method getHistorical = fetcherClass.getMethod("getHistorical");
        assertThrows(KeyException.class, () -> getHistorical.invoke(proxy));
    }

    @Test
    public void testWrongTicker() {
        assertThrows(Exception.class, () -> {
            Object fetcher = getFetcher("", 
                LocalDateTime.of(2020,1,1,0,0).atZone(ZoneId.systemDefault()).toEpochSecond(),
                LocalDateTime.of(2020,1,2,0,0).atZone(ZoneId.systemDefault()).toEpochSecond());
            fetcherClass.getMethod("getHistorical").invoke(fetcher);
        });
    }

    // Helper to instantiate Fetcher
    private Object getFetcher(String ticker, long start, long end) throws Exception {
        return fetcherClass.getConstructor(String.class, long.class, long.class)
                .newInstance(ticker, start, end);
    }
}