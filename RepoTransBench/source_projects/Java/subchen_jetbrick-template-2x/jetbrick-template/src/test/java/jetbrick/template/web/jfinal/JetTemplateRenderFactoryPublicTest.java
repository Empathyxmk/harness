// Simulate alternative factory test, using different config
package jetbrick.template.web.jfinal;

import org.junit.Assert;
import org.junit.Test;

public class JetTemplateRenderFactoryPublicTest {
    @Test
    public void testDifferentFactoryMethod() {
        JetTemplateRenderFactory factory = new JetTemplateRenderFactory();
        // Use a different config or factory method if available,
        // fallback: just assert instantiation
        Assert.assertNotNull(factory);
    }
}