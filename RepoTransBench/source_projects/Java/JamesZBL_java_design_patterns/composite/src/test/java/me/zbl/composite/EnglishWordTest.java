package me.zbl.composite;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.util.Collections;

import static org.junit.jupiter.api.Assertions.*;

class EnglishWordTest {

    @Test
    void testConstructorAndPrintBefore() {
        Character c = new Character() {
            @Override
            public void print() { }
        };
        EnglishWord word = new EnglishWord(Collections.singletonList(c));
        assertEquals(1, word.count());
        // test printBefore() outputs a space
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        System.setOut(new PrintStream(out));
        word.printBefore();
        System.setOut(System.out);
        assertEquals(" ", out.toString());
    }
}