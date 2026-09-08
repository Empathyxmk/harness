package com.github.tonyo.pyope.original;

import com.github.tonyo.pyope.hgd.HGD;
import com.github.tonyo.pyope.ope.ValueRange;
import com.github.tonyo.pyope.stat.StatUtils;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Random;

import static org.junit.jupiter.api.Assertions.*;

class StatTest {

    @Test
    void testUniform() {
        // Short ranges
        int value = 10;
        ValueRange unitRange = new ValueRange(value, value);
        assertEquals(value, StatUtils.sampleUniform(unitRange, new ArrayList<>()));

        ValueRange shortRange = new ValueRange(value, value + 1);
        List<Integer> c01 = new ArrayList<>();
        c01.add(0);
        assertEquals(value, StatUtils.sampleUniform(shortRange, c01));
        List<Integer> c1 = new ArrayList<>();
        c1.add(1);
        assertEquals(value + 1, StatUtils.sampleUniform(shortRange, c1));
        List<Object> more = new ArrayList<>();
        more.add(0);
        more.add(0);
        more.add(1);
        more.add(0);
        more.add("llama");
        assertEquals(value, StatUtils.sampleUniform(shortRange, more));

        assertThrows(Exception.class, () -> StatUtils.sampleUniform(shortRange, new ArrayList<>()));

        // Medium ranges
        int startRange = 20;
        int endRange = startRange + 15;
        ValueRange range1 = new ValueRange(startRange, startRange + 15);
        assertEquals(startRange, StatUtils.sampleUniform(range1, List.of(0, 0, 0, 0)));
        assertEquals(startRange + 1, StatUtils.sampleUniform(range1, List.of(0, 0, 0, 1)));
        assertEquals(endRange, StatUtils.sampleUniform(range1, List.of(1, 1, 1, 1)));

        // Test with generator-like
        List<Integer> zeros = new ArrayList<>();
        for (int i = 0; i < 10; i++) zeros.add(0);
        assertEquals(startRange, StatUtils.sampleUniform(range1, zeros));

        // Negative range
        startRange = -32;
        endRange = -17;
        ValueRange nr = new ValueRange(startRange, endRange);
        List<Integer> five0 = new ArrayList<>();
        List<Integer> five1 = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            five0.add(0);
            five1.add(1);
        }
        assertEquals(startRange, StatUtils.sampleUniform(nr, five0));
        assertEquals(endRange, StatUtils.sampleUniform(nr, five1));

        // Mixed range
        startRange = -32;
        endRange = 31;
        ValueRange mr = new ValueRange(startRange, endRange);
        List<Integer> six0 = new ArrayList<>();
        List<Integer> six1 = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            six0.add(0);
            six1.add(1);
        }
        assertEquals(startRange, StatUtils.sampleUniform(mr, six0));
        assertEquals(endRange, StatUtils.sampleUniform(mr, six1));
    }

    @Test
    void testHypergeometric() {
        // Infinite random coins
        Iterator<Integer> coins = new Iterator<>() {
            Random rand = new Random();
            public boolean hasNext() { return true; }
            public Integer next() { return rand.nextInt(2); }
        };
        assertEquals(0, HGD.rhyper(5, 0, 5, coins));
        assertEquals(6, HGD.rhyper(6, 6, 0, coins));

        assertEquals(0, HGD.rhyper((long) Math.pow(2, 32), 0, (long) Math.pow(2, 32), coins));
        assertEquals((long) Math.pow(2, 64), HGD.rhyper((long)Math.pow(2, 64), (long)Math.pow(2, 64), 0, coins));
        assertEquals(2, HGD.rhyper((long) Math.pow(2, 32), 2, (long) Math.pow(2, 32) - 2, coins));
    }
}