using System;
using System.IO;
using System.Reflection;
using OpenJfxJavafxMavenPlugin;
using Xunit;

namespace OpenJfxJavafxMavenPlugin.Tests.Original
{
    public class JavaFXRunMojoTest
    {
        private JavaFXRunMojo mojo;

        public JavaFXRunMojoTest()
        {
            mojo = new JavaFXRunMojo();
            mojo.mainClass = "com.example.Main";
            mojo.basedir = new DirectoryInfo(Path.GetTempPath());
            mojo.builddir = new DirectoryInfo(Path.GetTempPath());
        }

        [Fact]
        public void TestExecuteThrowsWhenExecutableNull()
        {
            // Will throw because executable is not set
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