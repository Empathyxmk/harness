using System;
using Moq;
using Xunit;
using ProjectName;

namespace OriginalTests
{
    public class PushMojoTests
    {
        [Fact]
        public void TestPush()
        {
            var pom = TestUtilities.GetPom("pom-push.xml");
            var mojo = TestUtilities.LookupMojo<PushMojo>("push", pom);
            Assert.NotNull(mojo);
            var docker = new Mock<IDockerClient>();
            mojo.Execute(docker.Object);
            docker.Verify(d => d.Push("busybox", It.IsAny<IAnsiProgressHandler>()), Times.Once());
        }

        [Fact]
        public void TestFailingPushWithRetries()
        {
            var pom = TestUtilities.GetPom("pom-push.xml");
            var mojo = TestUtilities.LookupMojo<PushMojo>("push", pom);
            Assert.NotNull(mojo);
            var docker = new Mock<IDockerClient>();
            docker.Setup(d => d.Push(It.IsAny<string>(), It.IsAny<IAnsiProgressHandler>()))
                  .Throws(new DockerException("Expected"));

            var ex = Record.Exception(() => mojo.Execute(docker.Object));
            Assert.IsType<DockerException>(ex);
            docker.Verify(d => d.Push("busybox", It.IsAny<IAnsiProgressHandler>()), Times.Exactly(4));
        }

        // ...other tests ...
    }
}