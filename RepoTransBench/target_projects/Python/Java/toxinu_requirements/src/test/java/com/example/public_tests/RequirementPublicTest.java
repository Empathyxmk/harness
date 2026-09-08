package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.example.Requirement;

public class RequirementPublicTest {

    @Test
    void testParseNormalRequirementPublic() {
        Requirement r = Requirement.parse("boto3>=1.15");
        assertNotNull(r);
        assertNotNull(r.getName());
        assertEquals("boto3", r.getName());
        if (r.hasSpecifier()) {
            assertNotNull(r.getSpecifier());
        }
        if (r.hasIsLocalFile()) {
            assertFalse(r.getIsLocalFile());
        }
    }

    @Test
    void testParseLocalFileEditablePublic() {
        Exception exception = assertThrows(Exception.class, () ->
                Requirement.parse("/another/path/to/pkg2", true));
    }

    @Test
    void testParseLocalFileSchemePublic() {
        Requirement r = Requirement.parse("file:///tmp/anotherpackage#egg=otherpkg");
        assertTrue(r.toString().contains("file://"));
    }

    @Test
    void testParseVcsUrlPublic() {
        String vcsUrl = "hg+https://bitbucket.org/user/repo2#egg=hgproject";
        Requirement r = Requirement.parse(vcsUrl);
        String rStr = r.toString();
        assertTrue(rStr.startsWith("hg+") || rStr.contains("hg+"));
    }

    @Test
    void testParseWithMarkerPublic() {
        Requirement r = Requirement.parse("urllib3; sys_platform==\"win32\"");
        assertNotNull(r.getName());
        if (r.hasMarker()) {
            assertNotNull(r.getMarker());
        }
    }

    @Test
    void testStrReprPublic() {
        Requirement r = Requirement.parse("sqlalchemy");
        String s = r.toString();
        assertTrue(s.equals("sqlalchemy") || s.equals("<Requirement: \"sqlalchemy\">"));
        assertTrue(r.toDebugString() instanceof String);
    }

    @Test
    void testEqualityAndHashPublic() {
        Requirement r1 = Requirement.parse("bar==3.4");
        Requirement r2 = Requirement.parse("bar==3.4");
        try {
            assertEquals(r1, r2);
        } catch (Exception e) {
        }
        r1.hashCode();
        r2.hashCode();
    }

    @Test
    void testRequirementExtrasPublic() {
        Requirement r = Requirement.parse("pandas[performance,io]>=1.0");
        assertTrue(r.hasExtras() && r.getExtras().contains("performance"));
    }

    @Test
    void testParseInvalidRequirementPublic() {
        assertThrows(Exception.class, () -> {
            Requirement.parse("??? this is not valid");
        });
    }

    @Test
    void testLocalFileDetectedPublic() {
        assertThrows(Exception.class, () -> {
            Requirement.parse("../something.whl");
        });
    }
}