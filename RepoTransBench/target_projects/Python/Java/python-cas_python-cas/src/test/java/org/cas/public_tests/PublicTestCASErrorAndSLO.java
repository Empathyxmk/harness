package org.cas.public_tests;

import org.cas.CASError;
import org.cas.SingleLogoutMixin;
import org.dom4j.Element;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class PublicTestCASErrorAndSLO {
    @Test
    void testCaserrorStrPublic() {
        CASError err = new CASError("another_fail");
        assertTrue(err instanceof CASError);
        assertEquals("another_fail", err.getMessage());
    }

    @Test
    void testSloGetSamlSlosInvalidXmlPublic() {
        String invalidXml = "<xml broken";
        List<Element> result = SingleLogoutMixin.getSamlSlos(invalidXml);
        assertNull(result);
    }

    @Test
    void testSloGetSamlSlosValidXmlPublic() {
        String validXml = "<samlp:LogoutRequest xmlns:samlp=\"urn:oasis:names:tc:SAML:2.0:protocol\">" +
                "<samlp:SessionIndex>ST-999-SLO</samlp:SessionIndex></samlp:LogoutRequest>";
        List<Element> result = SingleLogoutMixin.getSamlSlos(validXml);
        assertNotNull(result);
        assertEquals(1, result.size());
    }

    @Test
    void testSloVerifyLogoutRequestTruePublic() {
        String validTicket = "ST-999-SLO";
        String validXml = String.format(
                "<samlp:LogoutRequest xmlns:samlp=\"urn:oasis:names:tc:SAML:2.0:protocol\">" +
                "<samlp:SessionIndex>%s</samlp:SessionIndex></samlp:LogoutRequest>", validTicket);
        assertTrue(SingleLogoutMixin.verifyLogoutRequest(validXml, validTicket));
    }

    @Test
    void testSloVerifyLogoutRequestFalsePublic() {
        String validXml = "<samlp:LogoutRequest xmlns:samlp=\"urn:oasis:names:tc:SAML:2.0:protocol\">" +
                "<samlp:SessionIndex>ST-555</samlp:SessionIndex></samlp:LogoutRequest>";
        String ticket = "ST-999";
        assertFalse(SingleLogoutMixin.verifyLogoutRequest(validXml, ticket));
    }

    @Test
    void testSloVerifyLogoutRequestInvalidXmlPublic() {
        assertFalse(SingleLogoutMixin.verifyLogoutRequest("<broken <xml>", "otherticket"));
    }
}