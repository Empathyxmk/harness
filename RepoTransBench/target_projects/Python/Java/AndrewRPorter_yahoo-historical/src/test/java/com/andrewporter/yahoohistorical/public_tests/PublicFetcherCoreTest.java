package com.andrewporter.yahoohistorical.public_tests;

import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import java.lang.reflect.Method;
import java.time.LocalDateTime;
import java.time.ZoneId;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class PublicFetcherCoreTest {

    private static Class<?> fetcherClass;
    private static final String TEST_TICKER_PUBLIC = "GOOG";
    private static final long TIME_START_PUBLIC = LocalDateTime.of(2018, 2, 1, 0, 0).atZone(ZoneId.systemDefault()).toEpochSecond();
    private static final long TIME_END_PUBLIC = LocalDateTime.of(2018, 2, 5, 0, 0).atZone(ZoneId.systemDefault()).toEpochSecond();

    static {
        try {
            fetcherClass = Class.forName("com.andrewporter.yahoohistorical.fetch.Fetcher");
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Test
    public void testGetHistoricalPublic() throws Exception {
        Object fetcher = getFetcher(TEST_TICKER_PUBLIC, TIME_START_PUBLIC, TIME_END_PUBLIC);
        Object proxy = Mockito.spy(fetcher);
        doReturn("open,close\n5,6\n7,8").when(proxy)._get(any(String.class), anyBoolean());
        Method getHistorical = fetcherClass.getMethod("getHistorical", boolean.class);
        String result = (String) getHistorical.invoke(proxy, false);
        assertTrue(result.contains("open"));
    }

    @Test
    public void testReprStrPublic() throws Exception {
        Object fetcher = getFetcher(TEST_TICKER_PUBLIC, TIME_START_PUBLIC, TIME_END_PUBLIC);
        String r = fetcher.toString();
        assertTrue(r.contains("Fetcher") && r.contains("GOOG"));
    }

    @Test
    public void testGetHistoryWithKwargsPublic() throws Exception {
        Object fetcher = getFetcher(TEST_TICKER_PUBLIC, TIME_START_PUBLIC, TIME_END_PUBLIC);
        Object proxy = Mockito.spy(fetcher);
        doReturn("public_test").when(proxy)._get(any(String.class), anyBoolean());
        Method getHistorical = fetcherClass.getMethod("getHistorical", boolean.class);
        String got = (String) getHistorical.invoke(proxy, false);
        assertEquals("public_test", got);
    }

    @Test
    public void testGetDividendAndSplitPublic() throws Exception {
        Object fetcher = getFetcher(TEST_TICKER_PUBLIC, TIME_START_PUBLIC, TIME_END_PUBLIC);
        try {
            fetcherClass.getMethod("getDividend").invoke(fetcher);
            fetcherClass.getMethod("getSplit").invoke(fetcher);
            fail("Should have raised Exception or AttributeError");
        } catch (NoSuchMethodException e) {
            // Expected: methods don't exist
        } catch (Exception ex) {
            // Method exists, but may throw
        }
    }

    @Test
    public void testKeyerrorPublic() throws Exception {
        Object fetcher = getFetcher(TEST_TICKER_PUBLIC, TIME_START_PUBLIC, TIME_END_PUBLIC);
        Object proxy = Mockito.spy(fetcher);
        doThrow(new java.util.KeyException("fail-public")).when(proxy)._get(any(String.class), anyBoolean());
        Method getHistorical = fetcherClass.getMethod("getHistorical");
        assertThrows(java.util.KeyException.class, () -> getHistorical.invoke(proxy));
    }

    @Test
    public void testWrongTickerPublic() throws Exception {
        assertThrows(Exception.class, () -> {
            Object fetcher = getFetcher(
                    "!!!",
                    LocalDateTime.of(2019, 3, 4, 0, 0).atZone(ZoneId.systemDefault()).toEpochSecond(),
                    LocalDateTime.of(2019, 3, 5, 0, 0).atZone(ZoneId.systemDefault()).toEpochSecond()
            );
            fetcherClass.getMethod("getHistorical").invoke(fetcher);
        });
    }

    private Object getFetcher(String ticker, long start, long end) throws Exception {
        return fetcherClass.getConstructor(String.class, long.class, long.class)
                .newInstance(ticker, start, end);
    }
}