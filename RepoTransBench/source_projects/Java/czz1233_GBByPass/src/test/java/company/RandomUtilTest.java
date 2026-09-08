package company;

import org.junit.Test;
import static org.junit.Assert.*;

public class RandomUtilTest {

    @Test
    public void testRandomString_Length() {
        assertEquals(8, RandomUtil.randomString(8).length());
        assertEquals(1, RandomUtil.randomString(1).length());
        assertEquals(32, RandomUtil.randomString(32).length());
    }
    @Test
    public void testRandomString_Characters() {
        String str = RandomUtil.randomString(100);
        assertTrue(str.matches("[A-Za-z0-9]{100}"));
    }
    @Test
    public void testRandomString_ZeroAndNegativeLength() {
        assertEquals("", RandomUtil.randomString(0));
        assertEquals("", RandomUtil.randomString(-5));
    }
}