package jetbrick.template.exec;

import org.junit.Assert;
import org.junit.Test;

public class AbstractJetxPublicTest {

    @Test
    public void testNullSafeEqualsWithDifferentObjects() {
        Assert.assertTrue(AbstractJetxTest.nullSafeEquals("abc", "abc"));
        Assert.assertFalse(AbstractJetxTest.nullSafeEquals("abc", "xyz"));
    }

    @Test
    public void testNullSafeEqualsWithNullsAndDifferentValues() {
        Assert.assertFalse(AbstractJetxTest.nullSafeEquals(null, "notnull"));
        Assert.assertTrue(AbstractJetxTest.nullSafeEquals(null, null));
    }
}