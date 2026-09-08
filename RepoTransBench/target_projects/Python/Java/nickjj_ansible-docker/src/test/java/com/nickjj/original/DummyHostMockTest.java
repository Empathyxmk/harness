package com.nickjj.original;

import com.nickjj.dummy.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.regex.Pattern;

public class DummyHostMockTest {

    DummyHost getHost() {
        return new DummyHost();
    }

    @Test
    void testDockerVersion() {
        DummyHost host = getHost();
        assertEquals(0, host.run("docker --version").rc);
    }

    @Test
    void testPinnedDockerVersion() {
        DummyHost host = getHost();
        String existingDockerVersion = host.checkOutput("docker --version");
        host.run("sudo apt-get update");
        host.run("sudo apt-get upgrade");
        String dockerVersionAfterAptUpdate = host.checkOutput("docker --version");
        assertEquals(existingDockerVersion, dockerVersionAfterAptUpdate);
    }

    @Test
    void testDockerComposeV2Version() {
        DummyHost host = getHost();
        assertEquals(0, host.run("docker compose version").rc);
    }

    @Test
    void testPinnedDockerComposeV2Version() {
        DummyHost host = getHost();
        String existingDockerComposeVersion = host.checkOutput("docker compose version");
        host.run("sudo apt-get update");
        host.run("sudo apt-get upgrade");
        String dockerComposeVersionAfterAptUpdate = host.checkOutput("docker compose version");
        assertEquals(existingDockerComposeVersion, dockerComposeVersionAfterAptUpdate);
    }

    @Test
    void testAbleToAccessDockerWithoutRoot() {
        DummyHost host = getHost();
        assertTrue(host.user("test").groups.contains("docker"));
    }

    @Test
    void testDaemonJsonIsConfigured() {
        DummyHost host = getHost();
        DummyFile daemonJson = host.file("/etc/docker/daemon.json");
        assertTrue(daemonJson.contains("journald"));
        assertTrue(daemonJson.contains("8.8.8.8"));
    }

    @Test
    void testCustomizedEnvironmentSystemdUnitFile() {
        DummyHost host = getHost();
        String unitFile = "/etc/systemd/system/docker.service.d/environment.conf";
        String fileContents = host.file(unitFile).contentString;
        assertTrue(Pattern.compile("Environment=\"HTTP_PROXY=.*\"").matcher(fileContents).find());
        assertTrue(Pattern.compile("Environment=\"HTTPS_PROXY=.*\"").matcher(fileContents).find());
    }

    @Test
    void testCustomizedDaemonFlagsSystemdUnitFile() {
        DummyHost host = getHost();
        String unitFile = "/etc/systemd/system/docker.service.d/options.conf";
        String fileContents = host.file(unitFile).contentString;
        assertTrue(fileContents.contains("-H fd://"));
        assertTrue(fileContents.contains("--debug"));
    }

    @Test
    void testCustomizedSystemdOverride() {
        DummyHost host = getHost();
        String unitFile = "/etc/systemd/system/docker.service.d/custom.conf";
        String fileContents = host.file(unitFile).contentString;
        assertTrue(fileContents.contains("ATest"));
    }

    @Test
    void testDockerCleanUpCronJob() {
        DummyHost host = getHost();
        String cronConf = host.file("/etc/cron.d/docker-disk-clean-up").contentString;
        assertTrue(cronConf.contains("test docker system prune -af"));
    }

    @Test
    void testPythonDockerModule() {
        DummyHost host = getHost();
        assertEquals(0, host.run("python3-docker -c 'import docker'").rc);
    }

    @Test
    void testDaemonJsonMissingKeys() {
        DummyHost host = getHost();
        DummyFile f = host.file("/wrong/path");
        assertFalse(f.contains("journald"));
        assertFalse(f.contains("8.8.8.8"));
    }

    @Test
    void testCustomizedEnvironmentSystemdUnitFileMissingKeys() {
        DummyHost host = getHost();
        String fileContents = host.file("/wrong/path").contentString;
        if (fileContents == null) fileContents = "";
        assertFalse(Pattern.compile("Environment=\"HTTP_PROXY=.*\"").matcher(fileContents).find());
        assertFalse(Pattern.compile("Environment=\"HTTPS_PROXY=.*\"").matcher(fileContents).find());
    }

    @Test
    void testFileObjectEmpty() {
        DummyHost host = getHost();
        assertEquals("", host.file("/nonexistent/path").contentString);
    }

    @Test
    void testUserWithoutDockerGroup() {
        class NoDockerUser extends DummyUser {
            public NoDockerUser() {
                super(java.util.Collections.singletonList("test"));
            }
        }
        class NoDockerHost extends DummyHost {
            @Override
            public DummyUser user(String name) {
                return new NoDockerUser();
            }
        }
        NoDockerHost h = new NoDockerHost();
        assertFalse(h.user("test").groups.contains("docker"));
    }
}