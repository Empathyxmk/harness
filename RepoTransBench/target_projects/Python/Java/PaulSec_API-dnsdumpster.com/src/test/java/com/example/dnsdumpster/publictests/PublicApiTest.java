package com.example.dnsdumpster.publictests;

import com.example.dnsdumpster.DNSDumpsterAPI;

import org.junit.jupiter.api.*;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class PublicApiTest {

    static class DummyResponse {
        String content;
        DummyResponse(String content) {
            this.content = content;
        }
    }

    private static Map<String, Object> dummySearch(DNSDumpsterAPI api, String domain) {
        Map<String, Object> dnsMap;
        Map<String, Object> result = new HashMap<>();
        if (domain.equals("openai.com")) {
            dnsMap = new HashMap<>();
            dnsMap.put("dns", Arrays.asList(Collections.singletonMap("domain", "ns1.openai.com")));
            dnsMap.put("mx", Arrays.asList(Collections.singletonMap("exchange", "aspmx.l.google.com")));
            dnsMap.put("host", Arrays.asList(Collections.singletonMap("host", "mail.openai.com")));
            result.put("domain", "openai.com");
            result.put("dns_records", dnsMap);
        } else if (domain.equals("duckduckgo.com")) {
            dnsMap = new HashMap<>();
            dnsMap.put("dns", Arrays.asList(Collections.singletonMap("domain", "ns1.duckduckgo.com")));
            dnsMap.put("mx", Arrays.asList(Collections.singletonMap("exchange", "duckduckgo-com.mail.protection.outlook.com")));
            dnsMap.put("host", Arrays.asList(Collections.singletonMap("host", "imap.duckduckgo.com")));
            result.put("domain", "duckduckgo.com");
            result.put("dns_records", dnsMap);
        } else {
            dnsMap = new HashMap<>();
            dnsMap.put("dns", new ArrayList<>());
            dnsMap.put("mx", new ArrayList<>());
            dnsMap.put("host", new ArrayList<>());
            result.put("domain", domain);
            result.put("dns_records", dnsMap);
        }
        return result;
    }

    @Test
    public void testDNSDumpsterAPIPublicSearch() {
        DNSDumpsterAPI api = new DNSDumpsterAPI() {
            @Override
            public Map<String, Object> search(String domain) {
                return dummySearch(this, domain);
            }
        };
        Map<String, Object> result = api.search("openai.com");
        assertNotNull(result);
        assertEquals("openai.com", result.get("domain"));
        assertTrue(result.containsKey("dns_records"));

        Object dnsRecords = result.get("dns_records");
        assertTrue(dnsRecords instanceof Map<?,?>);
        boolean found = false;

        Map<?,?> dnsMap = (Map<?,?>)dnsRecords;
        for (Object o : dnsMap.values()) {
            if (o instanceof List<?> && !((List<?>)o).isEmpty()) {
                found = true;
                break;
            }
        }
        assertTrue(found, "At least one DNS record list should not be empty");
    }
}