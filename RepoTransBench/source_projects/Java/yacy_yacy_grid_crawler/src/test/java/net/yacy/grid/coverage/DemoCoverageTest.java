package net.yacy.grid.coverage;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class DemoCoverageTest {

    @Test
    public void testAdd_PositiveNumbers() {
        DemoCoverage demo = new DemoCoverage();
        assertEquals(5, demo.add(2, 3));
    }

    @Test
    public void testAdd_NegativeNumbers() {
        DemoCoverage demo = new DemoCoverage();
        assertEquals(-5, demo.add(-2, -3));
    }

    @Test
    public void testIsEven_EvenNumber() {
        DemoCoverage demo = new DemoCoverage();
        assertTrue(demo.isEven(4));
    }

    @Test
    public void testIsEven_OddNumber() {
        DemoCoverage demo = new DemoCoverage();
        assertFalse(demo.isEven(5));
    }

    @Test
    public void testDivide_RegularCase() {
        DemoCoverage demo = new DemoCoverage();
        assertEquals(2, demo.divide(6, 3));
    }

    @Test
    public void testDivide_DivideByZero() {
        DemoCoverage demo = new DemoCoverage();
        Exception exception = assertThrows(ArithmeticException.class, () -> {
            demo.divide(10, 0);
        });
        assertEquals("/ by zero", exception.getMessage());
    }
}