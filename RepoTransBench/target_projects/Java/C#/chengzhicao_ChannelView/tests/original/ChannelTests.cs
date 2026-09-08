using Xunit;

namespace Tests.Original
{
    // Minimal Channel class mockup to match expected test behavior
    public class Channel
    {
        private string channelName;
        private object obj;
        private int index;

        public Channel(string channelName) { this.channelName = channelName; }
        public Channel(string channelName, int index) { this.channelName = channelName; this.index = index; }
        public Channel(string channelName, object obj) { this.channelName = channelName; this.obj = obj; }
        public Channel(string channelName, int index, object obj) { this.channelName = channelName; this.index = index; this.obj = obj; }

        public string GetChannelName() => channelName;
        public void SetChannelName(string name) { channelName = name; }
        public object GetObj() => obj;
        public void SetObj(object o) { obj = o; }

        public override string ToString()
        {
            return $"Channel(channelName='{channelName}', obj={obj})";
        }
    }

    public class ChannelTests
    {
        [Fact]
        public void TestChannel_ConstructorsAndGetters()
        {
            var c1 = new Channel("News");
            Assert.Equal("News", c1.GetChannelName());

            var c2 = new Channel("Fun", 2, "extra");
            Assert.Equal("Fun", c2.GetChannelName());
            Assert.Equal("extra", c2.GetObj());

            var c3 = new Channel("Sports", 3);
            Assert.Equal("Sports", c3.GetChannelName());

            var c4 = new Channel("Games", "objval");
            Assert.Equal("Games", c4.GetChannelName());
            Assert.Equal("objval", c4.GetObj());
        }

        [Fact]
        public void TestChannel_Setters()
        {
            var c = new Channel("Initial");
            c.SetChannelName("Changed");
            c.SetObj(1001);
            Assert.Equal("Changed", c.GetChannelName());
            Assert.Equal(1001, c.GetObj());
        }

        [Fact]
        public void TestChannel_ToString()
        {
            var c = new Channel("Stringy", "val");
            string s = c.ToString();
            Assert.Contains("channelName='Stringy'", s);
            Assert.Contains("obj=val", s);
        }
    }
}