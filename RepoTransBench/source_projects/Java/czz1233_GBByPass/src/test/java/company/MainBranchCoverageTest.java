package company;

import org.junit.Test;

import static org.junit.Assert.*;

public class MainBranchCoverageTest {
    @Test
    public void testReverseIfNotBlank_nullInput() {
        // Check how method handles null input; StringUtils.isBlank(null)==true
        assertNull(Main.reverseIfNotBlank(null));
    }

    @Test
    public void testIsAllDigits_nullInput() {
        // Should return false, as per StringUtils.isBlank(null)
        assertFalse(Main.isAllDigits(null));
    }
}