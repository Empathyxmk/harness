using System;
using System.Collections.Generic;
using System.Reflection;
using System.Threading;
using Moq;
using Xunit;

namespace Wendy512Stream.Tests.Original
{
    public class MqttStateConfigure
    {
        private static readonly Dictionary<string, MqttStateConfigure> Instances = new();

        public static readonly string OPTIONS_HOST = "host";
        public static readonly string OPTIONS_CLIENT_ID = "clientId";

        private bool configured;

        private MqttStateConfigure() { }

        public static MqttStateConfigure GetInstance(string name)
        {
            if (!Instances.ContainsKey(name))
                Instances[name] = new MqttStateConfigure();
            return Instances[name];
        }

        public void Configure(IConfigContext ctx)
        {
            configured = true;
            var host = ctx.Instance?.GetString(OPTIONS_HOST) ?? "";
            if (string.IsNullOrWhiteSpace(host))
                throw new ArgumentException("MQTT host cannot be empty");
        }
    }

    public interface IConfigContext
    {
        IBaseProperties? Instance { get; }
        IBaseProperties Config { get; }
    }

    public interface IBaseProperties
    {
        string? GetString(string key);
        Dictionary<string, object>? Original { get; }
    }

    public class MqttStateConfigureTest
    {
        [Fact]
        public void TestSingletonInstance()
        {
            var a = MqttStateConfigure.GetInstance("foo");
            var b = MqttStateConfigure.GetInstance("foo");
            Assert.Same(a, b);

            var c = MqttStateConfigure.GetInstance("bar");
            Assert.NotSame(a, c);
        }

        [Fact]
        public void TestConfigureThrowsOnBlankHost()
        {
            var instance = MqttStateConfigure.GetInstance("t1");
            typeof(MqttStateConfigure).GetField("configured", BindingFlags.NonPublic | BindingFlags.Instance)
                ?.SetValue(instance, false);

            var mockCtx = new Mock<IConfigContext>();
            var mockProp = new Mock<IBaseProperties>();
            mockProp.Setup(p => p.GetString(MqttStateConfigure.OPTIONS_HOST)).Returns("");
            mockCtx.SetupGet(x => x.Instance).Returns(mockProp.Object);

            var ex = Assert.Throws<ArgumentException>(() => instance.Configure(mockCtx.Object));
            Assert.Contains("MQTT host cannot be empty", ex.Message);
        }
    }
}