using Xunit;
using System.Drawing;

namespace UberUX.Tests.Public
{
    public class getPolylinePublicTest
    {
        [Fact]
        public void TestDecodePolyline_DifferentCoords_Public()
        {
            // Test input
            string testPolyline = "_p~iF~ps|U_ulLnnqC_mqNvxq`@";
            var result = UberUX.getPolyline.decodePolyStatic(testPolyline);

            Assert.True(result.Count >= 2);
        }
    }
}