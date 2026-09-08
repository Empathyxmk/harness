package com.example.original;

import org.junit.jupiter.api.Test;
import com.example.termplotlib.subplot.Subplot;
import com.example.termplotlib.subplot.SubplotUtil;

import static org.junit.jupiter.api.Assertions.*;

public class TestSubplot {
    @Test
    public void testSubplotInit() {
        // Mimics: Subplot((3,3), 7)
        SubplotUtil.Tuple2 tup = new SubplotUtil.Tuple2(3, 3);
        Subplot sp = new Subplot(tup, 7);
        assertNotNull(sp);
        assertEquals(Subplot.class, sp.getClass());
    }
}