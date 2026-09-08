using System;
using System.Collections.Generic;
using Xunit;
using ProjectName;

namespace OriginalTests
{
    public class DockerBuildInformationTests
    {
        private class DummyLog : ILog
        {
            public void Debug(string content) { }
            public void Debug(string content, Exception t) { }
            public void Error(string content) { }
            public void Error(string content, Exception t) { }
            public void Info(string content) { }
            public void Info(string content, Exception t) { }
            public void Warn(string content) { }
            public void Warn(string content, Exception t) { }
        }

        [Fact]
        public void TestConstructorAndGetters()
        {
            var dbi = new DockerBuildInformation("theImage", new DummyLog());
            Assert.Equal("theImage", dbi.Image);
            dbi.Digest = "digestVal";
            Assert.Equal("digestVal", dbi.Digest);
        }

        [Fact]
        public void TestToJsonBytes()
        {
            var dbi = new DockerBuildInformation("testing", new DummyLog());
            dbi.Digest = "digest";
            var json = dbi.ToJsonBytes();
            var s = System.Text.Encoding.UTF8.GetString(json);
            Assert.Contains("\"digest\"", s);
            Assert.Contains("\"image\"", s);
        }
    }
}