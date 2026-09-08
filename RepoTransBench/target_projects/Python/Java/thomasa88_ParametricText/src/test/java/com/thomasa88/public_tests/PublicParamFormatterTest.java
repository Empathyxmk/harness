package com.thomasa88.public_tests;

import com.thomasa88.ParamFormatter;
import com.thomasa88.DummyParam;
import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

public class PublicParamFormatterTest {

    private static DummyParam makeParam(double val, String unit) {
        return new DummyParam(val, unit);
    }
    private static DummyParam makeParam(double val) {
        return new DummyParam(val, "");
    }

    @Test
    void testMixedFracInchWholeNumber() {
        DummyParam p = makeParam(15);
        assertEquals("15\"", ParamFormatter.mixedFracInch(p, null));
    }
    @Test
    void testMixedFracInchSimpleFraction() {
        DummyParam p = makeParam(0.625);
        assertEquals("5/8\"", ParamFormatter.mixedFracInch(p, null));
    }
    @Test
    void testMixedFracInchMixed() {
        DummyParam p = makeParam(3.75);
        assertEquals("3 3/4\"", ParamFormatter.mixedFracInch(p, null));
    }
    @Test
    void testMixedFracInchExactHalf() {
        DummyParam p = makeParam(6.5);
        assertEquals("6 1/2\"", ParamFormatter.mixedFracInch(p, null));
    }
    @Test
    void testMixedFracInchZero() {
        DummyParam p = makeParam(0);
        assertEquals("0\"", ParamFormatter.mixedFracInch(p, null));
    }
}