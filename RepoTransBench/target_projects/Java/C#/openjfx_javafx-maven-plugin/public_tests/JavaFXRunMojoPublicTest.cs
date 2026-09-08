using System;
using System.IO;
using System.Reflection;
using OpenJfxJavafxMavenPlugin;
using Xunit;

namespace OpenJfxJavafxMavenPlugin.PublicTests
{
    public class JavaFXRunMojoPublicTest
    {
        private JavaFXRunMojo mojo;

        public JavaFXRunMojoPublicTest()
        {
            mojo = new JavaFXRunMojo();
            mojo.mainClass = "org.publicexample.Launcher";
            var tmpDir = new DirectoryInfo(Path.Combine(Path.GetTempPath(), "publictestsubdir_run"));
            if (!tmpDir.Exists) tmpDir.Create();
            mojo.basedir = tmpDir;
            mojo.builddir = tmpDir;
        }

        [Fact]
        public void TestExecuteThrowsWhenExecutableNull()
        {
            typeof(JavaFXRunMojo)
                .GetField("executable", BindingFlags.NonPublic | BindingFlags.Instance)
                ?.SetValue(mojo, null);
            Assert.ThrowsAny<Exception>(() => mojo.Execute());
        }

        [Fact]
        public void TestSkipExecution()
        {
            mojo.skip = true;
            var exception = Record.Exception(() => mojo.Execute());
            Assert.Null(exception);
        }
    }
}