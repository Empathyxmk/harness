package com.example.dnsdumpster.original;

import com.example.dnsdumpster.DNSDumpsterAPI;
import com.example.dnsdumpster.DNSDumpsterAPI.HttpResponse;
import com.example.dnsdumpster.DNSDumpsterAPI.HttpSession;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class TestDNSDumpsterApiTest {

    private static class DummyResponse extends HttpResponse {
        public DummyResponse(String text) {
            super(text, 200, Collections.emptyMap());
        }
    }

    private String invalidHtml() {
        return "<html><body>No form here!</body></html>";
    }

    @Test
    public void testDnsdumpsterapiInit() {
        DNSDumpsterAPI api = new DNSDumpsterAPI();
        assertNotNull(api.session);
    }

    @Test
    public void testDnsdumpsterapiSearchUsage() {
        DNSDumpsterAPI api = new DNSDumpsterAPI();
        HttpSession mockSession = Mockito.mock(HttpSession.class);
        api.session = mockSession;

        when(mockSession.get(anyString()))
                .thenReturn(new DummyResponse("<html><form></form></html>"));

        when(mockSession.post(anyString(), anyMap(), anyMap()))
                .thenReturn(new DummyResponse("<html><table></table></html>"));

        DNSDumpsterAPI apiSpy = Mockito.spy(api);
        doReturn(new HashMap<String, Object>()).when(apiSpy).search(anyString());

        Map<String, Object> result = apiSpy.search("example.com");
        assertNotNull(result);
        assertTrue(result instanceof HashMap);
    }

    @Test
    public void testDnsdumpsterapiSearchNoCsrf() {
        DNSDumpsterAPI api = new DNSDumpsterAPI();
        HttpSession mockSession = Mockito.mock(HttpSession.class);
        api.session = mockSession;
        when(mockSession.get(anyString()))
                .thenReturn(new DummyResponse(invalidHtml()));

        DNSDumpsterAPI apiSpy = Mockito.spy(api);
        doThrow(new RuntimeException("CSRF not found")).when(apiSpy).search(anyString());
        assertThrows(RuntimeException.class, () -> apiSpy.search("example.com"));
    }

    @Test
    public void testDnsdumpsterapiFormParsing() {
        DNSDumpsterAPI api = new DNSDumpsterAPI();
        HttpSession mockSession = Mockito.mock(HttpSession.class);
        api.session = mockSession;

        String html = "<html>\n" +
                "<form>\n" +
                "  <input type=\"hidden\" name=\"csrfmiddlewaretoken\" value=\"12345\"/>\n" +
                "  <input type=\"text\" name=\"targetip\" value=\"example.com\"/>\n" +
                "</form>\n" +
                "</html>";
        when(mockSession.get(anyString()))
                .thenReturn(new DummyResponse(html));
        when(mockSession.post(anyString(), anyMap(), anyMap()))
                .thenReturn(new DummyResponse("<html><table></table></html>"));

        DNSDumpsterAPI apiSpy = Mockito.spy(api);
        doReturn(new HashMap<String, Object>()).when(apiSpy).search(anyString());
        assertDoesNotThrow(() -> apiSpy.search("example.com"));
    }
}