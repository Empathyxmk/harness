package com.owncloud.original;

import static org.junit.jupiter.api.Assertions.*;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class ShareInfoTest {
    // Placeholder: Replace with your implementation of ShareInfo and related utilities
    static class ShareInfo {
        public Map<String, Object> share_info;

        public ShareInfo(Map<String, Object> info) {
            share_info = new HashMap<>(info);
        }

        public int get_id() {
            Object id = share_info.get("id");
            if (id instanceof Integer) return (Integer) id;
            if (id instanceof String && !((String) id).isEmpty()) return Integer.parseInt((String) id);
            return 0;
        }

        public int get_share_type() {
            Object st = share_info.get("share_type");
            if (st == null || (st instanceof String && ((String) st).isEmpty())) return 0;
            if (st instanceof Integer) return (Integer) st;
            return Integer.parseInt(st.toString());
        }

        public String get_share_with() {
            return (String) share_info.getOrDefault("share_with", null);
        }

        public String get_share_with_displayname() {
            return (String) share_info.getOrDefault("share_with_displayname", null);
        }

        public String get_path() {
            return (String) share_info.getOrDefault("path", null);
        }

        public String get_expiration() {
            Object v = share_info.get("expiration");
            return v == null ? null : v.toString();
        }

        public java.util.Date get_share_time() {
            Object stime = share_info.get("stime");
            if (stime instanceof String && !((String) stime).isEmpty()) {
                long timestamp = Long.parseLong((String) stime);
                return Date.from(Instant.ofEpochSecond(timestamp));
            }
            return null;
        }

        public Integer _get_int(String field) {
            Object v = share_info.get(field);
            if (v == null || (v instanceof String && ((String) v).isEmpty())) return null;
            if (v instanceof Integer) return (Integer) v;
            try {
                return Integer.valueOf(v.toString());
            } catch (Exception e) {
                return null;
            }
        }

        public void del_attrs() {
            String[] remove = {"item_type", "parent"};
            for (String r : remove)
                share_info.remove(r);
        }

        public boolean containsKey(String k) {
            return share_info.containsKey(k);
        }

        public Object get(String key) {
            return share_info.get(key);
        }
    }

    ShareInfo share;

    @BeforeEach
    void setUp() {
        Map<String, Object> info = new HashMap<>();
        info.put("id", "123");
        info.put("share_type", "1");
        info.put("permissions", "3");
        info.put("share_with", "user1");
        info.put("share_with_displayname", "User One");
        info.put("stime", "1777777700");
        info.put("expiration", "2024-12-31");
        info.put("path", "/some.txt");
        share = new ShareInfo(info);
    }

    @Test
    void test_getters() {
        assertEquals(123, share.get_id());
        assertEquals(1, share.get_share_type());
        assertEquals("user1", share.get_share_with());
        assertEquals("User One", share.get_share_with_displayname());
        assertEquals("/some.txt", share.get_path());
        assertEquals("2024-12-31", share.get_expiration());
        assertNotNull(share.get_share_time());
        assertTrue(share.get_share_time() instanceof java.util.Date);
    }

    @Test
    void test_int_conversion() {
        Map<String, Object> info = new HashMap<>();
        info.put("id", 123);
        info.put("permissions", "");
        info.put("share_type", null);
        info.put("stime", "1777777700");
        info.put("expiration", null);
        ShareInfo si = new ShareInfo(info);
        assertEquals(123, si._get_int("id"));
        assertNull(si._get_int("permissions"));
        assertNull(si._get_int("share_type"));
        assertNotNull(si.get_share_time());
        assertTrue(si.get_share_time() instanceof java.util.Date);
    }

    @Test
    void test_missing_attrs() {
        ShareInfo blank = new ShareInfo(new HashMap<>());
        assertNull(blank.get_share_with());
        assertNull(blank.get_share_with_displayname());
        assertNull(blank.get_path());
    }

    @Test
    void test_del_attrs_removed() {
        Map<String, Object> input = new HashMap<>();
        input.put("id", "1");
        input.put("storage", "xxx");
        input.put("mail_send", 1);
        input.put("item_type", "foo");
        input.put("item_source", 42);
        input.put("file_source", 15);
        input.put("parent", null);
        input.put("other", "ok");
        input.put("stime", "1000");

        ShareInfo si = new ShareInfo(input);
        si.del_attrs();
        assertFalse(si.share_info.containsKey("item_type"));
        assertFalse(si.share_info.containsKey("parent"));
        assertTrue(si.share_info.containsKey("id"));
    }

    @Test
    void test_contains_and_getitem() {
        Map<String, Object> d = new HashMap<>();
        d.put("id", 99);
        d.put("foo", "bar");
        ShareInfo si = new ShareInfo(d);
        assertTrue(si.containsKey("id"));
        assertEquals("bar", si.get("foo"));
    }

}