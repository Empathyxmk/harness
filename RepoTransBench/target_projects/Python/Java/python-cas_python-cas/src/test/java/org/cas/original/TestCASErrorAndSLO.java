package org.cas.original;

import org.cas.CASError;
import org.cas.SingleLogoutMixin;
import org.dom4j.Element;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class TestCASErrorAndSLO {
    @Test
    void testCASErrorStr() {
        CASError err = new CASError("fail");
        assertTrue(err instanceof CASError);
        assertEquals("fail", err.getMessage());
    }

    @Test
    void testSloGetSamlSlosInvalidXml() {
        String invalidXml = "<bad<xml>";
        List<Element> result = SingleLogoutMixin.getSamlSlos(invalidXml);
        assertNull(result);
    }

    @Test
    void testSloGetSamlSlosValidXml() {
        String validXml = "<samlp:LogoutRequest xmlns:samlp=\"urn:oasis:names:tc:SAML:2.0:protocol\">" +
                "<samlp:SessionIndex>ST-123-SLO</samlp:SessionIndex></samlp:LogoutRequest>";
        List<Element> result = SingleLogoutMixin.getSamlSlos(validXml);
        assertNotNull(result);
        assertEquals(1, result.size());
    }

    @Test
    void testSloVerifyLogoutRequestTrue() {
        String validTicket = "ST-123-SLO";
        String validXml = String.format(
                "<samlp:LogoutRequest xmlns:samlp=\"urn:oasis:names:tc:SAML:2.0:protocol\">" +
                "<samlp:SessionIndex>%s</samlp:SessionIndex></samlp:LogoutRequest>", validTicket);
        assertTrue(SingleLogoutMixin.verifyLogoutRequest(validXml, validTicket));
    }

    @Test
    void testSloVerifyLogoutRequestFalse() {
        String validXml = "<samlp:LogoutRequest xmlns:samlp=\"urn:oasis:names:tc:SAML:2.0:protocol\">" +
                "<samlp:SessionIndex>ST-456</samlp:SessionIndex></samlp:LogoutRequest>";
        String ticket = "ST-123";
        assertFalse(SingleLogoutMixin.verifyLogoutRequest(validXml, ticket));
    }

    @Test
    void testSloVerifyLogoutRequestInvalidXml() {
        assertFalse(SingleLogoutMixin.verifyLogoutRequest("<bad<xml>", "anyticket"));
    }
}