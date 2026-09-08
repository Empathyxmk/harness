using System;
using System.Collections.Generic;
using System.Reflection;
using Moq;
using Xunit;

namespace Wendy512Stream.Tests.Original
{
    // These classes/interfaces are mocks or assumed (just for compile).
    public class PulsarStateConfigure
    {
        private static readonly Dictionary<string, PulsarStateConfigure> Instances = new();

        private bool configured;
        public object? Client { get; private set; }

        private PulsarStateConfigure() {}

        public static PulsarStateConfigure GetInstance(string name)
        {
            if (!Instances.ContainsKey(name))
                Instances[name] = new PulsarStateConfigure();
            return Instances[name];
        }

        public void Configure(IConfigContext ctx)
        {
            configured = true;
            var orig = ctx.Instance?.Original;
            if (orig == null)
                throw new ArgumentException("pulsar sink config cannot empty");
            this.Client = new object();
        }
    }

    public interface IConfigContext
    {
        IBaseProperties? Instance { get; }
        string InstanceName { get; }
        IBaseProperties Config { get; }
    }

    public interface IBaseProperties
    {
        Dictionary<string, object>? Original { get; }
    }

    public class PulsarStateConfigureTest
    {
        [Fact]
        public void TestSingletonInstance()
        {
            var a = PulsarStateConfigure.GetInstance("foo");
            var b = PulsarStateConfigure.GetInstance("foo");
            Assert.Same(a, b);

            var c = PulsarStateConfigure.GetInstance("bar");
            Assert.NotSame(a, c);
        }

        [Fact]
        public void TestConfigureThrowsOnNullConfig()
        {
            var instance = PulsarStateConfigure.GetInstance("cfgtest");
            var mockCtx = new Mock<IConfigContext>();
            mockCtx.Setup(ctx => ctx.Instance).Returns(() =>
            {
                var baseProps = new Mock<IBaseProperties>();
                baseProps.SetupGet(bp => bp.Original).Returns((Dictionary<string, object>?)null);
                return baseProps.Object;
            });

            // Reset private field 'configured' using reflection
            typeof(PulsarStateConfigure).GetField("configured", BindingFlags.NonPublic | BindingFlags.Instance)
                ?.SetValue(instance, false);

            var ex = Assert.Throws<ArgumentException>(() => instance.Configure(mockCtx.Object));
            Assert.Contains("pulsar sink config cannot empty", ex.Message);
        }

        [Fact]
        public void TestConfigureSuccessAndIdempotent()
        {
            var instance = PulsarStateConfigure.GetInstance("idemp");
            var configDict = new Dictionary<string, object> { { "foo", "bar" } };

            var mockProps = new Mock<IBaseProperties>();
            mockProps.SetupGet(x => x.Original).Returns(configDict);
            var mockCtx = new Mock<IConfigContext>();
            mockCtx.SetupGet(x => x.Instance).Returns(mockProps.Object);

            // Reset private field
            typeof(PulsarStateConfigure).GetField("configured", BindingFlags.NonPublic | BindingFlags.Instance)
                ?.SetValue(instance, false);

            instance.Configure(mockCtx.Object);
            Assert.NotNull(instance.Client);

            // Should be idempotent
            instance.Configure(mockCtx.Object);
        }
    }
}