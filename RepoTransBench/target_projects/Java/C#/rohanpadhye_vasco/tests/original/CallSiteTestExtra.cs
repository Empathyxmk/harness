using Xunit;

namespace Vasco.Tests.Original
{
    public class CallSiteTestExtra
    {
        [Fact]
        public void TestEqualsAndHashCode()
        {
            var cs1 = new CallSite("foo", 1);
            var cs2 = new CallSite("foo", 1);
            var cs3 = new CallSite("bar", 2);

            Assert.Equal(cs1, cs2);
            Assert.NotEqual(cs1, cs3);
            Assert.Equal(cs1.GetHashCode(), cs2.GetHashCode());
            Assert.NotEqual(cs1.GetHashCode(), cs3.GetHashCode());
        }

        [Fact]
        public void TestToString()
        {
            var cs = new CallSite("main", 3);
            string str = cs.ToString();
            Assert.Contains("main", str);
            Assert.Contains("3", str);
        }
    }
}