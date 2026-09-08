package me.zbl.composite;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.Collections;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

class ChineseWordTest {

    @Test
    void testConstructorAndPrintBefore() {
        Character c = new Character() {
            @Override
            public void print() {}
        };
        ChineseWord word = new ChineseWord(Collections.singletonList(c));
        assertEquals(1, word.count());
        // test printBefore() outputs ""
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        System.setOut(new PrintStream(out));
        word.printBefore();
        System.setOut(System.out);
        assertEquals("", out.toString());
    }
}