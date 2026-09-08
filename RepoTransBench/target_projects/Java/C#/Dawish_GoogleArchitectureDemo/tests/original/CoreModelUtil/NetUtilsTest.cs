using Xunit;
using Moq;
using System;
using System.Collections.Generic;

namespace DawishGoogleArchitectureDemo.Tests.Original.CoreModelUtil
{
    // Mocked network context and logic since .NET does not have Android network concepts.
    public static class NetUtils
    {
        public const int DISCONNECTED = 0;
        public const int WIFI_CONNECTED = 1;
        public const int ETHERNET_CONNECTED = 2;

        public static int GetNetConnStatus(object context)
        {
            if (context == null) return DISCONNECTED;
            var networkState = context as INetworkContext;
            if (networkState == null) return DISCONNECTED;
            if (networkState.IsWifiConnected()) return WIFI_CONNECTED;
            if (networkState.IsEthernetConnected()) return ETHERNET_CONNECTED;
            return DISCONNECTED;
        }

        public static bool IsNetConnected(object context)
        {
            if (context == null) return false;
            var networkState = context as INetworkContext;
            if (networkState == null) return false;
            return networkState.HasAnyConnection();
        }

        public static LiveBool NetConnected(object context)
        {
            bool value = IsNetConnected(context);
            return new LiveBool(value);
        }
    }

    // Simulate the Android "LiveData" class for boolean
    public class LiveBool
    {
        private readonly bool value;
        public LiveBool(bool v) { value = v; }
        public bool GetValue() => value;
    }

    public interface INetworkContext
    {
        bool IsWifiConnected();
        bool IsEthernetConnected();
        bool HasAnyConnection();
    }

    public class NetUtilsTest
    {
        private Mock<INetworkContext> mockContext;
        private Mock<INetworkContext> mockWifiContext;
        private Mock<INetworkContext> mockEthernetContext;

        public NetUtilsTest()
        {
            mockContext = new Mock<INetworkContext>();
            mockWifiContext = new Mock<INetworkContext>();
            mockEthernetContext = new Mock<INetworkContext>();
        }

        [Fact]
        public void TestGetNetConnStatus_NullContext()
        {
            int status = NetUtils.GetNetConnStatus(null);
            Assert.Equal(NetUtils.DISCONNECTED, status);
        }

        [Fact]
        public void TestGetNetConnStatus_WifiConnected()
        {
            mockWifiContext.Setup(m => m.IsWifiConnected()).Returns(true);
            mockWifiContext.Setup(m => m.IsEthernetConnected()).Returns(false);

            int status = NetUtils.GetNetConnStatus(mockWifiContext.Object);
            Assert.Equal(NetUtils.WIFI_CONNECTED, status);
        }

        [Fact]
        public void TestGetNetConnStatus_EthernetConnected()
        {
            mockEthernetContext.Setup(m => m.IsWifiConnected()).Returns(false);
            mockEthernetContext.Setup(m => m.IsEthernetConnected()).Returns(true);

            int status = NetUtils.GetNetConnStatus(mockEthernetContext.Object);
            Assert.Equal(NetUtils.ETHERNET_CONNECTED, status);
        }

        [Fact]
        public void TestGetNetConnStatus_None()
        {
            mockContext.Setup(m => m.IsWifiConnected()).Returns(false);
            mockContext.Setup(m => m.IsEthernetConnected()).Returns(false);

            int status = NetUtils.GetNetConnStatus(mockContext.Object);
            Assert.Equal(NetUtils.DISCONNECTED, status);
        }

        [Fact]
        public void TestIsNetConnected_NullContext()
        {
            Assert.False(NetUtils.IsNetConnected(null));
        }

        [Fact]
        public void TestIsNetConnected_Connected()
        {
            mockContext.Setup(m => m.HasAnyConnection()).Returns(true);
            Assert.True(NetUtils.IsNetConnected(mockContext.Object));
        }

        [Fact]
        public void TestIsNetConnected_None()
        {
            mockContext.Setup(m => m.HasAnyConnection()).Returns(false);
            Assert.False(NetUtils.IsNetConnected(mockContext.Object));
        }

        [Fact]
        public void TestNetConnected_NullContext()
        {
            var live = NetUtils.NetConnected(null);
            Assert.NotNull(live);
            Assert.False(live.GetValue());
        }
    }
}