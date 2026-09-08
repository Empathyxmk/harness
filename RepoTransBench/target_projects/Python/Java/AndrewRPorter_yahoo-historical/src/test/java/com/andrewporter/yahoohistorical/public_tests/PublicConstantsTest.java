package com.andrewporter.yahoohistorical.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicConstantsTest {

    @Test
    public void testConstantsFieldsPublic() throws Exception {
        Class<?> constants = Class.forName("com.andrewporter.yahoohistorical.constants.Constants");
        assertNotNull(constants.getField("API_URL"));
        assertNotNull(constants.getField("DATE_INTERVALS"));
        assertNotNull(constants.getField("ONE_DAY_INTERVAL"));
        Object intervals = constants.getField("DATE_INTERVALS").get(null);
        assertTrue(intervals.toString().contains("1d"));
        Object oneDay = constants.getField("ONE_DAY_INTERVAL").get(null);
        assertEquals("1d", oneDay);
    }

    @Test
    public void testApiUrlFormatPublic() throws Exception {
        Class<?> constants = Class.forName("com.andrewporter.yahoohistorical.constants.Constants");
        String API_URL = (String) constants.getField("API_URL").get(null);
        String url = String.format(API_URL, "TSLA", 1610000000L, 1610020000L, "1d", "history");
        assertTrue(url.contains("TSLA") && url.contains("16100") && url.contains("1d"));
        assertTrue(url.indexOf("history") > 0);
    }
}