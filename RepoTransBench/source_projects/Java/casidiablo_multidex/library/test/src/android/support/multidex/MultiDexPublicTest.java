package android.support.multidex;

import org.junit.Assert;
import org.junit.Test;

/**
 * Public test for {@link MultiDex} class with different VM version data.
 */
public class MultiDexPublicTest {
    @Test
    public void testVersionCheckPublic() {
        // Null and completely malformed
        Assert.assertFalse(MultiDex.isVMMultidexCapable("0.9"));
        Assert.assertFalse(MultiDex.isVMMultidexCapable("1.999.9999"));
        Assert.assertFalse(MultiDex.isVMMultidexCapable("2.0.0"));  // "2.0.0" should be false
        Assert.assertFalse(MultiDex.isVMMultidexCapable("2.0.1"));  // "2.0.x" should be false

        // True for >=2.1.x
        Assert.assertTrue(MultiDex.isVMMultidexCapable("2.10"));    // 2.10 > 2.1
        Assert.assertTrue(MultiDex.isVMMultidexCapable("2.1.1"));
        Assert.assertTrue(MultiDex.isVMMultidexCapable("4.0"));
        Assert.assertTrue(MultiDex.isVMMultidexCapable("10.2"));
        Assert.assertTrue(MultiDex.isVMMultidexCapable("2.1.1.5"));
        Assert.assertTrue(MultiDex.isVMMultidexCapable("2.2.12345"));
        Assert.assertTrue(MultiDex.isVMMultidexCapable("05.5.5"));

        // Edge, padded zeros
        Assert.assertTrue(MultiDex.isVMMultidexCapable("002.001.0001"));
        Assert.assertFalse(MultiDex.isVMMultidexCapable("2.0.9999"));
        Assert.assertFalse(MultiDex.isVMMultidexCapable("2.0.0000"));
        Assert.assertTrue(MultiDex.isVMMultidexCapable("3.0.42"));
    }
}