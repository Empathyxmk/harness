using System;
using Xunit;
using aegis1980_WifiHotSpot;

namespace aegis1980_WifiHotSpot.Tests
{
    public class WifiHotSpotTest
    {
        [Fact]
        public void TestHotspotStartStop()
        {
            var hotspot = new WifiHotSpot();
            Assert.False(hotspot.IsStarted);

            hotspot.Start();
            Assert.True(hotspot.IsStarted);

            hotspot.Stop();
            Assert.False(hotspot.IsStarted);
        }

        [Fact]
        public void TestConnectDisconnectDevice()
        {
            var hotspot = new WifiHotSpot();
            hotspot.Start();

            string deviceName = "DeviceA";
            Assert.False(hotspot.IsDeviceConnected(deviceName));

            hotspot.ConnectDevice(deviceName);
            Assert.True(hotspot.IsDeviceConnected(deviceName));

            hotspot.DisconnectDevice(deviceName);
            Assert.False(hotspot.IsDeviceConnected(deviceName));
        }

        [Fact]
        public void TestCannotConnectWhenStopped()
        {
            var hotspot = new WifiHotSpot();
            string deviceName = "DeviceB";

            Assert.Throws<InvalidOperationException>(() => hotspot.ConnectDevice(deviceName));
        }

        [Fact]
        public void TestConnectedDevicesList()
        {
            var hotspot = new WifiHotSpot();
            hotspot.Start();

            hotspot.ConnectDevice("Device1");
            hotspot.ConnectDevice("Device2");

            var devices = hotspot.GetConnectedDevices();
            Assert.Contains("Device1", devices);
            Assert.Contains("Device2", devices);
            Assert.Equal(2, devices.Count);

            hotspot.DisconnectDevice("Device1");
            devices = hotspot.GetConnectedDevices();
            Assert.DoesNotContain("Device1", devices);
            Assert.Single(devices);
        }
    }
}