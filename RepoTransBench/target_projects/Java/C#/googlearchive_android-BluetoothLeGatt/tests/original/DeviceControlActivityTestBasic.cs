using Xunit;
using BluetoothLeGatt;

namespace Tests.Original
{
    public class DeviceControlActivityTestBasic
    {
        [Fact]
        public void ExtrasConstantsAreNotNull()
        {
            Assert.NotNull(DeviceControlActivity.EXTRAS_DEVICE_NAME);
            Assert.NotNull(DeviceControlActivity.EXTRAS_DEVICE_ADDRESS);
        }
    }
}