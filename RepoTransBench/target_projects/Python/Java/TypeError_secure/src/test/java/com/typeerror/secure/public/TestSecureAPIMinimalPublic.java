package com.typeerror.secure.public_;

import com.typeerror.secure.headers.*;
import com.typeerror.secure.secure.Secure;
import java.util.List;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestSecureAPIMinimalPublic {

    @Test
    public void testSecureWithNoCustomHeadersPublic() {
        Secure s = new Secure();
        assertTrue(s.getHeadersList().isEmpty());
    }

    @Test
    public void testSecureWithOneHeaderPublic() {
        CacheControl c = new CacheControl().maxAge(1234);
        Secure s = new Secure.Builder().cache(c).build();
        assertSame(c, s.getHeadersList().get(0));
    }

    @Test
    public void testSecureWithMultipleCustomHeadersPublic() {
        CustomHeader ch1 = new CustomHeader("X-Public-Header", "Val1");
        CustomHeader ch2 = new CustomHeader("X-Diff-Header", "DiffVal");
        Secure s = new Secure.Builder().custom(List.of(ch1, ch2)).build();
        List<Object> headersList = s.getHeadersList();
        assertTrue(headersList.contains(ch1) && headersList.contains(ch2));
    }

    @Test
    public void testSecureWithVariousHeadersPublic() {
        Secure s = new Secure.Builder()
                .cache(new CacheControl().maxAge(500))
                .coep(new CrossOriginEmbedderPolicy().requireCorp())
                .csp(new ContentSecurityPolicy().defaultSrc("'self'"))
                .hsts(new StrictTransportSecurity().maxAge(1800))
                .permissions(new PermissionsPolicy().microphone())
                .referrer(new ReferrerPolicy().noReferrer())
                .server(new Server().set("Different"))
                .xcto(new XContentTypeOptions().nosniff())
                .xfo(new XFrameOptions().sameorigin())
                .custom(List.of(new CustomHeader("X-B", "C")))
                .build();
        assertTrue(s.getHeadersList().stream().anyMatch(h -> h instanceof CustomHeader));
        assertTrue(s.getHeadersList().stream().anyMatch(h -> h instanceof XFrameOptions));
    }

    @Test
    public void testSecureWithPartialHeadersPublic() {
        Secure s = new Secure.Builder()
                .xcto(new XContentTypeOptions().nosniff())
                .server(new Server().set("PublicTest"))
                .referrer(new ReferrerPolicy().origin())
                .custom(List.of(new CustomHeader("X-Y", "Z")))
                .build();
        assertTrue(s.getHeadersList().stream().anyMatch(h -> h instanceof XContentTypeOptions));
        assertTrue(s.getHeadersList().stream().anyMatch(h -> h instanceof Server));
        assertTrue(s.getHeadersList().stream().anyMatch(h -> h instanceof ReferrerPolicy));
        assertTrue(s.getHeadersList().stream().anyMatch(h -> h instanceof CustomHeader));
    }
}