package com.peritus.bumpversion.publictests;

import com.peritus.bumpversion.functions.Functions;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class PublicFunctionsEdgeTest {

    @Test
    void testReplaceNumericPostfixOnlyNumber() {
        assertEquals("334", Functions.replaceNumericPostfix("667", 334));
    }

    @Test
    void testFirstNumericMatchIndexNoneNumber() {
        assertNull(Functions.firstNumericMatchIndex("qwerty"));
    }

    @Test
    void testFirstAlphaPostfixEdge() {
        assertEquals("", Functions.firstAlphaPostfix("123456"));
    }

    @Test
    void testFindFirstNumberComplexString() {
        assertEquals("2", Functions.findFirstNumber("xy_hello2abc5"));
    }

    @Test
    void testIncrementStringNumberOnlyNumber() {
        assertEquals("106", Functions.incrementStringNumber("105"));
    }

    @Test
    void testIncrementStringNumberWithZeros() {
        assertEquals("code008bond", Functions.incrementStringNumber("code007bond"));
    }
}