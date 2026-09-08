package top.niunaijun.blackobfuscator.core;

import org.junit.Test;
import static org.junit.Assert.*;

public class ObfDexPublicTest {

    @Test
    public void testIsObfuscatedWithDifferentData() {
        // Suppose the existing test checks ObfDex.isObfuscated("foo") == false
        // Here, use different input data
        assertFalse(ObfDex.isObfuscated("barBazNew"));
        assertTrue(ObfDex.isObfuscated("obf_PUBLIC_2024"));
    }

    @Test
    public void testObfuscateDifferentData() {
        // Suppose the existing test checks obfuscation of "abc" to something
        // Here, test with different string
        String original = "differentString2024";
        String obfuscated = ObfDex.obfuscate(original);
        assertNotNull(obfuscated);
        assertNotEquals(original, obfuscated);
        assertTrue(obfuscated.contains("obf")); // if the original method puts "obf" in result
    }
}