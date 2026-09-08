package com.example.pynubank.original;

import com.example.pynubank.core.*;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.junit.jupiter.api.BeforeEach;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class CertificateGeneratorTest {
    private static final Map<String, String> headers = new HashMap<>();
    static {
        headers.put("WWW-Authenticate", "device-authorization encrypted-code=\"abc123\", sent-to=\"john@doe\"");
    }

    private static DummyResponse mockResponse(Object content, Map<String, String> returnHeaders, int statusCode) {
        return new DummyResponse(statusCode, "some-url", content, returnHeaders);
    }

    @Test
    void testRequestCodeFailsWhenStatusCodeIsDifferentFrom401() {
        MockHttpClient http = mock(MockHttpClient.class);
        when(http.rawPost(Mockito.anyString(), Mockito.any())).thenReturn(mockResponse(null, null, 200));
        CertificateGenerator generator = new CertificateGenerator("123456789", "hunter12", "1234", http);

        assertThrows(NuException.class, generator::requestCode);
    }

    @Test
    void testRequestCodeFailsWhenThereIsNoAuthenticateHeader() {
        MockHttpClient http = mock(MockHttpClient.class);
        when(http.rawPost(Mockito.anyString(), Mockito.any())).thenReturn(mockResponse(null, new HashMap<>(), 401));
        CertificateGenerator generator = new CertificateGenerator("123456789", "hunter12", "1234", http);

        assertThrows(NuException.class, generator::requestCode);
    }

    @Test
    void testRequestCode() {
        MockHttpClient http = mock(MockHttpClient.class);
        when(http.rawPost(Mockito.anyString(), Mockito.any())).thenReturn(mockResponse(null, headers, 401));
        CertificateGenerator generator = new CertificateGenerator("123456789", "hunter12", "1234", http);

        String email = generator.requestCode();

        assertEquals("john@doe", email);
        assertEquals("abc123", generator.getEncryptedCode());
    }

    @Test
    void testExchangeCertsFailsWhenCalledWithoutRequestCode() {
        MockHttpClient http = mock(MockHttpClient.class);
        CertificateGenerator generator = new CertificateGenerator("123456789", "hunter12", "1234", http);

        assertThrows(NuException.class, () -> generator.exchangeCerts("1234"));
    }

    @Test
    void testExchangeCertFailsWhenStatusCodeIsDifferentFrom200() {
        MockHttpClient http = mock(MockHttpClient.class);
        when(http.rawPost(Mockito.anyString(), Mockito.any()))
            .thenReturn(mockResponse(null, headers, 401));
        CertificateGenerator generator = new CertificateGenerator("123456789", "hunter12", "1234", http);
        generator.requestCode();

        assertThrows(NuException.class, () -> generator.exchangeCerts("1234"));
    }

    @Test
    void testExchangeCerts() {
        Map<String, Object> genCertificateReturn = new HashMap<>();
        genCertificateReturn.put("cert1", "abc");
        genCertificateReturn.put("cert2", "def");

        MockHttpClient http = mock(MockHttpClient.class);
        when(http.rawPost(Mockito.anyString(), Mockito.any()))
            .thenReturn(mockResponse(null, headers, 401)) // for requestCode
            .thenReturn(mockResponse(genCertificateReturn, headers, 200)); // for exchangeCerts
        CertificateGenerator generator = new CertificateGenerator("123456789", "hunter12", "1234", http);

        generator.requestCode();
        Object[] result = generator.exchangeCerts("1234");

        assertNotNull(result[0]);
        assertNotNull(result[1]);
    }
}