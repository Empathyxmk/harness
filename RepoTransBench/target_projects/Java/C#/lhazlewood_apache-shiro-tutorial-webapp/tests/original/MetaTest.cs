using System;
using Xunit;
using System.IO;

namespace OriginalTests
{
    public class MetaTest
    {
        [Fact]
        public void TestProjectStructureExists()
        {
            Assert.True(File.Exists("pom.xml"), "pom.xml should exist");
            Assert.True(File.Exists("README.md"), "README.md should exist");
        }
    }
}