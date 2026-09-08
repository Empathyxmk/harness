package com.typeerror.secure.original;

import com.typeerror.secure.headers.*;
import com.typeerror.secure.*;
import java.util.List;
import java.util.stream.Collectors;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestSecureAPIMinimal {

    @Test
    public void testSecureWithNoHeaders() {
        Secure s = new Secure();
        assertTrue(s.getHeadersList().isEmpty());
    }

    @Test
    public void testSecureWithSomeHeaders() {
        CacheControl c = new CacheControl().noStore();
        Secure s = new Secure.Builder().cache(c).build();
        assertSame(c, s.getHeadersList().get(0));
    }

    @Test
    public void testSecureWithCustomList() {
        CustomHeader ch1 = new CustomHeader("X-Test", "A");
        CustomHeader ch2 = new CustomHeader("X-Foo", "Bar");
        Secure s = new Secure.Builder().custom(List.of(ch1, ch2)).build();
        List<Object> actual = s.getHeadersList();
        assertTrue(actual.contains(ch1) && actual.contains(ch2));
    }

    @Test
    public void testSecureWithAllHeaders() {
        Secure s = new Secure.Builder()
                .cache(new CacheControl().noStore())
                .coop(new CrossOriginOpenerPolicy().sameOrigin())
                .csp(new ContentSecurityPolicy().defaultSrc("'none'"))
                .hsts(new StrictTransportSecurity().maxAge(3600))
                .permissions(new PermissionsPolicy().camera())
                .referrer(new ReferrerPolicy().strictOriginWhenCrossOrigin())
                .server(new Server().set("test"))
                .xcto(new XContentTypeOptions().nosniff())
                .xfo(new XFrameOptions().deny())
                .custom(List.of(new CustomHeader("X-A", "B")))
                .build();
        // Should be at least one CustomHeader in headers_list
        assertTrue(s.getHeadersList().stream().anyMatch(h -> h instanceof CustomHeader));
    }

    @Test
    public void testSecureWithDefaultHeaders() {
        Secure s = Secure.withDefaultHeaders();
        List<String> names = s.getHeadersList().stream()
                .map(h -> h.getClass().getSimpleName())
                .collect(Collectors.toList());
        String[] expectedTypes = {
            "CacheControl", "CrossOriginOpenerPolicy", 
            "ContentSecurityPolicy", "StrictTransportSecurity",
            "PermissionsPolicy", "ReferrerPolicy", "Server",
            "XContentTypeOptions", "XFrameOptions"
        };
        for (String typ : expectedTypes) {
            assertTrue(names.contains(typ), "Missing header type " + typ);
        }
    }
}