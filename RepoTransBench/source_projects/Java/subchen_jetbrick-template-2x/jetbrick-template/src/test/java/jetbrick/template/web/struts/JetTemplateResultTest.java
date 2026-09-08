package jetbrick.template.web.struts;

import org.junit.Test;
import org.junit.Before;
import static org.mockito.Mockito.*;
import javax.servlet.ServletContext;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.HashMap;
import java.util.Map;
import java.io.OutputStream;

import jetbrick.template.JetEngine;
import jetbrick.template.JetTemplate;
import jetbrick.template.web.JetWebContext;
import jetbrick.template.web.JetWebEngine;

import org.apache.struts2.ServletActionContext;
import org.apache.struts2.dispatcher.StrutsResultSupport;
import com.opensymphony.xwork2.ActionInvocation;
import com.opensymphony.xwork2.util.ValueStack;

// Note: This is a simplistic mock-based test. In CI with Struts2, more complex setup might be needed.
public class JetTemplateResultTest {

    @Test
    public void testDoExecute_withEngine() throws Exception {
        JetTemplateResult result = new JetTemplateResult();

        Map<String,Object> model = new HashMap<>();
        HttpServletRequest request = mock(HttpServletRequest.class);
        HttpServletResponse response = mock(HttpServletResponse.class);
        OutputStream outputStream = mock(OutputStream.class);
        when(response.getContentType()).thenReturn(null);
        when(response.getOutputStream()).thenReturn(outputStream);

        JetEngine engine = mock(JetEngine.class);
        JetTemplate template = mock(JetTemplate.class);
        when(engine.getConfig()).thenReturn(new MockConfig());
        when(engine.getTemplate(anyString())).thenReturn(template);

        JetWebEngine.setEngine(engine);

        model.put(ServletActionContext.HTTP_REQUEST, request);
        model.put(ServletActionContext.HTTP_RESPONSE, response);

        ActionInvocation ai = mock(ActionInvocation.class);
        ValueStack vs = mock(ValueStack.class);

        when(ai.getStack()).thenReturn(vs);
        when(ai.getAction()).thenReturn(new Object());
        when(vs.getContext()).thenReturn(model);

        result.doExecute("template.jetx", ai);

        verify(response).setCharacterEncoding(anyString());
        verify(response).setContentType(anyString());
        verify(template).render(any(JetWebContext.class), eq(outputStream));

        JetWebEngine.setEngine(null); // cleanup
    }

    @Test
    public void testDoExecute_withoutEngineCreates() throws Exception {
        JetTemplateResult result = new JetTemplateResult();

        Map<String,Object> model = new HashMap<>();
        HttpServletRequest request = mock(HttpServletRequest.class);
        HttpServletResponse response = mock(HttpServletResponse.class);
        OutputStream outputStream = mock(OutputStream.class);
        when(response.getContentType()).thenReturn("a/b");
        when(response.getOutputStream()).thenReturn(outputStream);

        ServletContext servletContext = mock(ServletContext.class);

        model.put(ServletActionContext.HTTP_REQUEST, request);
        model.put(ServletActionContext.HTTP_RESPONSE, response);
        model.put(ServletActionContext.SERVLET_CONTEXT, servletContext);

        ActionInvocation ai = mock(ActionInvocation.class);
        ValueStack vs = mock(ValueStack.class);

        when(ai.getStack()).thenReturn(vs);
        when(ai.getAction()).thenReturn(new Object());
        when(vs.getContext()).thenReturn(model);

        JetWebEngine.setEngine(null);

        // override JetWebEngine.create to return a mocked JetEngine
        JetEngine engine = mock(JetEngine.class);
        JetTemplate template = mock(JetTemplate.class);
        when(engine.getConfig()).thenReturn(new MockConfig());
        when(engine.getTemplate(anyString())).thenReturn(template);

        JetWebEngine.setMockEngineForTest(engine);

        result.doExecute("template.jetx", ai);

        verify(response).setCharacterEncoding(anyString());
        verify(response, never()).setContentType(anyString());
        verify(template).render(any(JetWebContext.class), eq(outputStream));

        JetWebEngine.setMockEngineForTest(null); // cleanup
    }

    private static class MockConfig extends jetbrick.template.JetConfig {
        public MockConfig() { super(null, null); }
        @Override
        public java.nio.charset.Charset getOutputEncoding() { return java.nio.charset.StandardCharsets.UTF_8; }
    }
}