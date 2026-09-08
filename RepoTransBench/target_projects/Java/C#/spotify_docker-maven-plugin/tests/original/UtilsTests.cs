using System;
using Xunit;
using ProjectName;

namespace OriginalTests
{
    public class UtilsTests
    {
        [Fact]
        public void TestParseImageName_Tagged()
        {
            var result = Utils.ParseImageName("foo/bar:latest");
            Assert.Equal("foo/bar", result[0]);
            Assert.Equal("latest", result[1]);
        }

        [Fact]
        public void TestParseImageName_NoTag()
        {
            var result = Utils.ParseImageName("foo/bar");
            Assert.Equal("foo/bar", result[0]);
            Assert.Null(result[1]);
        }

        [Fact]
        public void TestParseImageName_RepoPort()
        {
            var result = Utils.ParseImageName("myregistry:4000/bar");
            Assert.Equal("myregistry:4000/bar", result[0]);
            Assert.Null(result[1]);
        }

        [Fact]
        public void TestParseImageName_EmptyTag()
        {
            var result = Utils.ParseImageName("foo/bar:");
            Assert.Equal("foo/bar", result[0]);
            Assert.Null(result[1]);
        }

        [Fact]
        public void TestParseImageName_Error()
        {
            Assert.Throws<MojoExecutionException>(() => Utils.ParseImageName(null));
        }
    }
}