using Xunit;

namespace Vasco.Tests.Original
{
    public class CallSiteTest
    {
        private class DummyContext : Context<string, string, int>
        {
            private readonly int id;
            public DummyContext(int id) : base("m", default, false)
            {
                this.id = id;
            }
            public override int GetId() => id;

            public override bool Equals(object obj)
            {
                if (!(obj is DummyContext d)) return false;
                return this.id == d.id;
            }
            public override int GetHashCode() => id;
        }

        [Fact]
        public void TestEqualsAndHashCode()
        {
            var ctx1 = new DummyContext(1);
            var ctx2 = new DummyContext(2);
            var cs1 = new CallSite<string, string, int>(ctx1, "call1");
            var cs2 = new CallSite<string, string, int>(ctx1, "call1");
            var cs3 = new CallSite<string, string, int>(ctx1, "call2");
            var cs4 = new CallSite<string, string, int>(ctx2, "call1");

            Assert.True(cs1.Equals(cs2));
            Assert.Equal(cs1.GetHashCode(), cs2.GetHashCode());

            Assert.False(cs1.Equals(cs3));
            Assert.False(cs1.Equals(cs4));
            Assert.False(cs1.Equals(null));
            Assert.False(cs1.Equals("SomeString"));
        }

        [Fact]
        public void TestCompareTo()
        {
            var ctx1 = new DummyContext(1);
            var ctx2 = new DummyContext(4);

            var cs1 = new CallSite<string, string, int>(ctx1, "c1");
            var cs2 = new CallSite<string, string, int>(ctx2, "c1");

            Assert.True(cs1.CompareTo(cs2) < 0);
            Assert.True(cs2.CompareTo(cs1) > 0);
            Assert.Equal(0, cs1.CompareTo(new CallSite<string, string, int>(ctx1, "c2")));
        }

        [Fact]
        public void TestGettersToString()
        {
            var ctx1 = new DummyContext(42);
            var cs1 = new CallSite<string, string, int>(ctx1, "stmtNode");
            Assert.Equal(ctx1, cs1.GetCallingContext());
            Assert.Equal("stmtNode", cs1.GetCallNode());
            Assert.Contains("42", cs1.ToString());
            Assert.Contains("stmtNode", cs1.ToString());
        }
    }
}