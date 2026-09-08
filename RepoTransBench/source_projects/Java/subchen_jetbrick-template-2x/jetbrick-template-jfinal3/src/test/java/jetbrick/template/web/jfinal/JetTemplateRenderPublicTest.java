package jetbrick.template.web.jfinal;

import com.jfinal.render.Render;
import jetbrick.template.JetEngine;
import jetbrick.template.JetTemplate;
import jetbrick.template.web.JetWebContext;
import jetbrick.template.web.JetWebEngine;
import org.junit.Test;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import static org.mockito.Mockito.*;

import java.io.OutputStream;

public class JetTemplateRenderPublicTest {

    @Test
    public void testRender_Normal() {
        JetEngine engine = mock(JetEngine.class);
        JetTemplate template = mock(JetTemplate.class);
        when(engine.getConfig()).thenReturn(new MockConfig());
        when(engine.getTemplate(anyString())).thenReturn(template);
        JetWebEngine.setEngine(engine);

        JetTemplateRender render = new JetTemplateRender("public.jetx");

        // mock some static fields
        render.request = mock(HttpServletRequest.class);
        render.response = mock(HttpServletResponse.class);
        when(render.response.getContentType()).thenReturn(null);
        try {
            OutputStream out = mock(OutputStream.class);
            when(render.response.getOutputStream()).thenReturn(out);
            render.render();
            verify(render.response).setCharacterEncoding(anyString());
            verify(render.response).setContentType(anyString());
            verify(template).render(any(JetWebContext.class), eq(out));
        } catch (Exception e) {
            throw new RuntimeException(e);
        }

        JetWebEngine.setEngine(null);
    }

    @Test(expected = IllegalStateException.class)
    public void testRender_IOException() throws Exception {
        JetEngine engine = mock(JetEngine.class);
        JetTemplate template = mock(JetTemplate.class);
        when(engine.getConfig()).thenReturn(new MockConfig());
        when(engine.getTemplate(anyString())).thenReturn(template);
        JetWebEngine.setEngine(engine);

        JetTemplateRender render = new JetTemplateRender("ioerror.jetx");

        render.request = mock(HttpServletRequest.class);
        render.response = mock(HttpServletResponse.class);
        when(render.response.getContentType()).thenReturn(null);

        OutputStream out = mock(OutputStream.class);
        when(render.response.getOutputStream()).thenThrow(new java.io.IOException("public fail"));

        render.render();

        JetWebEngine.setEngine(null);
    }

    // Minimal mock config
    static class MockConfig extends jetbrick.template.JetConfig {
        public MockConfig() {super(null, null);}
        @Override public java.nio.charset.Charset getOutputEncoding() {return java.nio.charset.StandardCharsets.UTF_16;}
        @Override public String getTemplateSuffix() {return ".pub";}
    }
}