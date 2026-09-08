package company;

import org.junit.Test;

import static org.junit.Assert.*;

public class RandomUtilBranchCoverageTest {
    @Test
    public void testRandomString_lengthOne() {
        String s = RandomUtil.randomString(1);
        assertNotNull(s);
        assertEquals(1, s.length());
        assertTrue(s.matches("[A-Za-z0-9]"));
    }

    @Test
    public void testRandomString_largeLength() {
        String s = RandomUtil.randomString(1000);
        assertNotNull(s);
        assertEquals(1000, s.length());
        assertTrue(s.matches("[A-Za-z0-9]{1000}"));
    }
}