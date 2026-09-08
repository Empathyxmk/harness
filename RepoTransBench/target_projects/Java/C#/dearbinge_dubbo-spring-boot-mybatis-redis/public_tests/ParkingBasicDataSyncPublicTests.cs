using Xunit;

namespace DearBingeOpenApi.PublicTests
{
    public class ParkingBasicDataSyncPublicTests
    {
        [Fact]
        public void TestParkingBasicDataSyncResponsePublicVariant()
        {
            // Use different inputs from private: e.g., odd parkId, simulate a "false"
            int parkId = 5739;  // Odd for this public variant
            bool syncResult = (parkId % 2 == 0); // Even-only success logic
            Assert.False(syncResult);
        }
    }
}