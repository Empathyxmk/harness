using System;
using System.Collections.Generic;
using Xunit;
using ProjectName;

namespace PublicTests
{
    public class CompositeImageNamePublicTests
    {
        [Fact]
        public void TestCreate_OtherNameWithTagAndImageTags()
        {
            var cin = CompositeImageName.Create("publicrepo:pub1", new List<string> { "pub2", "pub3" });
            Assert.Equal("publicrepo", cin.Name);
            Assert.Equal(new List<string> { "pub1", "pub2", "pub3" }, cin.ImageTags);
        }

        [Fact]
        public void TestCreate_OtherNameWithoutTagButWithDifferentImageTags()
        {
            var cin = CompositeImageName.Create("publicrepo", new List<string> { "pub4" });
            Assert.Equal("publicrepo", cin.Name);
            Assert.Equal(new List<string> { "pub4" }, cin.ImageTags);
        }

        [Fact]
        public void TestCreate_BlankDifferentName()
        {
            Assert.Throws<MojoExecutionException>(() => CompositeImageName.Create("   ", new List<string> { "otherTag" }));
        }

        [Fact]
        public void TestCreate_NullTagsAndNoImageTagAgain()
        {
            Assert.Throws<MojoExecutionException>(() => CompositeImageName.Create("anotherrepo", null));
        }

        [Fact]
        public void TestCreate_InvalidColonName()
        {
            Assert.Throws<MojoExecutionException>(() => CompositeImageName.Create(":/", new List<string> { "pubTag" }));
        }

        [Fact]
        public void TestCreate_NameWithTagNoImageTags_Other()
        {
            var cin = CompositeImageName.Create("otherrepo:bar", null);
            Assert.Equal("otherrepo", cin.Name);
            Assert.Equal(new List<string> { "bar" }, cin.ImageTags);
        }

        [Fact]
        public void TestContainsTag_ColonSlashDifferentLogic()
        {
            Assert.True(CompositeImageName.ContainsTag("registry2/publicorigin:mytag"));
            Assert.False(CompositeImageName.ContainsTag("registry2:8080/publicorigin"));
            Assert.True(CompositeImageName.ContainsTag("custom:latest"));
            Assert.False(CompositeImageName.ContainsTag("custom"));
        }

        [Fact]
        public void TestCreate_AnotherTagWithSlashAndColon()
        {
            var cin = CompositeImageName.Create("myreg/pubimg:release", new List<string> { "stable" });
            Assert.Equal("myreg/pubimg", cin.Name);
            Assert.Equal(new List<string> { "release", "stable" }, cin.ImageTags);
        }
    }
}