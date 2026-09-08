package com.sshaudit.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

public class TestBanner {

    public static class Banner {
        public String proto;
        public int version;
        public String software;
        public String comments;

        public Banner(String proto, int version, String software, String comments) {
            this.proto = proto;
            this.version = version;
            this.software = software;
            this.comments = comments;
        }

        public static Banner parse(String banner) {
            if (banner == null || !banner.startsWith("SSH-")) return null;
            String[] parts = banner.split("-", 3);
            if (parts.length < 3) return null;
            String proto = parts[1];
            String[] softparts = parts[2].split(" ", 2);
            String software = softparts[0];
            String comments = "";
            int version = -1;
            try {
                if (proto.startsWith("2.0")) {
                    version = 2;
                } else if (proto.equals("1.99")) {
                    version = 2;
                } else if (proto.startsWith("1.")) {
                    version = 1;
                }
            } catch (Exception e) {
            }
            if (softparts.length > 1)
                comments = softparts[1];
            return new Banner(proto, version, software, comments);
        }
    }

    @Test
    public void test_banner_parse() {
        Object[][] data = {
                {"SSH-2.0-OpenSSH_7.4p1 Debian-10+deb9u7", "2.0", 2, "OpenSSH_7.4p1", "Debian-10+deb9u7"},
                {"SSH-1.99-OpenSSH_5.5p1 Debian-6+squeeze5", "1.99", 2, "OpenSSH_5.5p1", "Debian-6+squeeze5"},
                {"SSH-1.5-OpenSSH_4.3", "1.5", 1, "OpenSSH_4.3", ""},
                {"SSH-2.0-dropbear_2018.76", "2.0", 2, "dropbear_2018.76", ""}
        };
        for (Object[] d : data) {
            String ban = (String) d[0];
            String proto = (String) d[1];
            int version = (Integer) d[2];
            String software = (String) d[3];
            String comments = (String) d[4];
            Banner b = Banner.parse(ban);
            assertNotNull(b, "Banner should be parsed");
            assertEquals(proto, b.proto);
            assertEquals(version, b.version);
            assertEquals(software, b.software);
            assertEquals(comments, b.comments);
        }
        // Negative test
        assertNull(Banner.parse("invalid banner string"));
        assertNull(Banner.parse(null));
    }
}