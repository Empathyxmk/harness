package com.nickjj.publictests;

import com.nickjj.hostmock.HostMock;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class PublicHostMockTest {

    @Test
    void testAlternateHostname() {
        HostMock h = new HostMock("custom-server", "ubuntu", "debian");
        assertEquals("custom-server", h.hostname);
        assertEquals("custom-server", h.vars.get("inventory_hostname"));
    }

    @Test
    void testDifferentOsFamily() {
        HostMock h = new HostMock("web01", "fedora", "redhat");
        assertEquals("fedora", h.os);
        assertEquals("redhat", h.family);
        assertEquals("redhat", h.vars.get("ansible_os_family"));
    }

    @Test
    void testGroupsAndVarsPublic() {
        HostMock h = new HostMock(Arrays.asList("docker", "backend"), Map.of("extra", 123));
        assertEquals(Arrays.asList("docker", "backend"), h.groups);
        assertEquals(123, h.vars.get("extra"));
        assertEquals("unix:///var/run/docker.sock", h.vars.get("docker_host"));
    }

    @Test
    void testGetitemPublic() {
        HostMock h = new HostMock(Map.of("x", 100));
        assertEquals(100, h.getIndexer("x"));
    }

    @Test
    void testVarsMergingPublic() {
        HostMock h = new HostMock("merge", "ubuntu", "debian", Arrays.asList("docker"), Map.of("a", 90, "docker_host", "/tmp"));
        assertEquals(90, h.vars.get("a"));
        assertEquals("/tmp", h.vars.get("docker_host"));
        assertTrue(h.vars.containsKey("inventory_hostname"));
    }

    @Test
    void testEnvvarPublic() {
        HostMock h = new HostMock(Map.of("env", "prod"));
        assertEquals("prod", h.vars.get("env"));
    }

    @Test
    void testReprOutputPublic() {
        HostMock h = new HostMock("visual", "redhat", "rhel");
        String rep = h.toString();
        assertTrue(rep.contains("visual"));
        assertTrue(rep.contains("redhat"));
        assertTrue(rep.contains("rhel"));
    }
}