using Xunit;
using BluetoothLeGatt;

namespace Tests.Original
{
    public class DeviceScanActivityTestBasic
    {
        [Fact]
        public void ScanPeriod_Is10000()
        {
            Assert.Equal(10000L, DeviceScanActivity.SCAN_PERIOD);
        }
    }
}