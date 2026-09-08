using System;
using Moq;
using Xunit;
using ProjectName;

namespace PublicTests
{
    public class PushMojoPublicTests
    {
        [Fact]
        public void TestPushMojoSkippedDockerPublic()
        {
            var pom = TestUtilities.GetPom("pom-push-skip-docker.xml");
            var mojo = TestUtilities.LookupMojo<PushMojo>("push", pom);
            Assert.NotNull(mojo);
            var mojoMock = new Mock<PushMojo> { CallBase = true };
            mojoMock.SetupAllProperties();
            mojoMock.Object.Execute();
            mojoMock.Verify(m => m.Execute(It.IsAny<IDockerClient>()), Times.Never());
        }

        [Fact]
        public void TestPushMojoSkippedPushPublic()
        {
            var pom = TestUtilities.GetPom("pom-push-skip-push.xml");
            var mojo = TestUtilities.LookupMojo<PushMojo>("push", pom);
            Assert.NotNull(mojo);
            var docker = new Mock<IDockerClient>();
            mojo.Execute(docker.Object);
            docker.Verify(d => d.Push(It.IsAny<string>()), Times.Never());
        }
    }
}