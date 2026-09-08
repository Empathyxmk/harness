package guru.springframework.spring5webapp;

import org.junit.Test;
import static org.junit.Assert.*;

public class SampleBranchingServiceTest {

    private final SampleBranchingService service = new SampleBranchingService();

    @Test
    public void testCategorizeNegative() {
        assertEquals("negative", service.categorizeNumber(-5));
    }

    @Test
    public void testCategorizeZero() {
        assertEquals("zero", service.categorizeNumber(0));
    }

    @Test
    public void testCategorizeSmall() {
        assertEquals("small", service.categorizeNumber(5));
    }

    @Test
    public void testCategorizeLarge() {
        assertEquals("large", service.categorizeNumber(100));
    }

    @Test
    public void testIsEvenTrue() {
        assertTrue(service.isEven(2));
    }

    @Test
    public void testIsEvenFalse() {
        assertFalse(service.isEven(3));
    }
}