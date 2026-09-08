package org.openjfx;

import org.apache.maven.plugin.MojoExecutionException;
import org.junit.Before;
import org.junit.Test;

import java.io.File;

public class JavaFXJLinkMojoPublicTest {

    private JavaFXJLinkMojo mojo;

    @Before
    public void setUp() {
        mojo = new JavaFXJLinkMojo();
        // Use different mainClass and a different path in tmpdir
        mojo.mainClass = "org.publicexample.Launcher";
        File tmpDir = new File(System.getProperty("java.io.tmpdir"), "publictestsubdir");
        tmpDir.mkdirs();
        mojo.basedir = tmpDir;
        mojo.builddir = tmpDir;
    }

    @Test(expected = MojoExecutionException.class)
    public void testExecuteWithException() throws Exception {
        // Should fail because of incomplete setup
        mojo.execute();
    }
}