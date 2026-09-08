package com.typeerror.secure.original;

import com.typeerror.secure.secure.HeadersProtocol;
import com.typeerror.secure.secure.SetHeaderProtocol;
import com.typeerror.secure.secure.Secure;
import com.typeerror.secure.headers.CacheControl;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestSecureProtocols {

    static class DummyHeadersObj implements HeadersProtocol {
        public java.util.Map<String, String> headers = new java.util.HashMap<>();
        @Override
        public java.util.Map<String, String> getHeaders() { return headers; }
    }

    static class DummySetHeaderObj implements SetHeaderProtocol {
        public boolean called = false;
        public String lastKey = null;
        public String lastValue = null;
        @Override
        public void setHeader(String key, String value) {
            this.called = true;
            this.lastKey = key;
            this.lastValue = value;
        }
    }

    @Test
    public void testHeadersProtocolPep544() {
        DummyHeadersObj o = new DummyHeadersObj();
        assertTrue(o instanceof HeadersProtocol);
        Object notHdrs = new Object();
        assertFalse(notHdrs instanceof HeadersProtocol);
    }

    @Test
    public void testSetHeaderProtocolPep544() {
        DummySetHeaderObj o = new DummySetHeaderObj();
        assertTrue(o instanceof SetHeaderProtocol);
        Object notSet = new Object();
        assertFalse(notSet instanceof SetHeaderProtocol);
    }

    @Test
    public void testSecureResponseProtocolHeaders() {
        Secure s = new Secure.Builder().cache(new CacheControl().noStore()).build();
        DummyHeadersObj dummyResp = new DummyHeadersObj();
        assertNotNull(s.getHeadersList());
        assertTrue(s.getHeadersList().get(0) instanceof CacheControl);
    }
}