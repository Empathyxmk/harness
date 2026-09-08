package com.typeerror.secure.original.headers;

import com.typeerror.secure.headers.StrictTransportSecurity;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestStrictTransportSecurity {

    @Test
    public void testDefaultHeaderValue() {
        StrictTransportSecurity sts = new StrictTransportSecurity();
        assertTrue(sts.getHeaderValue().contains("max-age"));
    }

    @Test
    public void testSetAndClearDirectives() {
        StrictTransportSecurity sts = new StrictTransportSecurity();
        sts.maxAge(1234);
        assertTrue(sts.getHeaderValue().contains("max-age=1234"));
        sts.includeSubdomains();
        assertTrue(sts.getHeaderValue().contains("includeSubDomains"));
        sts.preload();
        assertTrue(sts.getHeaderValue().contains("preload"));
        String val = sts.getHeaderValue();
        assertTrue(val.contains("max-age=1234") && val.contains("includeSubDomains") && val.contains("preload"));
        sts.clear();
        assertEquals("max-age=31536000", sts.getHeaderValue());
    }

    @Test
    public void testSetCustomValue() {
        StrictTransportSecurity sts = new StrictTransportSecurity();
        sts.maxAge(1).includeSubdomains();
        sts.set("something-custom");
        assertEquals("something-custom", sts.getHeaderValue());
    }

    @Test
    public void testNoDuplicateDirectives() {
        StrictTransportSecurity sts = new StrictTransportSecurity();
        sts.includeSubdomains().includeSubdomains();
        assertEquals(1, countSubstring(sts.getHeaderValue(), "includeSubDomains"));
    }

    private int countSubstring(String str, String sub) {
        int lastIndex = 0;
        int count = 0;
        while(lastIndex != -1){
            lastIndex = str.indexOf(sub,lastIndex);
            if(lastIndex != -1){
                count ++;
                lastIndex += sub.length();
            }
        }
        return count;
    }
}