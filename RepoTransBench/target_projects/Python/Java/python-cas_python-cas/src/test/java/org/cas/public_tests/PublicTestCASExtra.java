package org.cas.public_tests;

import org.cas.CASError;
import org.cas.SingleLogoutMixin;
import org.dom4j.Element;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class PublicTestCASExtra {
    @Test
    void testExtraErrorTypePublic() {
        CASError x = new CASError("extra public error example");
        assertTrue(x.getMessage().contains("extra"));
        assertTrue(x instanceof CASError);
    }

    @Test
    void testExtraLogoutMixinInvalidXmlPublic() {
        String invalidXml = "some completely invalid {{{";
        List<Element> result = SingleLogoutMixin.getSamlSlos(invalidXml);
        assertNull(result);
    }

    @Test
    void testExtraLogoutMixinValidXmlPublic() {
        String validXml = "<samlp:LogoutRequest xmlns:samlp=\"urn:oasis:names:tc:SAML:2.0:protocol\">" +
                "<samlp:SessionIndex>EXTRA-222-SLO</samlp:SessionIndex></samlp:LogoutRequest>";
        List<Element> result = SingleLogoutMixin.getSamlSlos(validXml);
        assertNotNull(result);
        assertEquals(1, result.size());
        assertEquals("EXTRA-222-SLO", result.get(0).getTextTrim());
    }
}