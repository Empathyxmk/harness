package jetbrick.template;

import org.junit.Assert;
import org.junit.Test;
import java.util.Properties;
import jetbrick.io.resource.ResourceNotFoundException;

public class JetEngineTest {

    @Test
    public void testCreateDefaults() {
        JetEngine engine1 = JetEngine.create();
        Assert.assertNotNull(engine1);
        JetEngine engine2 = JetEngine.create(new Properties());
        Assert.assertNotNull(engine2);
        JetEngine engine3 = JetEngine.create("jetbrick-template.properties");
        Assert.assertNotNull(engine3);
        JetEngine engine4 = JetEngine.create(new Properties(), "jetbrick-template.properties");
        Assert.assertNotNull(engine4);
    }

    @Test
    public void testAbstractMethods() {
        JetEngine engine = JetEngine.create();
        Assert.assertNotNull(engine.getConfig());
        Assert.assertNotNull(engine.getGlobalContext());
        Assert.assertNotNull(engine.getGlobalResolver());
    }

    @Test
    public void testCheckTemplateAndResourceException() {
        JetEngine engine = JetEngine.create();
        Assert.assertFalse(engine.checkTemplate("not_existing_template.jetx"));

        try {
            engine.getTemplate("not_existing_template.jetx");
            Assert.fail("Should have thrown ResourceNotFoundException");
        } catch (ResourceNotFoundException e) {
            // expected
        }

        try {
            engine.getResource("not_existing_resource.txt");
            Assert.fail("Should have thrown ResourceNotFoundException");
        } catch (Exception e) {
            // expected
        }
    }

    @Test
    public void testCreateTemplateFromSource() {
        JetEngine engine = JetEngine.create();
        JetTemplate template = engine.createTemplate("${1+1}");
        Assert.assertNotNull(template);

        JetTemplate template2 = engine.createTemplate("test_id", "${2+2}");
        Assert.assertNotNull(template2);
    }
}