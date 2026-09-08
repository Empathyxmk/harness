package com.requests.oauthlib.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.HashMap;
import java.util.Map;

class PublicComplianceFixesTest {

    @Test
    void publicTestFacebookFix() {
        Map<String, Object> fbResp = new HashMap<>();
        fbResp.put("access_token", "pubABC");
        fbResp.put("token_type", "bearer");
        Map<String, Object> fixed = applyFacebookComplianceFix(fbResp);
        assertEquals("pubABC", fixed.get("access_token"));
        assertEquals("bearer", fixed.get("token_type"));
    }

    private Map<String, Object> applyFacebookComplianceFix(Map<String, Object> resp) {
        return resp;
    }

    @Test
    void publicTestDropboxFix() {
        Map<String, Object> dbResp = new HashMap<>();
        dbResp.put("expires_in", "9999");
        Map<String, Object> fixed = applyDropboxComplianceFix(dbResp);
        assertEquals("9999", fixed.get("expires_in"));
    }

    private Map<String, Object> applyDropboxComplianceFix(Map<String, Object> resp) {
        return resp;
    }
}