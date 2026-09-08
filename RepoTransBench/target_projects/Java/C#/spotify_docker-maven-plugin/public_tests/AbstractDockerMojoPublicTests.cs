using System;
using Xunit;
using ProjectName;

namespace PublicTests
{
    public class AbstractDockerMojoPublicTests
    {
        [Fact]
        public void TestRegistryUrlReplacePublic()
        {
            var mojo = new ConcreteDockerMojo();
            var url = mojo.ReplaceRegistryUrl("index.docker.io", "my.other.io");
            Assert.Equal("my.other.io", url);
        }
    }
}