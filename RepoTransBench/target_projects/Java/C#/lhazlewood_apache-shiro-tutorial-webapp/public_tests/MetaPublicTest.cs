using System;
using Xunit;
using System.IO;

namespace PublicTests
{
    public class MetaPublicTest
    {
        [Fact]
        public void TestProjectRequiredFilesExist_Public()
        {
            Assert.True(File.Exists("pom.xml"), "pom.xml must be present in the repo");
            Assert.True(File.Exists("LICENSE"), "LICENSE should exist in project root");
        }
    }
}