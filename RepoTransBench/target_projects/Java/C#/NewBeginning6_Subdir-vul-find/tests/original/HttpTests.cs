using Xunit;
using NewBeginning6_Subdir.Models;

namespace NewBeginning6_Subdir.Tests.Original
{
    public class HttpTests
    {
        [Fact]
        public void TestHttpApi()
        {
            try
            {
                Assert.Contains("example", Http.ToUrl("http://example.com"));
            }
            catch (System.Exception e)
            {
                Assert.True(false, e.ToString());
            }
            Assert.Equal("GET", Http.MethodType("GET"));

            Assert.NotNull(Http.Agent());
            Assert.NotNull(Http.ToStringOrNull(null));
            Assert.Null(Http.ToStringOrNull(null));
        }
    }
}