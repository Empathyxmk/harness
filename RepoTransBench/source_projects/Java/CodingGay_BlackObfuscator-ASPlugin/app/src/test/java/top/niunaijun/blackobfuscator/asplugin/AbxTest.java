package top.niunaijun.blackobfuscator.asplugin;

import org.junit.Test;
import static org.junit.Assert.*;

public class AbxTest {
    @Test
    public void testGoAlwaysTrue() {
        // System.currentTimeMillis() > 0 should always be true
        assertTrue(Abx.go());
    }
}