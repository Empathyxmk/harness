package top.niunaijun.blackobfuscator.asplugin;

import org.junit.Test;
import static org.junit.Assert.*;

public class MainActivityPublicTest {

    @Test
    public void testGetWelcomeMessageWithDifferentUser() {
        // Suppose MainActivity.getWelcomeMessage("Alice") returns something like "Welcome, Alice!"
        assertEquals("Welcome, Charlie!", MainActivity.getWelcomeMessage("Charlie"));
        assertEquals("Welcome, Zoe!", MainActivity.getWelcomeMessage("Zoe"));
    }
}