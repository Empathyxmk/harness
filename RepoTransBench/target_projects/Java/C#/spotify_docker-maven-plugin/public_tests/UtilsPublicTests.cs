using System;
using System.IO;
using Xunit;
using ProjectName;

namespace PublicTests
{
    public class UtilsPublicTests
    {
        [Fact]
        public void TestParseImageNameForAnotherFormat()
        {
            var input = "registry.example.com/newrepo/sample:mytag";
            var result = Utils.ParseImageName(input);
            Assert.Equal("registry.example.com/newrepo/sample", result[0]);
            Assert.Equal("mytag", result[1]);
        }

        [Fact]
        public void TestParseImageName_WhenNoTagProvided()
        {
            var input = "ubuntu";
            var result = Utils.ParseImageName(input);
            Assert.Equal(new string[] { "ubuntu", null }, result);
        }

        [Fact]
        public void TestPushImageNoPush()
        {
            // Just checks that pushImage can be called without exceptions when pushImage is false.
            var pom = "not/actually/used/public";
            Utils.PushImage(null, false, "image:tag", null, pom, null, null, null);
        }

        [Fact]
        public void TestWriteImageInfoFile()
        {
            Utils.WriteImageInfoFile("image:pub", "imagetag", "target/image_pub_info.json");
            Assert.True(File.Exists("target/image_pub_info.json"));
            File.Delete("target/image_pub_info.json");
        }
    }
}