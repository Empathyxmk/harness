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

public class SsoApplicationTest {

    @Test
    public void testDashboardMessage() {
        SsoApplication app = new SsoApplication();
        Map<String, Object> message = app.dashboard();
        assertNotNull(message);
        assertEquals("Yay!", message.get("message"));
    }

    @Test
    public void testUserPrincipal() {
        SsoApplication app = new SsoApplication();
        Principal p = () -> "testuser";
        assertEquals(p, app.user(p));
        assertEquals("testuser", app.user(p).getName());
    }

    @Test
    public void testMainNoArgs() {
        // Just for coverage
        SsoApplication.main(new String[] {});
    }

    @Test
    public void testLoginErrorsDashboard() {
        SsoApplication.LoginErrors errors = new SsoApplication.LoginErrors();
        assertEquals("redirect:/#/", errors.dashboard());
    }

    @Test
    public void testCsrfHeaderFilterSetsCookie() throws Exception {
        SsoApplication.LoginConfigurer configurer = new SsoApplication.LoginConfigurer();
        FilterChain chain = mock(FilterChain.class);

        HttpServletRequest request = mock(HttpServletRequest.class);
        HttpServletResponse response = mock(HttpServletResponse.class);

        CsrfToken csrfToken = mock(CsrfToken.class);
        when(csrfToken.getToken()).thenReturn("testToken");
        when(request.getAttribute(CsrfToken.class.getName())).thenReturn(csrfToken);

        // call the private filter via reflection
        java.lang.reflect.Method m = SsoApplication.LoginConfigurer.class.getDeclaredMethod("csrfHeaderFilter");
        m.setAccessible(true);
        Object filterObj = m.invoke(configurer);
        assertNotNull(filterObj);

        javax.servlet.Filter filter = (javax.servlet.Filter) filterObj;
        filter.doFilter(request, response, chain);

        verify(response, times(1)).addCookie(any(Cookie.class));
        verify(chain, times(1)).doFilter(request, response);
    }

    @Test
    public void testCsrfHeaderFilterNoCsrf() throws Exception {
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
    public void testCsrfTokenRepository() throws Exception {
        SsoApplication.LoginConfigurer configurer = new SsoApplication.LoginConfigurer();
        java.lang.reflect.Method m = SsoApplication.LoginConfigurer.class.getDeclaredMethod("csrfTokenRepository");
        m.setAccessible(true);
        Object repository = m.invoke(configurer);
        assertNotNull(repository);
        assertEquals("X-XSRF-TOKEN", org.springframework.test.util.ReflectionTestUtils.getField(repository, "headerName"));
    }
}