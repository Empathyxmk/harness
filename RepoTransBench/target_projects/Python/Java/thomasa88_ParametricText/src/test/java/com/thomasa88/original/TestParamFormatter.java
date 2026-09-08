package com.thomasa88.original;

import com.thomasa88.DummyParam;
import com.thomasa88.DummyDesign;
import com.thomasa88.ParamFormatter;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class TestParamFormatter {

    private DummyDesign design;

    @BeforeEach
    void setUp() {
        design = new DummyDesign();
    }

    @Test
    void testUnitlessPositive() {
        DummyParam p = new DummyParam(1.75, "");
        assertEquals("1 3/4\"", ParamFormatter.mixedFracInch(p, design));
    }

    @Test
    void testUnitlessNegative() {
        DummyParam p = new DummyParam(-2.5, "");
        assertEquals("-2 1/2\"", ParamFormatter.mixedFracInch(p, design));
    }

    @Test
    void testUnitInch() {
        DummyParam p = new DummyParam(2.5, "in");
        assertEquals("2 1/2\"", ParamFormatter.mixedFracInch(p, design));
    }

    @Test
    void testWholeNumber() {
        DummyParam p = new DummyParam(3.0, "");
        assertEquals("3\"", ParamFormatter.mixedFracInch(p, design));
        DummyParam p2 = new DummyParam(0.0, "");
        assertEquals("0\"", ParamFormatter.mixedFracInch(p2, design));
    }

    @Test
    void testFractionOnly() {
        DummyParam p = new DummyParam(0.25, "");
        assertEquals("1/4\"", ParamFormatter.mixedFracInch(p, design));
        DummyParam p2 = new DummyParam(-0.75, "");
        assertEquals("-3/4\"", ParamFormatter.mixedFracInch(p2, design));
    }

    @Test
    void testZero() {
        DummyParam p = new DummyParam(0, "");
        assertEquals("0\"", ParamFormatter.mixedFracInch(p, design));
    }
}