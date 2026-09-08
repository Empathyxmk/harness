package com.ramonhagenaars.jsons.public_tests;

import org.junit.jupiter.api.Test;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import static org.junit.jupiter.api.Assertions.*;

public class PublicDefaultTimeTest {

    @Test
    void testDefaultTimeDumpPublic() {
        LocalTime t = LocalTime.of(14, 22, 6);
        assertEquals(14, t.getHour());
        assertEquals(22, t.getMinute());
        assertEquals(6, t.getSecond());
    }

    @Test
    void testDefaultTimeLoadPublic() {
        LocalTime t = LocalTime.parse("07:55:44", DateTimeFormatter.ofPattern("HH:mm:ss"));
        assertEquals(7, t.getHour());
        assertEquals(55, t.getMinute());
        assertEquals(44, t.getSecond());
    }
}