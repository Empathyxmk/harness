package me.zbl.composite;

import org.junit.jupiter.api.Test;

import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.*;

class EnglishWordPublicTest {

    @Test
    void testConstructionAndPrintBeforeOtherValue() {
        CharacterComposite word = new EnglishWord(Arrays.asList(
                new Character('P'), new Character('u'), new Character('b'), new Character('l'), new Character('i'), new Character('c')
        ));
        assertEquals(6, word.count());
        // The printBefore adds a space -- test that
        word.printBefore();
        // The method does not output the text, this is just a branch check
    }
}