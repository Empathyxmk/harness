package com.example.homu.original;

import com.example.homu.utils.Utils;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.HashMap;
import java.util.Map;

public class UtilsTest {

    @Test
    public void testAlphanumericOnlyCases() {
        assertEquals("abc123DEF", Utils.alphanumericOnly("abc123DEF!@#"));
        assertEquals("456", Utils.alphanumericOnly(" **&$  456 "));
    }
}