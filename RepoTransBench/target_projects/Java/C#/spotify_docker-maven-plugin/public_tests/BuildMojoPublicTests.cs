using System;
using Moq;
using Xunit;
using ProjectName;

namespace PublicTests
{
    public class BuildMojoPublicTests
    {
        [Fact]
        public void TestBuildMojoWithNoPushPublic()
        {
            var pom = TestUtilities.GetPom("pom-build-skip-push.xml");
            var mojo = TestUtilities.LookupMojo<BuildMojo>("build", pom);
            Assert.NotNull(mojo);
            var docker = new Mock<IDockerClient>();
            mojo.Execute(docker.Object);
            docker.Verify(d => d.Push(It.IsAny<string>()), Times.Never());
        }

        [Fact]
        public void TestBuildMojoSkipBuildPublic()
        {
            var pom = TestUtilities.GetPom("pom-build-skip-build.xml");
            var mojo = TestUtilities.LookupMojo<BuildMojo>("build", pom);
            Assert.NotNull(mojo);
            var docker = new Mock<IDockerClient>();
            mojo.Execute(docker.Object);
            docker.Verify(d => d.Build(It.IsAny<string>(), It.IsAny<string>()), Times.Never());
        }
    }
}