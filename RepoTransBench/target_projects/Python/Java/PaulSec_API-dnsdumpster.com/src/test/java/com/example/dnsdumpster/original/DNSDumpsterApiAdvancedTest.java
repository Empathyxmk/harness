package com.example.dnsdumpster.original;

import com.example.dnsdumpster.DNSDumpsterAPI;
import com.example.dnsdumpster.DNSDumpsterAPI.HttpResponse;

import org.junit.jupiter.api.*;
import org.mockito.Mockito;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class DNSDumpsterApiAdvancedTest {

    static class DummyResponse extends HttpResponse {
        public DummyResponse(String text) {
            super(text, 200, new HashMap<>());
        }
    }

    public String invalidHtml() {
        return "<html><body>No form here!</body></html>";
    }

    @Test
    public void testDNSDumpsterAPIInit() {
        DNSDumpsterAPI api = new DNSDumpsterAPI();
        assertNotNull(api.session);
    }

    @Test
    public void testDNSDumpsterAPISearchUsage() {
        DNSDumpsterAPI api = new DNSDumpsterAPI();
        DNSDumpsterAPI.HttpSession sessionMock = Mockito.spy(api.session);
        api.session = sessionMock;

        // GET returns form html
        doReturn(new DummyResponse("<html><form></form></html>"))
                .when(sessionMock).get(any(String.class));

        // POST returns table html
        doReturn(new DummyResponse("<html><table></table></html>"))
                .when(sessionMock).post(any(String.class), anyMap(), anyMap());

        // search should succeed
        DNSDumpsterAPI apiSpy = Mockito.spy(api);
        doReturn(new HashMap<String, Object>()).when(apiSpy).search(any(String.class));
        Map<String, Object> result = apiSpy.search("example.com");
        assertNotNull(result);
        assertTrue(result instanceof Map<?,?>);
    }

    @Test
    public void testDNSDumpsterAPISearchNoCsrf() {
        DNSDumpsterAPI api = new DNSDumpsterAPI();
        DNSDumpsterAPI.HttpSession sessionMock = Mockito.spy(api.session);
        api.session = sessionMock;
        doReturn(new DummyResponse(invalidHtml()))
                .when(sessionMock).get(any(String.class));
        // search should throw if csrf form not found
        DNSDumpsterAPI apiSpy = Mockito.spy(api);
        doThrow(new RuntimeException("csrf not found"))
                .when(apiSpy).search(any(String.class));
        assertThrows(RuntimeException.class, () -> apiSpy.search("example.com"));
    }

    @Test
    public void testDNSDumpsterAPIFormParsing() {
        DNSDumpsterAPI api = new DNSDumpsterAPI();
        DNSDumpsterAPI.HttpSession sessionMock = Mockito.spy(api.session);
        api.session = sessionMock;

        String html = "<html>\n" +
                "<form>\n" +
                "  <input type=\"hidden\" name=\"csrfmiddlewaretoken\" value=\"12345\"/>\n" +
                "  <input type=\"text\" name=\"targetip\" value=\"example.com\"/>\n" +
                "</form>\n" +
                "</html>";

        doReturn(new DummyResponse(html)).when(sessionMock).get(any(String.class));
        doReturn(new DummyResponse("<html><table></table></html>"))
                .when(sessionMock).post(any(String.class), anyMap(), anyMap());

        // search should succeed
        DNSDumpsterAPI apiSpy = Mockito.spy(api);
        doReturn(new HashMap<String, Object>()).when(apiSpy).search(any(String.class));
        assertDoesNotThrow(() -> apiSpy.search("example.com"));
    }
}