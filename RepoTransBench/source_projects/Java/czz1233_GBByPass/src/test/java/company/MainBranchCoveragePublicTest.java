package company;

import org.junit.Test;

import static org.junit.Assert.*;

public class MainBranchCoveragePublicTest {
    @Test
    public void testReverseIfNotBlank_emptyStringInput() {
        // Instead of null, use empty string (also blank)
        assertEquals("", Main.reverseIfNotBlank(""));
    }

    @Test
    public void testIsAllDigits_emptyStringInput() {
        assertFalse(Main.isAllDigits(""));
    }
}