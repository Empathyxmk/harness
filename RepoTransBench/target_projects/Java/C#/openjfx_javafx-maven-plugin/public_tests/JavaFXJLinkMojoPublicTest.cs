using System;
using System.IO;
using OpenJfxJavafxMavenPlugin;
using Xunit;

namespace OpenJfxJavafxMavenPlugin.PublicTests
{
    public class JavaFXJLinkMojoPublicTest
    {
        private JavaFXJLinkMojo mojo;

        public JavaFXJLinkMojoPublicTest()
        {
            mojo = new JavaFXJLinkMojo();
            mojo.mainClass = "org.publicexample.Launcher";
            var tmpDir = new DirectoryInfo(Path.Combine(Path.GetTempPath(), "publictestsubdir"));
            if (!tmpDir.Exists) tmpDir.Create();
            mojo.basedir = tmpDir;
            mojo.builddir = tmpDir;
        }

        [Fact]
        public void TestExecuteWithException()
        {
            // Should fail because of incomplete setup (simulate by making one required field null)
            mojo.mainClass = null;
            Assert.ThrowsAny<Exception>(() => mojo.Execute());
        }
    }
}