using System;
using System.Collections.Generic;
using Moq;
using Xunit;
using ProjectName;

namespace OriginalTests
{
    public class RemoveImageMojoTests
    {
        [Fact]
        public void TestRemoveImage()
        {
            var pom = TestUtilities.GetPom("pom-removeImage.xml");
            var mojo = TestUtilities.LookupMojo<RemoveImageMojo>("removeImage", pom);
            Assert.NotNull(mojo);
            var docker = new Mock<IDockerClient>();
            mojo.Execute(docker.Object);
            docker.Verify(d => d.RemoveImage("imageToRemove", true, false), Times.Once());
        }

        [Fact]
        public void TestRemoveMissingImage()
        {
            var pom = TestUtilities.GetPom("pom-removeImage.xml");
            var mojo = TestUtilities.LookupMojo<RemoveImageMojo>("removeImage", pom);
            Assert.NotNull(mojo);
            var docker = new Mock<IDockerClient>();
            docker.Setup(d => d.RemoveImage("imageToRemove", true, false)).Throws(new ImageNotFoundException("imageToRemove"));
            Exception ex = Record.Exception(() => mojo.Execute(docker.Object));
            // Should not throw ImageNotFoundException
            Assert.False(ex is ImageNotFoundException, "image to remove was missing");
            docker.Verify(d => d.RemoveImage("imageToRemove", true, false), Times.Once());
        }

        [Fact]
        public void TestRemoveImageWithTags()
        {
            var pom = TestUtilities.GetPom("pom-removeMultipleImages.xml");
            var mojo = TestUtilities.LookupMojo<RemoveImageMojo>("removeImage", pom);
            Assert.NotNull(mojo);
            var docker = new Mock<IDockerClient>();
            docker.Setup(d => d.RemoveImage("imageToRemove", true, false)).Throws(new ImageNotFoundException("imageToRemove"));
            docker.Setup(d => d.RemoveImage("imageToRemove:123456", true, false)).Throws(new ImageNotFoundException("imageToRemove:123456"));
            docker.Setup(d => d.RemoveImage("imageToRemove:bbbbbbb", true, false)).Returns(new List<RemovedImage>());
            Exception ex = Record.Exception(() => mojo.Execute(docker.Object));
            // Should not throw ImageNotFoundException
            Assert.False(ex is ImageNotFoundException, "image to remove was missing");
            docker.Verify(d => d.RemoveImage("imageToRemove:123456", true, false), Times.Once());
            docker.Verify(d => d.RemoveImage("imageToRemove:bbbbbbb", true, false), Times.Once());
        }
    }
}