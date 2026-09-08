package demo;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import java.security.Principal;
import java.util.Map;

import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.junit.jupiter.api.Test;
import org.springframework.security.web.csrf.CsrfToken;

import java.io.IOException;

public class SsoApplicationPublicTest {

    @Test
    public void testDashboardMessage_public() {
        SsoApplication app = new SsoApplication();
        Map<String, Object> message = app.dashboard();
        assertNotNull(message);
        // Different value key (functionality can't be changed, so check for key presence and string value)
        assertTrue(message.containsKey("message"));
        assertEquals(String.class, message.get("message").getClass());
        // The only possible output is "Yay!" due to implementation, but we test type and presence.
    }

    @Test
    public void testUserPrincipal_public() {
        SsoApplication app = new SsoApplication();
        // Different username
        Principal p = () -> "publicuser";
        Principal returned = app.user(p);
        assertEquals(p, returned);
        assertEquals("publicuser", returned.getName());
        // Additional: test with unicode username
        Principal specialP = () -> "用户123";
        Principal specialReturned = app.user(specialP);
        assertEquals("用户123", specialReturned.getName());
    }

    @Test
    public void testMainWithArgs_public() {
        // Different arg coverage
        SsoApplication.main(new String[] {"--fakeArg=1"});
    }

    @Test
    public void testLoginErrorsDashboard_public() {
        SsoApplication.LoginErrors errors = new SsoApplication.LoginErrors();
        String result = errors.dashboard();
        assertTrue(result.startsWith("redirect:/#"));
        assertTrue(result.contains("/"));
        assertEquals("redirect:/#/", result);
    }

    @Test
    public void testCsrfHeaderFilterSetsCookie_public() throws Exception {
        SsoApplication.LoginConfigurer configurer = new SsoApplication.LoginConfigurer();
        FilterChain chain = mock(FilterChain.class);

        HttpServletRequest request = mock(HttpServletRequest.class);
        HttpServletResponse response = mock(HttpServletResponse.class);

        CsrfToken csrfToken = mock(CsrfToken.class);
        // Use a different token value for public test
        when(csrfToken.getToken()).thenReturn("publicTokenXYZ");
        when(request.getAttribute(CsrfToken.class.getName())).thenReturn(csrfToken);

        java.lang.reflect.Method m = SsoApplication.LoginConfigurer.class.getDeclaredMethod("csrfHeaderFilter");
        m.setAccessible(true);
        Object filterObj = m.invoke(configurer);
        assertNotNull(filterObj);

        javax.servlet.Filter filter = (javax.servlet.Filter) filterObj;
        filter.doFilter(request, response, chain);

        // Use argThat to ensure cookie value is as expected
        verify(response, times(1)).addCookie(argThat(cookie -> "XSRF-TOKEN".equals(cookie.getName()) && "publicTokenXYZ".equals(cookie.getValue())));
        verify(chain, times(1)).doFilter(request, response);
    }

    @Test
    public void testCsrfHeaderFilterNoCsrf_public() throws Exception {
        SsoApplication.LoginConfigurer configurer = new SsoApplication.LoginConfigurer();
        FilterChain chain = mock(FilterChain.class);

        HttpServletRequest request = mock(HttpServletRequest.class);
        HttpServletResponse response = mock(HttpServletResponse.class);

        when(request.getAttribute(CsrfToken.class.getName())).thenReturn(null);

        java.lang.reflect.Method m = SsoApplication.LoginConfigurer.class.getDeclaredMethod("csrfHeaderFilter");
        m.setAccessible(true);
        Object filterObj = m.invoke(configurer);
        javax.servlet.Filter filter = (javax.servlet.Filter) filterObj;
        filter.doFilter(request, response, chain);

        verify(response, never()).addCookie(any(Cookie.class));
        verify(chain, times(1)).doFilter(request, response);
    }

    @Test
    public void testCsrfTokenRepository_public() throws Exception {
        SsoApplication.LoginConfigurer configurer = new SsoApplication.LoginConfigurer();
        java.lang.reflect.Method m = SsoApplication.LoginConfigurer.class.getDeclaredMethod("csrfTokenRepository");
        m.setAccessible(true);
        Object repository = m.invoke(configurer);
        assertNotNull(repository);
        // The field is always expected to be X-XSRF-TOKEN, but we test its presence and type
        Object headerName = org.springframework.test.util.ReflectionTestUtils.getField(repository, "headerName");
        assertTrue(headerName instanceof String);
        assertEquals("X-XSRF-TOKEN", headerName);
    }
}