package com.venthur.gscholar.original;

import com.venthur.gscholar.GScholar;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestVersion {

    @Test
    public void testVersion() {
        assertTrue(GScholar.__VERSION__ instanceof String);
    }
}