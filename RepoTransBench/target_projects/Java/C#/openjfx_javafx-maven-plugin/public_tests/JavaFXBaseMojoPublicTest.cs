using System;
using System.IO;
using System.Linq;
using OpenJfxJavafxMavenPlugin;
using OpenJfxJavafxMavenPlugin.Model;
using Xunit;

namespace OpenJfxJavafxMavenPlugin.PublicTests
{
    public class JavaFXBaseMojoPublicTest
    {
        private static string tempDirPath = Path.GetTempPath();
        private static DirectoryInfo publicPath = Directory.CreateDirectory(Path.Combine(tempDirPath, "publictest", "pubdir"));
        private JavaFXBaseMojo mojo;
        private string moduleDescriptor;

        public JavaFXBaseMojoPublicTest()
        {
            mojo = new JavaFXBaseMojoImpl();
            moduleDescriptor = "publicmodule";
        }

        [Fact]
        public void ParentTest()
        {
            var expectedParent = Directory.GetParent(publicPath.FullName);
            expectedParent = Directory.GetParent(expectedParent.FullName);
            var parent = JavaFXBaseMojo.GetParent(publicPath, 2);
            Assert.Equal(expectedParent.FullName, parent.FullName);
        }

        [Fact]
        public void MainClassStringWithModuleDescriptor()
        {
            Assert.Equal("publicmodule/com.publicexample.Main", 
                mojo.CreateMainClassString("com.publicexample.Main", moduleDescriptor, null));
        }

        [Fact]
        public void MainClassStringWithoutModuleDescriptor()
        {
            Assert.Equal("com.publicexample.Main", 
                mojo.CreateMainClassString("com.publicexample.Main", null, null));
            Assert.Equal("publicmodule/com.publicexample.Main", 
                mojo.CreateMainClassString("publicmodule/com.publicexample.Main", null, null));
        }

        [Fact]
        public void MainClassStringWithClasspathWithModuleDescriptor()
        {
            Assert.Equal("com.publicexample.Main", 
                mojo.CreateMainClassString("com.publicexample.Main", moduleDescriptor, RuntimePathOption.CLASSPATH));
            Assert.Equal("com.publicexample.Main", 
                mojo.CreateMainClassString("publicmodule/com.publicexample.Main", moduleDescriptor, RuntimePathOption.CLASSPATH));
        }

        [Fact]
        public void MainClassStringWithClasspathWithoutModuleDescriptor()
        {
            Assert.Equal("com.publicexample.Main", 
                mojo.CreateMainClassString("com.publicexample.Main", null, RuntimePathOption.CLASSPATH));
            Assert.Equal("com.publicexample.Main", 
                mojo.CreateMainClassString("publicmodule/com.publicexample.Main", null, RuntimePathOption.CLASSPATH));
        }

        [Fact]
        public void MainClassStringWithModulepathWithModuleDescriptor()
        {
            Assert.Equal("publicmodule/com.publicexample.Main", 
                mojo.CreateMainClassString("com.publicexample.Main", moduleDescriptor, RuntimePathOption.MODULEPATH));
            Assert.Equal("publicmodule/com.publicexample.Main", 
                mojo.CreateMainClassString("publicmodule/com.publicexample.Main", moduleDescriptor, RuntimePathOption.MODULEPATH));
        }

        [Fact]
        public void MainClassStringWithModulepathWithoutModuleDescriptor()
        {
            Assert.Equal("com.publicexample.Main", 
                mojo.CreateMainClassString("com.publicexample.Main", null, RuntimePathOption.MODULEPATH));
            Assert.Equal("publicmodule/com.publicexample.Main", 
                mojo.CreateMainClassString("publicmodule/com.publicexample.Main", null, RuntimePathOption.MODULEPATH));
        }

        [Fact]
        public void InvalidParentTest()
        {
            Assert.Null(JavaFXBaseMojo.GetParent(publicPath, 10));
        }

        [Fact]
        public void InvalidPathTest()
        {
            string path = "/some-other-invalid-path";
            Assert.Null(JavaFXBaseMojo.GetParent(new DirectoryInfo(path), 0));
        }

        [Fact]
        public void InvalidPathWithDepthTest()
        {
            string path = "/some-other-invalid-path";
            Assert.Null(JavaFXBaseMojo.GetParent(new DirectoryInfo(path), 2));
        }

        private class JavaFXBaseMojoImpl : JavaFXBaseMojo
        {
            public override void Execute() { }
        }
    }
}