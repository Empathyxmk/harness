package company;

import org.junit.Test;
import static org.junit.Assert.*;

public class RandomUtilPublicTest {
    @Test
    public void testRandomString_typicalLength() {
        String s = RandomUtil.randomString(5);
        assertNotNull(s);
        assertEquals(5, s.length());
        assertTrue(s.matches("[A-Za-z0-9]{5}"));
    }

    @Test
    public void testRandomString_zeroLength() {
        String s = RandomUtil.randomString(0);
        assertNotNull(s);
        assertEquals(0, s.length());
        assertEquals("", s);
    }
}