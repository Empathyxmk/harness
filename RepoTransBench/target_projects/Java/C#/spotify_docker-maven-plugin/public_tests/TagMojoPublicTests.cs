using System;
using Moq;
using Xunit;
using ProjectName;

namespace PublicTests
{
    public class TagMojoPublicTests
    {
        [Fact]
        public void TestTagAlpha()
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
            Assert.Matches("[a-f0-9]{7,}.*", split[1]);
        }

        [Fact]
        public void TestTagBeta()
        {
            var pom = TestUtilities.GetPom("pom-tag3.xml");
            var mojo = TestUtilities.LookupMojo<TagMojo>("tag", pom);
            Assert.NotNull(mojo);
            var docker = new Mock<IDockerClient>();
            mojo.Execute(docker.Object);
            docker.Verify(d => d.Tag("imageToTag", "newRepo:newTag", false), Times.Once());
        }

        [Fact]
        public void TestTagSkipTagPublic()
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
        public void TestTagSkipDockerPublic()
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