package org.openjfx;

import org.codehaus.plexus.languages.java.jpms.JavaModuleDescriptor;
import org.junit.AfterClass;
import org.junit.Assert;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Comparator;

import static org.openjfx.model.RuntimePathOption.CLASSPATH;
import static org.openjfx.model.RuntimePathOption.MODULEPATH;

public class JavaFXBaseMojoPublicTest {

    private static Path publicPath;
    private static String tempDirPath;

    private JavaFXBaseMojo mojo;
    private JavaModuleDescriptor moduleDescriptor;

    @BeforeClass
    public static void setup() throws IOException {
        tempDirPath = System.getProperty("java.io.tmpdir");
        publicPath = Files.createDirectories(Paths.get(tempDirPath, "publictest", "pubdir"));
    }

    @Before
    public void create() {
        mojo = new JavaFXBaseMojo() {
            @Override
            public void execute() {
                //no-op
            }
        };
        moduleDescriptor = JavaModuleDescriptor.newModule("publicmodule").build();
    }

    @Test
    public void parentTest() {
        Assert.assertEquals(Paths.get(tempDirPath), JavaFXBaseMojo.getParent(publicPath, 2));
    }

    @Test
    public void mainClassStringWithModuleDescriptor() {
        Assert.assertEquals("publicmodule/com.publicexample.Main", 
            mojo.createMainClassString("com.publicexample.Main", moduleDescriptor, null));
    }

    @Test
    public void mainClassStringWithoutModuleDescriptor() {
        Assert.assertEquals("com.publicexample.Main", 
            mojo.createMainClassString("com.publicexample.Main", null, null));
        Assert.assertEquals("publicmodule/com.publicexample.Main", 
            mojo.createMainClassString("publicmodule/com.publicexample.Main", null, null));
    }

    @Test
    public void mainClassStringWithClasspathWithModuleDescriptor() {
        Assert.assertEquals("com.publicexample.Main", 
            mojo.createMainClassString("com.publicexample.Main", moduleDescriptor, CLASSPATH));
        Assert.assertEquals("com.publicexample.Main", 
            mojo.createMainClassString("publicmodule/com.publicexample.Main", moduleDescriptor, CLASSPATH));
    }

    @Test
    public void mainClassStringWithClasspathWithoutModuleDescriptor() {
        Assert.assertEquals("com.publicexample.Main", 
            mojo.createMainClassString("com.publicexample.Main", null, CLASSPATH));
        Assert.assertEquals("com.publicexample.Main", 
            mojo.createMainClassString("publicmodule/com.publicexample.Main", null, CLASSPATH));
    }

    @Test
    public void mainClassStringWithModulepathWithModuleDescriptor() {
        Assert.assertEquals("publicmodule/com.publicexample.Main", 
            mojo.createMainClassString("com.publicexample.Main", moduleDescriptor, MODULEPATH));
        Assert.assertEquals("publicmodule/com.publicexample.Main", 
            mojo.createMainClassString("publicmodule/com.publicexample.Main", moduleDescriptor, MODULEPATH));
    }

    @Test
    public void mainClassStringWithModulepathWithoutModuleDescriptor() {
        Assert.assertEquals("com.publicexample.Main", 
            mojo.createMainClassString("com.publicexample.Main", null, MODULEPATH));
        Assert.assertEquals("publicmodule/com.publicexample.Main", 
            mojo.createMainClassString("publicmodule/com.publicexample.Main", null, MODULEPATH));
    }

    @Test
    public void invalidParentTest() {
        Assert.assertNull(JavaFXBaseMojo.getParent(publicPath, 10));
    }

    @Test
    public void invalidPathTest() {
        Assert.assertNull(JavaFXBaseMojo.getParent(Paths.get("/some-other-invalid-path"), 0));
    }

    @Test
    public void invalidPathWithDepthTest() {
        Assert.assertNull(JavaFXBaseMojo.getParent(Paths.get("/some-other-invalid-path"), 2));
    }

    @AfterClass
    public static void destroy() throws IOException {
        Files.walk(publicPath.getParent())
                .sorted(Comparator.reverseOrder())
                .map(Path::toFile)
                .filter(f -> "publictest".equals(f.getName()))
                .forEach(File::delete);
    }
}