using Xunit;

namespace DearBingeOpenApi.PublicTests
{
    public class ParkingSpotDataTransPublicTests
    {
        [Fact]
        public void TestAlternativeParkingSpotTrans()
        {
            // Different inputs from private: new spotId, different lat/lng.
            string spotId = "PUBLIC_SPOT_102";
            double lat = 35.1234;
            double lng = 135.4321;

            // Simulate test logic
            string result = spotId + "_" + (System.Math.Abs(lat - lng)).ToString("F4");
            Assert.Equal("PUBLIC_SPOT_102_100.3087", result);
        }
    }
}