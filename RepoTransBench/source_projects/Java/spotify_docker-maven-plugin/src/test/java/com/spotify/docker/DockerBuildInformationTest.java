package com.spotify.docker;

import org.apache.maven.plugin.logging.Log;
import org.junit.Test;

import static org.junit.Assert.*;

public class DockerBuildInformationTest {

    private static class DummyLog implements Log {
        public void debug(CharSequence content) {}
        public void debug(CharSequence content, Throwable t) {}
        public void debug(Throwable t) {}
        public void error(CharSequence content) {}
        public void error(CharSequence content, Throwable t) {}
        public void error(Throwable t) {}
        public void info(CharSequence content) {}
        public void info(CharSequence content, Throwable t) {}
        public void info(Throwable t) {}
        public void warn(CharSequence content) {}
        public void warn(CharSequence content, Throwable t) {}
        public void warn(Throwable t) {}
    }

    @Test
    public void testConstructorAndGetters() {
        DockerBuildInformation dbi = new DockerBuildInformation("theImage", new DummyLog());
        assertEquals("theImage", dbi.getImage());
        // repo, commit may be null on a dummy log
        dbi.setDigest("digestVal");
        assertEquals("digestVal", dbi.getDigest());
    }

    @Test
    public void testToJsonBytes() {
        DockerBuildInformation dbi = new DockerBuildInformation("testing", new DummyLog());
        dbi.setDigest("digest");
        byte[] json = dbi.toJsonBytes();
        String s = new String(json);
        assertTrue(s.contains("\"digest\""));
        assertTrue(s.contains("\"image\""));
    }
}