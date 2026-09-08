package org.openjfx;

import org.apache.maven.plugin.MojoExecutionException;
import org.junit.Before;
import org.junit.Test;

import java.io.File;

public class JavaFXRunMojoPublicTest {

    private JavaFXRunMojo mojo;

    @Before
    public void setUp() {
        mojo = new JavaFXRunMojo();
        // Use a different mainClass and a different tmp subdir
        mojo.mainClass = "org.publicexample.Launcher";
        File tmpDir = new File(System.getProperty("java.io.tmpdir"), "publictestsubdir_run");
        tmpDir.mkdirs();
        mojo.basedir = tmpDir;
        mojo.builddir = tmpDir;
    }

    @Test(expected = MojoExecutionException.class)
    public void testExecuteThrowsWhenExecutableNull() throws Exception {
        // Will throw because executable is not set (private, but constructor default is "java"; so forcibly set)
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