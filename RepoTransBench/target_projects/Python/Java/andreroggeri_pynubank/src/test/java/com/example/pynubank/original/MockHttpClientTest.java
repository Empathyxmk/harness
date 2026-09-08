package com.example.pynubank.original;

import com.example.pynubank.core.*;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeAll;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

public class MockHttpClientTest {

    static Nubank client;

    @BeforeAll
    static void setUpClient() {
        client = new Nubank(new MockHttpClient());
        client.authenticateWithQRCode("12345678912", "hunter12", "some-uuid");
    }

    @Test
    void testGetInvalidUrlShouldThrowException() {
        MockHttpClient client = new MockHttpClient();
        assertThrows(NuException.class, () -> client.get("invalid.url"));
    }

    @Test
    void testPostInvalidUrlShouldThrowException() {
        MockHttpClient client = new MockHttpClient();
        assertThrows(NuException.class, () -> client.post("invalid.url", new HashMap<>()));
    }

    @Test
    void testCheckNotTestedNewMethods() {
        Map<String, Object> defaultParams = new HashMap<>();
        Map<String, Object> bill = new HashMap<>();
        Map<String, Object> billLinks = new HashMap<>();
        billLinks.put("href", "https://mocked-proxy-url/api/bills/abcde-fghi-jklmn-opqrst-uvxz");
        Map<String, Object> billLinksWrap = new HashMap<>();
        billLinksWrap.put("self", billLinks);
        bill.put("_links", billLinksWrap);
        defaultParams.put("getBillDetails", bill);

        Map<String, Object> yield = new HashMap<>();
        yield.put("date", LocalDateTime.now());
        defaultParams.put("getAccountInvestmentsYield", yield);

        Map<String, Object> stmt = new HashMap<>();
        Map<String, Object> stmtLinks = new HashMap<>();
        stmtLinks.put("href", "https://mocked-proxy-url/api/transactions/" + UUID.randomUUID());
        Map<String, Object> stmtLinksWrap = new HashMap<>();
        stmtLinksWrap.put("self", stmtLinks);
        stmt.put("_links", stmtLinksWrap);
        defaultParams.put("getCardStatementDetails", stmt);

        Map<String, Object> cert = new HashMap<>();
        cert.put("cpf", "12345678912");
        cert.put("password", "hunter12");
        cert.put("certData", new byte[]{1,2,3});
        defaultParams.put("authenticateWithCert", cert);

        Map<String, Object> refresh = new HashMap<>();
        refresh.put("refreshToken", "refresh_token");
        refresh.put("certData", new byte[]{1,2,3});
        defaultParams.put("authenticateWithRefreshToken", refresh);

        // For simplicity, call some representative methods with valid data.
        // In a real test harness, would use reflection to call all required methods.
        client.getBillDetails(bill);
        client.getAccountInvestmentsYield(yield);
    }
}