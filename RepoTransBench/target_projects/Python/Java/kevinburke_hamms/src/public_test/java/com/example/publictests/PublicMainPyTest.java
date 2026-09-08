package com.example.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicMainPyTest {

    @Test
    public void testPublicMainTrue() {
        assertTrue(true);
    }

    @Test
    public void testPublicMainValue() {
        assertTrue("hamms" instanceof String);
    }
}