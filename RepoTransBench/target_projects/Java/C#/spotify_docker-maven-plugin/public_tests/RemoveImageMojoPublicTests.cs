using System;
using Moq;
using Xunit;
using ProjectName;

namespace PublicTests
{
    public class RemoveImageMojoPublicTests
    {
        [Fact]
        public void TestRemoveImageBasicPublic()
        {
            var pom = TestUtilities.GetPom("pom-removeImage.xml");
            var mojo = TestUtilities.LookupMojo<RemoveImageMojo>("removeImage", pom);
            Assert.NotNull(mojo);
            var docker = new Mock<IDockerClient>();
            docker.Setup(d => d.InspectImage("imageToRemove")).Returns((object)null);
            mojo.Execute(docker.Object);
            docker.Verify(d => d.RemoveImage(It.IsAny<string>(), It.IsAny<bool>(), It.IsAny<bool>()), Times.AtLeast(0));
        }

        [Fact]
        public void TestRemoveMultipleImagesPublic()
        {
            var pom = TestUtilities.GetPom("pom-removeMultipleImages.xml");
            var mojo = TestUtilities.LookupMojo<RemoveImageMojo>("removeImage", pom);
            Assert.NotNull(mojo);
            var docker = new Mock<IDockerClient>();
            docker.Setup(d => d.InspectImage(It.IsAny<string>())).Returns((object)null);
            mojo.Execute(docker.Object);
            docker.Verify(d => d.RemoveImage(It.IsAny<string>(), It.IsAny<bool>(), It.IsAny<bool>()), Times.AtLeast(0));
        }
    }
}