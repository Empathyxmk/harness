using System;
using System.IO;
using System.Linq;
using OpenJfxJavafxMavenPlugin;
using OpenJfxJavafxMavenPlugin.Model;
using Xunit;

namespace OpenJfxJavafxMavenPlugin.Tests.Original
{
    public class JavaFXBaseMojoTest
    {
        private static string tempDirPath = Path.GetTempPath();
        private static DirectoryInfo path = Directory.CreateDirectory(Path.Combine(tempDirPath, "test", "test"));
        private JavaFXBaseMojo mojo;
        private string moduleDescriptor;

        public JavaFXBaseMojoTest()
        {
            mojo = new JavaFXBaseMojoImpl();
            moduleDescriptor = "hellofx";
        }

        [Fact]
        public void ParentTest()
        {
            // path is .../tmp/test/test, so GetParent depth 2 should be .../tmp/test
            var expectedParent = Directory.GetParent(path.FullName);
            expectedParent = Directory.GetParent(expectedParent.FullName);
            var result = JavaFXBaseMojo.GetParent(path, 2);
            Assert.Equal(expectedParent.FullName, result.FullName);
        }

        [Fact]
        public void MainClassStringWithModuleDescriptor()
        {
            Assert.Equal("hellofx/org.openjfx.Main", mojo.CreateMainClassString("org.openjfx.Main", moduleDescriptor, null));
        }

        [Fact]
        public void MainClassStringWithoutModuleDescriptor()
        {
            Assert.Equal("org.openjfx.Main", mojo.CreateMainClassString("org.openjfx.Main", null, null));
            Assert.Equal("hellofx/org.openjfx.Main", mojo.CreateMainClassString("hellofx/org.openjfx.Main", null, null));
        }

        [Fact]
        public void MainClassStringWithClasspathWithModuleDescriptor()
        {
            Assert.Equal("org.openjfx.Main", mojo.CreateMainClassString("org.openjfx.Main", moduleDescriptor, RuntimePathOption.CLASSPATH));
            Assert.Equal("org.openjfx.Main", mojo.CreateMainClassString("hellofx/org.openjfx.Main", moduleDescriptor, RuntimePathOption.CLASSPATH));
        }

        [Fact]
        public void MainClassStringWithClasspathWithoutModuleDescriptor()
        {
            Assert.Equal("org.openjfx.Main", mojo.CreateMainClassString("org.openjfx.Main", null, RuntimePathOption.CLASSPATH));
            Assert.Equal("org.openjfx.Main", mojo.CreateMainClassString("hellofx/org.openjfx.Main", null, RuntimePathOption.CLASSPATH));
        }

        [Fact]
        public void MainClassStringWithModulepathWithModuleDescriptor()
        {
            Assert.Equal("hellofx/org.openjfx.Main", mojo.CreateMainClassString("org.openjfx.Main", moduleDescriptor, RuntimePathOption.MODULEPATH));
            Assert.Equal("hellofx/org.openjfx.Main", mojo.CreateMainClassString("hellofx/org.openjfx.Main", moduleDescriptor, RuntimePathOption.MODULEPATH));
        }

        [Fact]
        public void MainClassStringWithModulepathWithoutModuleDescriptor()
        {
            Assert.Equal("org.openjfx.Main", mojo.CreateMainClassString("org.openjfx.Main", null, RuntimePathOption.MODULEPATH));
            Assert.Equal("hellofx/org.openjfx.Main", mojo.CreateMainClassString("hellofx/org.openjfx.Main", null, RuntimePathOption.MODULEPATH));
        }

        [Fact]
        public void InvalidParentTest()
        {
            Assert.Null(JavaFXBaseMojo.GetParent(path, 10));
        }

        [Fact]
        public void InvalidPathTest()
        {
            string somePath = "/some-invalid-path";
            Assert.Null(JavaFXBaseMojo.GetParent(new DirectoryInfo(somePath), 0));
        }

        [Fact]
        public void InvalidPathWithDepthTest()
        {
            string somePath = "/some-invalid-path";
            Assert.Null(JavaFXBaseMojo.GetParent(new DirectoryInfo(somePath), 2));
        }

        private class JavaFXBaseMojoImpl : JavaFXBaseMojo
        {
            public override void Execute() { }
        }
    }
}