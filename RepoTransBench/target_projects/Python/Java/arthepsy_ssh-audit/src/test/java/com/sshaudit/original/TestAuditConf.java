package com.sshaudit.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

public class TestAuditConf {

    static class AuditConf {
        private Set<String> hosts;
        private boolean strict;
        private boolean timeout_set;
        private int timeout;

        public AuditConf() {
            this.hosts = new HashSet<String>();
            this.strict = false;
            this.timeout_set = false;
            this.timeout = 0;
        }
        public void add_host(String host) {
            hosts.add(host);
        }
        public void set_strict(boolean value) {
            this.strict = value;
        }
        public boolean is_strict() {
            return strict;
        }
        public void set_timeout(int val) {
            this.timeout_set = true;
            this.timeout = val;
        }
        public int get_timeout() {
            return this.timeout;
        }
        public boolean is_timeout_set() {
            return this.timeout_set;
        }
        public Set<String> get_hosts() {
            return hosts;
        }
    }

    @Test
    public void test_add_host() {
        AuditConf conf = new AuditConf();
        conf.add_host("example.com");
        conf.add_host("1.2.3.4");
        conf.add_host("::1");
        assertTrue(conf.get_hosts().contains("example.com"));
        assertTrue(conf.get_hosts().contains("1.2.3.4"));
        assertTrue(conf.get_hosts().contains("::1"));
        assertEquals(3, conf.get_hosts().size());
    }

    @Test
    public void test_strict_flag_set() {
        AuditConf conf = new AuditConf();
        assertFalse(conf.is_strict());
        conf.set_strict(true);
        assertTrue(conf.is_strict());
        conf.set_strict(false);
        assertFalse(conf.is_strict());
    }

    @Test
    public void test_timeout_set_and_get() {
        AuditConf conf = new AuditConf();
        assertFalse(conf.is_timeout_set());
        conf.set_timeout(15);
        assertTrue(conf.is_timeout_set());
        assertEquals(15, conf.get_timeout());
    }
}