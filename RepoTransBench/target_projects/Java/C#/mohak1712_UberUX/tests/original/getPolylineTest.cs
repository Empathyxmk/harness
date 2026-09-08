using Xunit;

namespace UberUX.Tests.Original
{
    public class getPolylineTest
    {
        [Fact]
        public void TestDecodePoly_ReturnsCorrectSize()
        {
            var poly = new UberUX.getPolyline();
            // polyline encoding for [(38.5, -120.2), (40.7, -120.95), (43.252, -126.453)]
            string encoded = "_p~iF~ps|U_ulLnnqC_mqNvxq`@";
            Assert.Equal(3, poly.decodePoly(encoded).Count);
        }

        [Fact]
        public void TestDecodePoly_EmptyString()
        {
            var poly = new UberUX.getPolyline();
            Assert.Empty(poly.decodePoly(""));
        }
    }
}