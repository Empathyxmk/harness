using System;
using System.Collections.Generic;
using System.Reflection;
using Xunit;
using Moq;

namespace Wendy512Stream.Tests.Public
{
    public class MqttStateConfigurePublicTest
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
                var orig = ctx.Instance?.Original;
                if (orig == null)
                    throw new ArgumentException("mqtt config cannot empty");
            }
        }

        public interface IConfigContext
        {
            IBaseProperties? Instance { get; }
            IBaseProperties Config { get; }
        }
        public interface IBaseProperties
        {
            Dictionary<string, object>? Original { get; }
        }

        [Fact]
        public void TestSingletonInstancePublic()
        {
            var a = MqttStateConfigure.GetInstance("uniqueOne");
            var b = MqttStateConfigure.GetInstance("uniqueOne");
            Assert.Same(a, b);

            var c = MqttStateConfigure.GetInstance("uniqueTwo");
            Assert.NotSame(a, c);
        }

        [Fact]
        public void TestConfigureThrowsOnNullPublic()
        {
            var instance = MqttStateConfigure.GetInstance("cfgPublic");
            var mockCtx = new Mock<IConfigContext>();
            var mockBase = new Mock<IBaseProperties>();
            mockBase.SetupGet(x => x.Original).Returns((Dictionary<string, object>?)null);
            mockCtx.SetupGet(x => x.Instance).Returns(mockBase.Object);

            typeof(MqttStateConfigure)
                .GetField("configured", BindingFlags.NonPublic | BindingFlags.Instance)
                ?.SetValue(instance, false);

            var ex = Assert.Throws<ArgumentException>(() => instance.Configure(mockCtx.Object));
            Assert.Contains("mqtt config cannot empty", ex.Message, StringComparison.OrdinalIgnoreCase);
        }

        [Fact]
        public void TestConfigureSuccessIdempotentPublic()
        {
            var instance = MqttStateConfigure.GetInstance("anotherUnique");
            var mockCtx = new Mock<IConfigContext>();
            var mockProps = new Mock<IBaseProperties>();
            var dict = new Dictionary<string, object> { { "fooPublic", "barPublic" } };
            mockProps.SetupGet(x => x.Original).Returns(dict);
            mockCtx.SetupGet(x => x.Instance).Returns(mockProps.Object);

            typeof(MqttStateConfigure)
                .GetField("configured", BindingFlags.NonPublic | BindingFlags.Instance)
                ?.SetValue(instance, false);

            var ex1 = Record.Exception(() => instance.Configure(mockCtx.Object));
            Assert.Null(ex1);

            // Idempotency: call again
            var ex2 = Record.Exception(() => instance.Configure(mockCtx.Object));
            Assert.Null(ex2);
        }
    }
}