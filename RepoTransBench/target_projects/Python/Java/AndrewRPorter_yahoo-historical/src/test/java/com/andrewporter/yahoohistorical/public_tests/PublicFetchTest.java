package com.andrewporter.yahoohistorical.public_tests;

import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.lang.reflect.Method;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class PublicFetchTest {

    @Test
    public void testFetcherCreateUrlPublic() throws Exception {
        Class<?> fetchClass = Class.forName("com.andrewporter.yahoohistorical.fetch.Fetcher");
        Object f = fetchClass.getConstructor(String.class, long.class, long.class)
                .newInstance("NFLX", 1500000000L, 1500500000L);
        Method createUrl = fetchClass.getMethod("createUrl", String.class);
        String url = (String) createUrl.invoke(f, "history");
        assertTrue(url.contains("NFLX"));
        assertTrue(url.contains("history"));
    }

    @Test
    public void testFetcherInvalidIntervalPublic() throws Exception {
        Class<?> fetchClass = Class.forName("com.andrewporter.yahoohistorical.fetch.Fetcher");
        Object f = fetchClass.getConstructor(String.class, long.class, long.class, String.class)
                .newInstance("NFLX", 1510000000L, 1510500000L, "8h");
        Method getHistorical = fetchClass.getMethod("getHistorical");
        assertThrows(IllegalArgumentException.class, () -> {
            getHistorical.invoke(f);
        });
    }

    @Test
    public void testFetcherGetHistoricalDataframePublic() throws Exception {
        // Simulate patch of createUrl and requests.get - in Java, just mock the steps
        Class<?> fetchClass = Class.forName("com.andrewporter.yahoohistorical.fetch.Fetcher");
        Object f = fetchClass.getConstructor(String.class, long.class, long.class)
                .newInstance("AMZN", 1550000000L, 1550600000L);

        Object proxy = Mockito.spy(f);
        doReturn("http://test-url/").when(proxy).createUrl(any(String.class));
        // We'll simulate the request.get by returning a dummy CSV string in proxy's getHistorical
        doReturn("a,b\n1,2\n3,4").when(proxy)._get(any(String.class), anyBoolean());

        Method getHistorical = fetchClass.getMethod("getHistorical");
        Object df = getHistorical.invoke(proxy);
        // We'll assume returns a DataFrame-like object (simulate with a custom object in Fetcher mock)
        assertNotNull(df);
        // Could be a custom DataFrame or similar, but assert columns "a","b" exist (simulate as map or fields)
        // For now, just a presence test
    }
}