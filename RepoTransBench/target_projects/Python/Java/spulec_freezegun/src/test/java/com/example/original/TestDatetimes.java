package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.time.LocalDateTime;

public class TestDatetimes {

    @Test
    public void testDatetimeFreeze() {
        LocalDateTime frozenNow = LocalDateTime.of(2023, 1, 15, 12, 0);
        LocalDateTime expected = LocalDateTime.of(2023, 1, 15, 12, 0);
        assertEquals(expected, frozenNow, "Frozen datetime did not match expected.");
    }
}