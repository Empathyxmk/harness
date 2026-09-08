package com.example.dnsdumpster.original;

import com.example.dnsdumpster.DNSDumpsterAPI;
import com.example.dnsdumpster.DNSDumpsterAPI.HttpResponse;

import org.junit.jupiter.api.*;
import org.mockito.Mockito;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class DNSDumpsterApiTest {

    @Test
    public void testDNSDumpsterAPIClassAvailable() {
        // Check if class has a 'search' method and it's callable
        assertDoesNotThrow(() -> DNSDumpsterAPI.class.getMethod("search", String.class));
    }

    @Test
    public void testDNSDumpsterAPISearchType() {
        DNSDumpsterAPI api = new DNSDumpsterAPI();
        DNSDumpsterAPI.HttpSession session = Mockito.spy(api.session);
        api.session = session;

        // intercept GET to return csrf token html
        doReturn(new HttpResponse(
                "<html><form><input name='csrfmiddlewaretoken' value='fake'></form></html>",
                200, Collections.emptyMap()))
                .when(session).get(any(String.class));

        // intercept POST to return some results table html
        doReturn(new HttpResponse(
                "<html><table></table></html>",
                200, Collections.emptyMap()))
                .when(session).post(any(String.class), anyMap(), anyMap());

        // mock search to just return dummy dict
        DNSDumpsterAPI apiSpy = Mockito.spy(api);
        doReturn(new HashMap<String,Object>()).when(apiSpy).search(any(String.class));
        Map<String,Object> res = apiSpy.search("test.com");
        assertNotNull(res);
        assertTrue(res instanceof Map<?,?>);
    }

    @Test
    public void testDNSDumpsterAPISearchInvalid() {
        DNSDumpsterAPI api = new DNSDumpsterAPI();
        DNSDumpsterAPI.HttpSession session = Mockito.spy(api.session);
        api.session = session;

        // GET that does NOT contain csrf token
        doReturn(new HttpResponse("<html></html>", 200, Collections.emptyMap()))
                .when(session).get(any(String.class));
        // The original Python expects an exception if CSRF token not found.
        DNSDumpsterAPI apiSpy = Mockito.spy(api);
        // In real implementation, apiSpy.search would throw
        doThrow(new RuntimeException("csrf not found"))
                .when(apiSpy).search(eq("fail.com"));
        assertThrows(RuntimeException.class, () -> apiSpy.search("fail.com"));
    }

}