package guru.springframework.spring5webapp;

import org.junit.Test;
import static org.junit.Assert.*;

public class SampleBranchingServicePublicTest {

    private final SampleBranchingService service = new SampleBranchingService();

    @Test
    public void testCategorizeNegativePublic() {
        assertEquals("negative", service.categorizeNumber(-15));
    }

    @Test
    public void testCategorizeZeroPublic() {
        assertEquals("zero", service.categorizeNumber(0));
    }

    @Test
    public void testCategorizeSmallPublic() {
        assertEquals("small", service.categorizeNumber(8));
    }

    @Test
    public void testCategorizeLargePublic() {
        assertEquals("large", service.categorizeNumber(50));
    }

    @Test
    public void testIsEvenTruePublic() {
        assertTrue(service.isEven(6));
    }

    @Test
    public void testIsEvenFalsePublic() {
        assertFalse(service.isEven(9));
    }
}