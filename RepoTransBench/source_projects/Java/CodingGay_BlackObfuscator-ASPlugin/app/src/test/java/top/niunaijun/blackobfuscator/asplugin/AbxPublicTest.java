package top.niunaijun.blackobfuscator.asplugin;

import org.junit.Test;
import static org.junit.Assert.*;

public class AbxPublicTest {

    @Test
    public void testAddDifferentValues() {
        // Suppose existing test uses (2, 3)
        assertEquals(13, Abx.add(7, 6));
        assertEquals(0, Abx.add(-3, 3));
    }

    @Test
    public void testIsPositiveDifferentData() {
        // Suppose existing test uses 1 and -1
        assertTrue(Abx.isPositive(2024));
        assertFalse(Abx.isPositive(-2025));
    }
}