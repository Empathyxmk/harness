package jetbrick.template;

import org.junit.Assert;
import org.junit.Test;

public class JetEnginePublicTest {

    @Test
    public void testEngineCreateWithDifferentConfig() {
        JetConfig config = new JetConfig();
        config.setTemplateReloadable(false); // use different value from the likely default
        JetEngine engine = JetEngine.create(config);
        Assert.assertNotNull(engine);
    }

    @Test
    public void testDefaultContextAttributesAreEmptyWithDifferentKey() {
        JetEngine engine = JetEngine.create();
        // use unlikely key to avoid replicate
        Object value = engine.getGlobalContext().get("nonexistent_key_xyz");
        Assert.assertNull(value);
    }
}