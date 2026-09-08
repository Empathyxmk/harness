package com.itsdangerous.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.itsdangerous.Itsdangerous;

public class InitTest {

    @Test
    public void testVersion() {
        assertEquals("3.1.1", Itsdangerous.getVersion());
    }
}