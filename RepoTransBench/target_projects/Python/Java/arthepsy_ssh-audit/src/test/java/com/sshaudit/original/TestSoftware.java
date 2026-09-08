package com.sshaudit.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class TestSoftware {

    public static class Software {
        private final String name;
        private final String version;
        private final String comments;

        public Software(String name, String version, String comments) {
            this.name = name;
            this.version = version;
            this.comments = comments;
        }

        public static Software parse(String s) {
            if (s == null) return null;
            Pattern pattern = Pattern.compile("^([^-\\s]+)-([0-9a-zA-Z.]+)(\\s(.*))?$");
            Matcher m = pattern.matcher(s.trim());
            if (m.find()) {
                String name = m.group(1);
                String version = m.group(2);
                String comments = m.group(4);
                return new Software(name, version, comments);
            }
            return null;
        }

        public String getName() { return name; }
        public String getVersion() { return version; }
        public String getComments() { return comments; }

        @Override
        public String toString() {
            return name + "-" + version + (comments != null && !comments.isEmpty() ? " " + comments : "");
        }

        @Override
        public boolean equals(Object obj) {
            if (!(obj instanceof Software)) return false;
            Software o = (Software)obj;
            return
                ((name == null && o.name == null) || (name != null && name.equals(o.name))) &&
                ((version == null && o.version == null) || (version != null && version.equals(o.version))) &&
                ((comments == null && o.comments == null) || (comments != null && comments.equals(o.comments)));
        }
    }

    @Test
    public void test_software_parse_simple() {
        Software s = Software.parse("OpenSSH-8.5");
        assertNotNull(s);
        assertEquals("OpenSSH", s.getName());
        assertEquals("8.5", s.getVersion());
        assertNull(s.getComments());
    }

    @Test
    public void test_software_parse_with_comments() {
        Software s = Software.parse("Dropbear-2020.80 beta-test version");
        assertNotNull(s);
        assertEquals("Dropbear", s.getName());
        assertEquals("2020.80", s.getVersion());
        assertEquals("beta-test version", s.getComments());
    }

    @Test
    public void test_software_parse_invalid_input() {
        Software s = Software.parse("no-version-string");
        assertNotNull(s);
        assertEquals("no", s.getName());
        assertEquals("version", s.getVersion());
        assertEquals("string", s.getComments());
    }

    @Test
    public void test_software_parse_null() {
        Software s = Software.parse(null);
        assertNull(s);
    }

    @Test
    public void test_software_toString() {
        Software s = new Software("OpenSSH", "7.9", null);
        assertEquals("OpenSSH-7.9", s.toString());
        Software s2 = new Software("Dropbear", "2018.76", "testing");
        assertEquals("Dropbear-2018.76 testing", s2.toString());
    }

    @Test
    public void test_software_equality() {
        Software s1 = new Software("A", "1", "x");
        Software s2 = new Software("A", "1", "x");
        Software s3 = new Software("A", "1", null);
        assertEquals(s1, s2);
        assertNotEquals(s1, s3);
    }
}