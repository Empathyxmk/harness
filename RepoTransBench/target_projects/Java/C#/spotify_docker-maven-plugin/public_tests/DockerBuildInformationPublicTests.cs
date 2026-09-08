using System;
using System.Collections.Generic;
using Xunit;
using ProjectName;

namespace PublicTests
{
    public class DockerBuildInformationPublicTests
    {
        [Fact]
        public void TestBuildInfoSetterGetterPublic()
        {
            var info = new DockerBuildInformation();
            info.ImageId = "publicId2";
            info.ImageName = "publicName2";
            info.Tags = new List<string> { "publicTag1", "publicTag2" };
            Assert.Equal("publicId2", info.ImageId);
            Assert.Equal("publicName2", info.ImageName);
            Assert.Equal(new List<string> { "publicTag1", "publicTag2" }, info.Tags);
        }
    }
}