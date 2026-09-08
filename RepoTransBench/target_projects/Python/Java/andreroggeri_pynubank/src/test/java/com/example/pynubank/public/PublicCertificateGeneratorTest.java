package com.example.pynubank.public;

import com.example.pynubank.core.*;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class PublicCertificateGeneratorTest {
    private static final Map<String, String> headers = new HashMap<>();
    static {
        headers.put("WWW-Authenticate", "device-authorization encrypted-code=\"xyz987\", sent-to=\"foo@bar\"");
    }

    private static DummyResponse mockResponse(Object content, Map<String, String> returnHeaders, int statusCode) {
        return new DummyResponse(statusCode, "url", content, returnHeaders);
    }

    @Test
    void testRequestCode() {
        MockHttpClient http = mock(MockHttpClient.class);
        when(http.rawPost(Mockito.anyString(), Mockito.any())).thenReturn(mockResponse(null, headers, 401));
        CertificateGenerator generator = new CertificateGenerator("public_cpf", "public_pass", "public_id", http);

        String email = generator.requestCode();

        assertEquals("foo@bar", email);
        assertEquals("xyz987", generator.getEncryptedCode());
    }

    @Test
    void testExchangeCerts() {
        Map<String, Object> certResp = new HashMap<>();
        certResp.put("pub1", "val1");
        certResp.put("pub2", "val2");

        MockHttpClient http = mock(MockHttpClient.class);
        when(http.rawPost(Mockito.anyString(), Mockito.any()))
            .thenReturn(mockResponse(null, headers, 401))
            .thenReturn(mockResponse(certResp, headers, 200));

        CertificateGenerator generator = new CertificateGenerator("public_cpf", "public_pass", "public_id", http);
        generator.requestCode();
        Object[] result = generator.exchangeCerts("public_code");

        assertNotNull(result[0]);
        assertNotNull(result[1]);
    }
}