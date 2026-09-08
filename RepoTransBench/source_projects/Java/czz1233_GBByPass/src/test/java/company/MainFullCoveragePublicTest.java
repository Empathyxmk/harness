package company;

import org.junit.Test;
import static org.junit.Assert.*;

public class MainFullCoveragePublicTest {
    @Test
    public void testReverseIfNotBlank_withNumbersAndLetters() {
        assertEquals("Ba98", Main.reverseIfNotBlank("89aB"));
    }
    @Test
    public void testReverseIfNotBlank_withSpecialCharacters() {
        assertEquals("!@#", Main.reverseIfNotBlank("#@!"));
    }
    @Test
    public void testIsAllDigits_withSpacesAndDigits() {
        assertFalse(Main.isAllDigits(" 789 "));
    }
    @Test
    public void testIsAllDigits_withDash() {
        assertFalse(Main.isAllDigits("123-456"));
    }
}