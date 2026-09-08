package jetbrick.template.web.struts;

import org.junit.Assert;
import org.junit.Test;

public class JetTemplateResultPublicTest {

    @Test
    public void testEvaluateTemplateNameWithDifferentExtension() {
        // Different extension than likely in default
        JetTemplateResult result = new JetTemplateResult();
        String tname = "file.template";
        String evaluated = result.evaluateTemplateName(tname);
        Assert.assertNotNull(evaluated);
        Assert.assertTrue(evaluated.endsWith(".template"));
    }
}