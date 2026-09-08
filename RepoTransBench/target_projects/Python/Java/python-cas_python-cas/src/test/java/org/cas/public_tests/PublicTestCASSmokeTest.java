package org.cas.public_tests;

import org.cas.CASError;
import org.cas.SingleLogoutMixin;
import org.dom4j.Element;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class PublicTestCASSmokeTest {
    @Test
    void testSmoketestCasErrorPublic() {
        CASError e = new CASError("smoke_public");
        assertEquals("smoke_public", e.getMessage());
    }

    @Test
    void testSmoketestSloPublic() {
        String logoutXml = "<samlp:LogoutRequest xmlns:samlp=\"urn:oasis:names:tc:SAML:2.0:protocol\">" +
                "<samlp:SessionIndex>ST-PUBLIC-777</samlp:SessionIndex></samlp:LogoutRequest>";
        List<Element> sessionIndexes = SingleLogoutMixin.getSamlSlos(logoutXml);
        assertNotNull(sessionIndexes);
        assertEquals(1, sessionIndexes.size());
        assertEquals("ST-PUBLIC-777", sessionIndexes.get(0).getTextTrim());

        assertTrue(SingleLogoutMixin.verifyLogoutRequest(logoutXml, "ST-PUBLIC-777"));
        assertFalse(SingleLogoutMixin.verifyLogoutRequest(logoutXml, "ST-PUBLIC-888"));
    }

    @Test
    void testSmoketestClientbasePublic() {
        // Just instantiate and check getLoginUrl/getLogoutUrl
        org.cas.CASClientBase cl = new org.cas.CASClientBase(
                true, null,
                "https://smoke.cas.org/server/",
                "https://smoke.cas.org/client/"
        );
        String url = cl.getLoginUrl();
        assertTrue(url.startsWith("https://smoke.cas.org/server/login?"));
        assertTrue(url.contains("renew=true"));
        String out = cl.getLogoutUrl();
        assertEquals("https://smoke.cas.org/server/logout", out);
    }
}