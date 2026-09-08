using System;
using Moq;
using Xunit;
using ProjectName;

namespace OriginalTests
{
    public class TagMojoTests
    {
        [Fact]
        public void TestTag1()
        {
            var pom = TestUtilities.GetPom("pom-tag1.xml");
            var mojo = TestUtilities.LookupMojo<TagMojo>("tag", pom);
            Assert.NotNull(mojo);
            var docker = new Mock<IDockerClient>();
            mojo.Execute(docker.Object);
            docker.Verify(d => d.Tag("imageToTag", "newRepo:newTag", false), Times.Once());
            docker.Verify(d => d.Push("newRepo:newTag", It.IsAny<IAnsiProgressHandler>()), Times.Once());
        }

        [Fact]
        public void TestTag2()
        {
            var pom = TestUtilities.GetPom("pom-tag2.xml");
            var mojo = TestUtilities.LookupMojo<TagMojo>("tag", pom);
            Assert.NotNull(mojo);
            var docker = new Mock<IDockerClient>();
            string capturedImage = null, capturedName = null;
            docker.Setup(d => d.Tag(It.IsAny<string>(), It.IsAny<string>(), false))
                  .Callback<string, string, bool>((img, name, force) => { capturedImage = img; capturedName = name; });
            mojo.Execute(docker.Object);
            Assert.Equal("imageToTag", capturedImage);
            var split = capturedName.Split(':');
            Assert.Equal("newRepo", split[0]);
            Assert.True(split[1].Length >= 7, $"Tag '{split[1]}' should be at least 7 characters long.");
        }

        [Fact]
        public void TestTag3()
        {
            var pom = TestUtilities.GetPom("pom-tag3.xml");
            var mojo = TestUtilities.LookupMojo<TagMojo>("tag", pom);
            Assert.NotNull(mojo);
            var docker = new Mock<IDockerClient>();
            mojo.Execute(docker.Object);
            docker.Verify(d => d.Tag("imageToTag", "newRepo:newTag", false), Times.Once());
        }

        [Fact]
        public void TestTagSkipTag()
        {
            var pom = TestUtilities.GetPom("pom-tag-skip-tag.xml");
            var mojo = TestUtilities.LookupMojo<TagMojo>("tag", pom);
            Assert.NotNull(mojo);
            Assert.True(mojo.SkipDockerTag);
            var docker = new Mock<IDockerClient>();
            mojo.Execute(docker.Object);
            docker.Verify(d => d.Tag(It.IsAny<string>(), It.IsAny<string>(), It.IsAny<bool>()), Times.Never());
        }

        [Fact]
        public void TestTagSkipDocker()
        {
            var pom = TestUtilities.GetPom("pom-tag-skip-docker.xml");
            var mojo = TestUtilities.LookupMojo<TagMojo>("tag", pom);
            Assert.True(mojo.SkipDocker);
            var mojoMock = new Mock<TagMojo> { CallBase = true };
            mojoMock.SetupAllProperties();
            mojoMock.Object.Execute();
            mojoMock.Verify(m => m.Execute(It.IsAny<IDockerClient>()), Times.Never());
        }
    }
}