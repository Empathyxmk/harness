package com.example.publictest;

import org.junit.jupiter.api.Test;
import com.example.termplotlib.subplot.Subplot;
import com.example.termplotlib.subplot.SubplotUtil;

import static org.junit.jupiter.api.Assertions.*;

public class TestSubplotPublic {
    @Test
    public void testSubplotInitDifferentData() {
        SubplotUtil.Tuple2 tup = new SubplotUtil.Tuple2(2, 4);
        Subplot sp = new Subplot(tup, 5);
        assertNotNull(sp);
        assertEquals(Subplot.class, sp.getClass());
    }
}