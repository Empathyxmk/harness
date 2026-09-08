package com.andrewporter.yahoohistorical.public_tests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class PublicInitImportTest {

    @Test
    public void testImportFetcherPublic() throws Exception {
        // Simulate "from yahoo_historical import Fetcher"
        Class<?> fetcherClass = null;
        try {
            fetcherClass = Class.forName("com.andrewporter.yahoohistorical.Fetcher");
        } catch (ClassNotFoundException e) {
            fetcherClass = Class.forName("com.andrewporter.yahoohistorical.fetch.Fetcher");
        }
        assertNotNull(fetcherClass);

        Object f = fetcherClass.getConstructor(String.class, long.class, long.class)
                .newInstance("msft", 1650000000L, 1650001000L);

        boolean found = false;
        for (var m : fetcherClass.getMethods()) {
            if (m.getName().equals("getHistorical")) {
                found = true;
                break;
            }
        }
        assertTrue(found, "Fetcher should have a getHistorical method");
    }
}