using System.IO;
using System.Collections.Generic;
using Xunit;
using MeituanDianpingWalle;

namespace MeituanDianpingWalle.Tests
{
    public class ChannelReaderTest
    {
        [Fact]
        public void TestGetChannel_Normal()
        {
            FileInfo file = null;
            Assert.Null(ChannelReader.GetChannel(file));
        }

        [Fact]
        public void TestGetChannelInfo_Normal()
        {
            FileInfo file = null;
            Assert.Null(ChannelReader.GetChannelInfo(file));
        }

        [Fact]
        public void TestGetChannelInfoMap_NullFile()
        {
            FileInfo file = null;
            Assert.Null(ChannelReader.GetChannelInfoMap(file));
        }

        [Fact]
        public void TestParseChannel_NullString()
        {
            Assert.Null(ChannelReader.ParseChannel(null));
        }

        [Fact]
        public void TestParseChannel_Malformed()
        {
            string malformed = "{not-a-json}";
            Assert.Null(ChannelReader.ParseChannel(malformed));
        }

        [Fact]
        public void TestParseChannel_Valid()
        {
            string json = "{\"channel\":\"TestChannel\",\"extra\":{\"foo\":\"bar\"}}";
            var info = ChannelReader.ParseChannel(json);
            Assert.NotNull(info);
            Assert.Equal("TestChannel", info.Channel);
            Assert.NotNull(info.ExtraInfo);
            Assert.Equal("bar", info.ExtraInfo["foo"]);
        }

        [Fact]
        public void TestParseChannel_Valid_NoExtra()
        {
            string json = "{\"channel\":\"A\"}";
            var info = ChannelReader.ParseChannel(json);
            Assert.NotNull(info);
            Assert.Equal("A", info.Channel);
            Assert.Null(info.ExtraInfo);
        }

        [Fact]
        public void TestParseChannel_Valid_NullChannel()
        {
            string json = "{\"extra\":{\"foo\":\"bar\"}}";
            var info = ChannelReader.ParseChannel(json);
            Assert.NotNull(info);
            Assert.Null(info.Channel);
            Assert.NotNull(info.ExtraInfo);
            Assert.Equal("bar", info.ExtraInfo["foo"]);
        }
    }
}