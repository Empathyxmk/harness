package jetbrick.template.web.jfinal;

import com.jfinal.render.Render;
import org.junit.Test;
import static org.junit.Assert.*;

public class JetTemplateRenderFactoryTest {
    @Test
    public void testGetRender() {
        JetTemplateRenderFactory factory = new JetTemplateRenderFactory();
        Render render = factory.getRender("test.jetx");
        assertNotNull(render);
        assertTrue(render instanceof JetTemplateRender);
    }
}