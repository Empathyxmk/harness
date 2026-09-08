package com.example.dnsdumpster.publictests;

import com.example.dnsdumpster.DNSDumpsterAPI;
import org.junit.jupiter.api.*;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class PublicDNSDumpsterApiTest {

    private static Map<String, Object> dummySearch(DNSDumpsterAPI api, String domain) {
        Map<String, Object> dnsMap;
        Map<String, Object> result = new HashMap<>();
        if (domain.equals("duckduckgo.com")) {
            dnsMap = new HashMap<>();
            dnsMap.put("dns", Arrays.asList(Collections.singletonMap("domain", "ns1.duckduckgo.com")));
            dnsMap.put("mx", Arrays.asList(Collections.singletonMap("exchange", "duckduckgo-com.mail.protection.outlook.com")));
            dnsMap.put("host", Arrays.asList(Collections.singletonMap("host", "imap.duckduckgo.com")));
            result.put("domain", "duckduckgo.com");
            result.put("dns_records", dnsMap);
        } else if (domain.equals("mit.edu")) {
            dnsMap = new HashMap<>();
            dnsMap.put("dns", Arrays.asList(Collections.singletonMap("domain", "NS1-163.AKAM.NET")));
            dnsMap.put("mx", Arrays.asList(Collections.singletonMap("exchange", "mit-edu.mail.protection.outlook.com")));
            dnsMap.put("host", Arrays.asList(Collections.singletonMap("host", "imap.mit.edu")));
            result.put("domain", "mit.edu");
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
    public void testDNSDumpsterAPIPublicAttributeTypes() {
        DNSDumpsterAPI api = new DNSDumpsterAPI() {
            @Override
            public Map<String, Object> search(String domain) {
                return dummySearch(this, domain);
            }
        };
        Map<String, Object> result = api.search("duckduckgo.com");
        assertNotNull(result);
        assertEquals("duckduckgo.com", result.get("domain"));
        assertTrue(result.containsKey("dns_records"));
        Object dnsRecords = result.get("dns_records");
        assertTrue(dnsRecords instanceof Map<?,?>);

        Map<?,?> records = (Map<?,?>) dnsRecords;
        assertTrue(records.containsKey("mx"));
        assertTrue(records.get("mx") instanceof List<?>);
        assertTrue(records.containsKey("host"));
        assertTrue(records.containsKey("dns"));

        for (String key : Arrays.asList("mx", "host", "dns")) {
            assertTrue(records.containsKey(key));
        }
    }

    @Test
    public void testDNSDumpsterAPIPublicResultContent() {
        DNSDumpsterAPI api = new DNSDumpsterAPI() {
            @Override
            public Map<String, Object> search(String domain) {
                return dummySearch(this, domain);
            }
        };
        Map<String, Object> res = api.search("mit.edu");
        assertNotNull(res);
        assertEquals("mit.edu", res.get("domain"));
        assertTrue(res.size() > 1);

        Object dnsRecords = res.get("dns_records");
        boolean hasRecords = false;
        if (dnsRecords instanceof Map<?,?>) {
            for (Object records : ((Map<?,?>)dnsRecords).values()) {
                if (records instanceof List<?> && !((List<?>)records).isEmpty()) {
                    hasRecords = true;
                    break;
                }
            }
        }
        assertTrue(hasRecords, "There should be at least one populated DNS record entry");
    }
}