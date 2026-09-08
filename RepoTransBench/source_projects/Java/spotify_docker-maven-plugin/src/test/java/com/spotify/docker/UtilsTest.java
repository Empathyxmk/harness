package com.spotify.docker;

import org.apache.maven.plugin.MojoExecutionException;
import org.junit.Test;

import static org.junit.Assert.*;

public class UtilsTest {

    @Test
    public void testParseImageName_Tagged() throws Exception {
        String[] result = Utils.parseImageName("foo/bar:latest");
        assertEquals("foo/bar", result[0]);
        assertEquals("latest", result[1]);
    }

    @Test
    public void testParseImageName_NoTag() throws Exception {
        String[] result = Utils.parseImageName("foo/bar");
        assertEquals("foo/bar", result[0]);
        assertNull(result[1]);
    }

    @Test
    public void testParseImageName_RepoPort() throws Exception {
        String[] result = Utils.parseImageName("myregistry:4000/bar");
        assertEquals("myregistry:4000/bar", result[0]);
        assertNull(result[1]);
    }

    @Test
    public void testParseImageName_EmptyTag() throws Exception {
        String[] result = Utils.parseImageName("foo/bar:");
        assertEquals("foo/bar", result[0]);
        assertNull(result[1]);
    }

    @Test(expected = MojoExecutionException.class)
    public void testParseImageName_Error() throws Exception {
        Utils.parseImageName(null);
    }
}