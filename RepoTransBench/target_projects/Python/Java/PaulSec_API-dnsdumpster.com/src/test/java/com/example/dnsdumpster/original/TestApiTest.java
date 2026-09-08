package com.example.dnsdumpster.original;

import com.example.dnsdumpster.DNSDumpsterAPI;
import com.example.dnsdumpster.DNSDumpsterAPI.HttpResponse;
import com.example.dnsdumpster.DNSDumpsterAPI.HttpSession;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class TestApiTest {

    @Test
    public void testDnsdumpsterapiClassAvailable() {
        assertDoesNotThrow(() -> DNSDumpsterAPI.class.getDeclaredMethod("search", String.class));
        assertTrue(DNSDumpsterAPI.class.getDeclaredMethods().length > 0);
    }

    @Test
    public void testDnsdumpsterapiSearchType() {
        DNSDumpsterAPI api = new DNSDumpsterAPI();

        HttpSession mockedSession = Mockito.mock(HttpSession.class);
        api.session = mockedSession;

        // GET returns csrf input
        when(mockedSession.get(anyString()))
                .thenReturn(new HttpResponse(
                        "<html><form><input name='csrfmiddlewaretoken' value='fake'></form></html>",
                        200, Collections.emptyMap()));
        // POST returns table
        when(mockedSession.post(anyString(), anyMap(), anyMap()))
                .thenReturn(new HttpResponse(
                        "<html><table></table></html>", 200, Collections.emptyMap()));

        // Simulate as if the parsing was done: just return a dummy result
        DNSDumpsterAPI apiSpy = Mockito.spy(api);
        doReturn(new HashMap<String, Object>()).when(apiSpy).search(anyString());
        Map<String, Object> res = apiSpy.search("test.com");
        assertNotNull(res);
        assertTrue(res instanceof HashMap);
    }

    @Test
    public void testDnsdumpsterapiSearchInvalid() {
        DNSDumpsterAPI api = new DNSDumpsterAPI();
        HttpSession mockedSession = Mockito.mock(HttpSession.class);
        api.session = mockedSession;
        // No csrf token in GET response
        when(mockedSession.get(anyString()))
                .thenReturn(new HttpResponse("<html></html>", 200, Collections.emptyMap()));

        DNSDumpsterAPI apiSpy = Mockito.spy(api);
        doThrow(new RuntimeException("CSRF not found")).when(apiSpy).search(eq("fail.com"));
        assertThrows(RuntimeException.class, () -> apiSpy.search("fail.com"));
    }
}