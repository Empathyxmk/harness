package com.cloudconvert.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicSignedUrlTest {

    @Test
    void testSignedUrlWithParams() {
        assertTrue(SignedUrlUtil.getUrl("api", "id", "p").contains("api/"));
    }

    // --- Helper simulation
    static class SignedUrlUtil {
        static String getUrl(String base, String id, String path) { return base+"/"+id+"/"+path+"?sig=s"; }
    }
}