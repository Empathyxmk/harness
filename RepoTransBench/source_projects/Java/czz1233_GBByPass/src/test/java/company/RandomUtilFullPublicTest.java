package company;

import org.junit.Test;
import static org.junit.Assert.*;

public class RandomUtilFullPublicTest {
    @Test
    public void testRandomString_negativeLength() {
        String val = RandomUtil.randomString(-7);
        assertEquals("", val);
    }
    @Test
    public void testRandomString_allValidCharactersMany() {
        String val = RandomUtil.randomString(32);
        assertNotNull(val);
        assertEquals(32, val.length());
        assertTrue(val.matches("[A-Za-z0-9]{32}"));
    }
}