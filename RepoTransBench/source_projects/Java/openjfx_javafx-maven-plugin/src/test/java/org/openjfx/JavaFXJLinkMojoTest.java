package org.openjfx;

import org.apache.maven.plugin.MojoExecutionException;
import org.junit.Before;
import org.junit.Test;

import java.io.File;

public class JavaFXJLinkMojoTest {

    private JavaFXJLinkMojo mojo;

    @Before
    public void setUp() {
        mojo = new JavaFXJLinkMojo();
        // Provide required fields
        mojo.mainClass = "com.example.Main";
        mojo.basedir = new File(System.getProperty("java.io.tmpdir"));
        mojo.builddir = new File(System.getProperty("java.io.tmpdir"));
    }

    @Test(expected = MojoExecutionException.class)
    public void testExecuteWithException() throws Exception {
        // Should fail because of incomplete setup
        mojo.execute();
    }
}