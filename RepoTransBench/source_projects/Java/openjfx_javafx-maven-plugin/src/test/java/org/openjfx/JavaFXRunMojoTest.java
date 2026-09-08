package org.openjfx;

import org.apache.maven.plugin.MojoExecutionException;
import org.junit.Before;
import org.junit.Test;

import java.io.File;

public class JavaFXRunMojoTest {

    private JavaFXRunMojo mojo;

    @Before
    public void setUp() {
        mojo = new JavaFXRunMojo();
        // assign required parameters for testing
        mojo.mainClass = "com.example.Main";
        mojo.basedir = new File(System.getProperty("java.io.tmpdir"));
        mojo.builddir = new File(System.getProperty("java.io.tmpdir"));
    }

    @Test(expected = MojoExecutionException.class)
    public void testExecuteThrowsWhenExecutableNull() throws Exception {
        // Will throw because executable is not set (private, but constructor default is "java"; so forcibly set)
        // simulate null assignment via reflection
        java.lang.reflect.Field execField = JavaFXRunMojo.class.getDeclaredField("executable");
        execField.setAccessible(true);
        execField.set(mojo, null);
        mojo.execute();
    }

    @Test
    public void testSkipExecution() throws Exception {
        mojo.skip = true;
        mojo.execute();
        // Should not throw
    }
}