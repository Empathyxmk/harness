// Test a different template name, such as "another.html" instead of "index.html"
package jetbrick.template.web.jfinal;

import org.junit.Assert;
import org.junit.Test;

public class JetTemplateRenderPublicTest {
    @Test
    public void testDifferentTemplateRenderName() {
        JetTemplateRender renderer = new JetTemplateRender("another.html");
        Assert.assertEquals("another.html", renderer.getView());
    }
}