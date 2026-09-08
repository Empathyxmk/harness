package com.peritus.bumpversion.publictests;

import com.peritus.bumpversion.functions.Functions;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class PublicFunctionsTest {

    @Test
    void testReplaceNumericPostfixDifferentNumber() {
        assertEquals("abc44xyz", Functions.replaceNumericPostfix("abc22xyz", 44));
    }

    @Test
    void testReplaceNumericPostfixNoDigits() {
        assertEquals("no_digits_here", Functions.replaceNumericPostfix("no_digits_here", 9000));
    }

    @Test
    void testFirstNumericMatchIndexNew() {
        assertArrayEquals(new int[]{6, 9}, Functions.firstNumericMatchIndex("prefix007suffix"));
    }

    @Test
    void testFirstNumericMatchIndexLeadingNumber() {
        assertArrayEquals(new int[]{0, 2}, Functions.firstNumericMatchIndex("99redballoons"));
    }

    @Test
    void testFirstAlphaPostfix() {
        assertEquals("z", Functions.firstAlphaPostfix("xy3z"));
    }

    @Test
    void testFindFirstNumberCustom_ABC9() {
        assertEquals("9", Functions.findFirstNumber("ABC9"));
    }

    @Test
    void testFindFirstNumberCustom_a1b2c3() {
        assertEquals("1", Functions.findFirstNumber("a1b2c3"));
    }

    @Test
    void testFindFirstNumberCustom_noDigits() {
        assertEquals("", Functions.findFirstNumber("no_digits"));
    }

    @Test
    void testIncrementStringNumberVariant() {
        assertEquals("hello110world", Functions.incrementStringNumber("hello109world"));
    }
}