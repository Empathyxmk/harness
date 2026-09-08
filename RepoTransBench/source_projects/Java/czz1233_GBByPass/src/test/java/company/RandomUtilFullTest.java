package company;

import org.junit.Test;
import static org.junit.Assert.*;

public class RandomUtilFullTest {

    @Test
    public void testRandomStringWithZeroLength() {
        String result = RandomUtil.randomString(0);
        assertNotNull(result);
        assertEquals(0, result.length());
    }

    @Test
    public void testRandomStringWithNegativeLength() {
        String result = RandomUtil.randomString(-1);
        assertNotNull(result);
        assertEquals(0, result.length());
    }

    @Test
    public void testRandomStringWithHighLength() {
        String result = RandomUtil.randomString(100);
        assertNotNull(result);
        assertEquals(100, result.length());
    }

    @Test
    public void testRandomStringIsAlphanumeric() {
        String result = RandomUtil.randomString(20);
        assertTrue(result.matches("[A-Za-z0-9]+") || result.isEmpty());
    }

    // The following methods are commented out
    // because isAllDigits and reverse are not found in RandomUtil (based on build errors)
    /*
    @Test
    public void testIsAllDigitsTrue() {
        assertTrue(RandomUtil.isAllDigits("1234567890"));
    }

    @Test
    public void testIsAllDigitsFalseAlpha() {
        assertFalse(RandomUtil.isAllDigits("1234abc"));
    }

    @Test
    public void testIsAllDigitsFalseEmpty() {
        assertFalse(RandomUtil.isAllDigits(""));
    }

    @Test
    public void testReverseNull() {
        assertEquals("", RandomUtil.reverse(null));
    }

    @Test
    public void testReverseEmpty() {
        assertEquals("", RandomUtil.reverse(""));
    }

    @Test
    public void testReverseString() {
        assertEquals("cba", RandomUtil.reverse("abc"));
    }

    @Test
    public void testReversePalindrome() {
        assertEquals("madam", RandomUtil.reverse("madam"));
    }
    */
}