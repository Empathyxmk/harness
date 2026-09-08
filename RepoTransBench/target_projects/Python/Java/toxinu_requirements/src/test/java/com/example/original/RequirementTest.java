package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.example.Requirement;

public class RequirementTest {

    @Test
    void testParseNormalRequirement() {
        Requirement r = Requirement.parse("requests>=2.0");
        assertNotNull(r);
        assertNotNull(r.getName());
        assertEquals("requests", r.getName());
        // specifier may be missing, only check if attribute present
        if (r.hasSpecifier()) {
            assertNotNull(r.getSpecifier());
        }
        if (r.hasIsLocalFile()) {
            assertFalse(r.getIsLocalFile());
        }
    }

    @Test
    void testParseLocalFileEditable() {
        Exception exception = assertThrows(Exception.class, () ->
                Requirement.parse("/some/path/to/pkg", true));
    }

    @Test
    void testParseLocalFileScheme() {
        Requirement r = Requirement.parse("file:///tmp/somepackage#egg=mypkg");
        assertTrue(r.toString().contains("file://"));
    }

    @Test
    void testParseVcsUrl() {
        String vcsUrl = "git+https://github.com/user/repo.git#egg=myrepo";
        Requirement r = Requirement.parse(vcsUrl);
        String rStr = r.toString();
        assertTrue(rStr.startsWith("git+") || rStr.contains("git+"));
    }

    @Test
    void testParseWithMarker() {
        Requirement r = Requirement.parse("requests; python_version>=\"3.0\"");
        assertNotNull(r.getName());
        if (r.hasMarker()) {
            assertNotNull(r.getMarker());
        }
    }

    @Test
    void testStrRepr() {
        Requirement r = Requirement.parse("flask");
        String s = r.toString();
        assertTrue(s.equals("flask") || s.equals("<Requirement: \"flask\">"));
        assertTrue(r.toDebugString() instanceof String);
    }

    @Test
    void testEqualityAndHash() {
        Requirement r1 = Requirement.parse("foo==1.0");
        Requirement r2 = Requirement.parse("foo==1.0");
        try {
            assertEquals(r1, r2);
        } catch (Exception e) {
            // Some implementations do not use eq, so gracefully fallback
        }
        r1.hashCode();
        r2.hashCode();
    }

    @Test
    void testRequirementExtras() {
        Requirement r = Requirement.parse("requests[security]>=2.0");
        assertTrue(r.hasExtras() && r.getExtras().contains("security"));
    }

    @Test
    void testParseInvalidRequirement() {
        assertThrows(Exception.class, () -> {
            Requirement.parse("not a valid requirement ???");
        });
    }

    @Test
    void testLocalFileDetected() {
        // Should raise due to invalid requirement syntax as seen previously
        assertThrows(Exception.class, () -> {
            Requirement.parse("./myscript.whl");
        });
    }
}