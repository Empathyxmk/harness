package com.example.homu.publictests;

import com.example.homu.utils.Utils;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class UtilsPublicTest {

    @Test
    public void testAlphanumericOnlyPublic() {
        assertEquals("xyz789GH", Utils.alphanumericOnly("xyz789GH@#!"));
        assertEquals("321", Utils.alphanumericOnly(" **&$  321 "));
    }
}