using Xunit;
using BluetoothLeGatt;

namespace Tests.Original
{
    public class BluetoothLeServiceTestBasic
    {
        [Fact]
        public void TestStaticFieldsNotNull()
        {
            Assert.NotNull(BluetoothLeService.ACTION_GATT_CONNECTED);
            Assert.NotNull(BluetoothLeService.ACTION_GATT_DISCONNECTED);
            Assert.NotNull(BluetoothLeService.ACTION_GATT_SERVICES_DISCOVERED);
            Assert.NotNull(BluetoothLeService.ACTION_DATA_AVAILABLE);
            Assert.NotNull(BluetoothLeService.EXTRA_DATA);
            Assert.NotNull(BluetoothLeService.UUID_HEART_RATE_MEASUREMENT);
        }
    }
}