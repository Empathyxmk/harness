package com.typeerror.secure.public_;

import com.typeerror.secure.secure.HeadersProtocol;
import com.typeerror.secure.secure.SetHeaderProtocol;
import com.typeerror.secure.secure.Secure;
import com.typeerror.secure.headers.StrictTransportSecurity;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestSecureProtocolsPublic {

    static class AlternateHeadersObj implements HeadersProtocol {
        public java.util.Map<String, String> headers = new java.util.HashMap<>();
        public AlternateHeadersObj() { headers.put("X-Test", "abc"); }
        @Override
        public java.util.Map<String, String> getHeaders() { return headers; }
    }

    static class AlternateSetHeaderObj implements SetHeaderProtocol {
        public boolean wasCalled = false;
        public String k = null, v = null;
        @Override
        public void setHeader(String k, String v) {
            this.wasCalled = true;
            this.k = k;
            this.v = v;
        }
    }

    @Test
    public void testHeadersProtocolPublic() {
        AlternateHeadersObj o = new AlternateHeadersObj();
        assertTrue(o instanceof HeadersProtocol);
        Object notHdrs = Integer.valueOf(42);
        assertFalse(notHdrs instanceof HeadersProtocol);
    }

    @Test
    public void testSetHeaderProtocolPublic() {
        AlternateSetHeaderObj o = new AlternateSetHeaderObj();
        assertTrue(o instanceof SetHeaderProtocol);
        Object notSet = new java.util.ArrayList<>();
        assertFalse(notSet instanceof SetHeaderProtocol);
    }

    @Test
    public void testSecureResponseProtocolHeadersPublic() {
        Secure s = new Secure.Builder().hsts(new StrictTransportSecurity().maxAge(777)).build();
        AlternateHeadersObj dummyResp = new AlternateHeadersObj();
        assertNotNull(s.getHeadersList());
        assertTrue(s.getHeadersList().get(0) instanceof StrictTransportSecurity);
    }
}