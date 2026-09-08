using System;
using Moq;
using Xunit;
using ProjectName;

namespace PublicTests
{
    public class GitPublicTests
    {
        private Mock<Repository> _repo;
        public GitPublicTests()
        {
            _repo = new Mock<Repository>();
        }

        [Fact]
        public void TestGetCommitId_WhenRepoStillNull_ThrowsException()
        {
            var git = new Git();
            git.SetRepo(null);
            Assert.Throws<MojoExecutionException>(() => git.GetCommitId());
        }

        [Fact]
        public void TestGetCommitId_WhenHeadIsMissing_ReturnsNull()
        {
            _repo.Setup(r => r.Resolve("HEAD")).Returns((string)null);
            var git = new Git();
            git.SetRepo(_repo.Object);
            var commitId = git.GetCommitId();
            Assert.Null(commitId);
        }
    }
}