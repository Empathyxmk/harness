using System;
using System.IO;
using OpenJfxJavafxMavenPlugin;
using Xunit;

namespace OpenJfxJavafxMavenPlugin.Tests.Original
{
    public class JavaFXJLinkMojoTest
    {
        private JavaFXJLinkMojo mojo;

        public JavaFXJLinkMojoTest()
        {
            mojo = new JavaFXJLinkMojo();
            mojo.mainClass = "com.example.Main";
            mojo.basedir = new DirectoryInfo(Path.GetTempPath());
            mojo.builddir = new DirectoryInfo(Path.GetTempPath());
        }

        [Fact]
        public void TestExecuteWithException()
        {
            // Should throw because of incomplete setup (simulate by making one required field null)
            mojo.mainClass = null;
            Assert.ThrowsAny<Exception>(() => mojo.Execute());
        }
    }
}