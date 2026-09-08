package company;

import org.junit.Test;

import static org.junit.Assert.*;

public class RandomUtilBranchCoveragePublicTest {
    @Test
    public void testRandomString_lengthTwo() {
        String s = RandomUtil.randomString(2);
        assertNotNull(s);
        assertEquals(2, s.length());
        assertTrue(s.matches("[A-Za-z0-9]{2}"));
    }

    @Test
    public void testRandomString_mediumLength() {
        String s = RandomUtil.randomString(50);
        assertNotNull(s);
        assertEquals(50, s.length());
        assertTrue(s.matches("[A-Za-z0-9]{50}"));
    }
}