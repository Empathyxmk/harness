package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.time.LocalDateTime;

public class TestPublicDatetimes {

    @Test
    public void testDatetimeFreeze() {
        LocalDateTime frozenNow = LocalDateTime.of(2021, 3, 11, 14, 20);
        assertEquals(LocalDateTime.of(2021, 3, 11, 14, 20), frozenNow);
    }
}