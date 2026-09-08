using System;
using System.Collections.Generic;
using Xunit;
using ProjectName;

namespace OriginalTests
{
    public class CompositeImageNameTests
    {
        [Fact]
        public void TestCreate_NameWithTagAndImageTags()
        {
            var cin = CompositeImageName.Create("repo:tag1", new List<string> { "tag2", "tag3" });
            Assert.Equal("repo", cin.Name);
            Assert.Equal(new List<string> { "tag1", "tag2", "tag3" }, cin.ImageTags);
        }

        [Fact]
        public void TestCreate_NameWithoutTagButWithImageTags()
        {
            var cin = CompositeImageName.Create("repo", new List<string> { "tag2" });
            Assert.Equal("repo", cin.Name);
            Assert.Equal(new List<string> { "tag2" }, cin.ImageTags);
        }

        [Fact]
        public void TestCreate_BlankName()
        {
            Assert.Throws<MojoExecutionException>(() => CompositeImageName.Create("", new List<string> { "atag" }));
        }

        [Fact]
        public void TestCreate_NullTagsAndNoImageTag()
        {
            Assert.Throws<MojoExecutionException>(() => CompositeImageName.Create("repo", null));
        }

        [Fact]
        public void TestCreate_OnlyColon()
        {
            Assert.Throws<MojoExecutionException>(() => CompositeImageName.Create(":", new List<string> { "someTag" }));
        }

        [Fact]
        public void TestCreate_NameWithTagNoImageTags()
        {
            var cin = CompositeImageName.Create("repo:foo", null);
            Assert.Equal("repo", cin.Name);
            Assert.Equal(new List<string> { "foo" }, cin.ImageTags);
        }

        [Fact]
        public void TestContainsTag_ColonSlashLogic()
        {
            Assert.True(CompositeImageName.ContainsTag("myregistry/origin:tag1"));
            Assert.False(CompositeImageName.ContainsTag("myregistry:5000/origin"));
            Assert.True(CompositeImageName.ContainsTag("image:tag"));
            Assert.False(CompositeImageName.ContainsTag("image"));
        }

        [Fact]
        public void TestCreate_TagWithSlashAndColon()
        {
            var cin = CompositeImageName.Create("reg/some:image", new List<string> { "more" });
            Assert.Equal("reg/some", cin.Name);
            Assert.Equal(new List<string> { "image", "more" }, cin.ImageTags);
        }
    }
}