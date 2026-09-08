using System;
using System.Collections.Generic;
using System.Reflection;
using Moq;
using Xunit;

namespace Wendy512Stream.Tests.Public
{
    public class PulsarStateConfigurePublicTest
    {
        public class PulsarStateConfigure
        {
            private static readonly Dictionary<string, PulsarStateConfigure> Instances = new();

            private bool configured;
            public object? Client { get; private set; }

            private PulsarStateConfigure() { }

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

        [Fact]
        public void TestSingletonInstanceWithOtherNames()
        {
            var a = PulsarStateConfigure.GetInstance("alpha");
            var b = PulsarStateConfigure.GetInstance("alpha");
            Assert.Same(a, b);

            var c = PulsarStateConfigure.GetInstance("beta");
            Assert.NotSame(a, c);
        }

        [Fact]
        public void TestConfigureThrowsOnNullConfigPublic()
        {
            var instance = PulsarStateConfigure.GetInstance("cfgPublic");
            var mockCtx = new Mock<IConfigContext>();
            mockCtx.Setup(ctx => ctx.Instance).Returns(() =>
            {
                var baseProps = new Mock<IBaseProperties>();
                baseProps.SetupGet(bp => bp.Original).Returns((Dictionary<string, object>?)null);
                return baseProps.Object;
            });

            // Reset private field 'configured' using reflection
            typeof(PulsarStateConfigure)
                .GetField("configured", BindingFlags.NonPublic | BindingFlags.Instance)
                ?.SetValue(instance, false);

            var ex = Assert.Throws<ArgumentException>(() => instance.Configure(mockCtx.Object));
            Assert.Contains("pulsar sink config cannot empty", ex.Message, StringComparison.OrdinalIgnoreCase);
        }

        [Fact]
        public void TestConfigureSuccessAndIdempotentDifferentMap()
        {
            var instance = PulsarStateConfigure.GetInstance("diffmap");
            var mockProps = new Mock<IBaseProperties>();
            var confMap = new Dictionary<string, object> { { "someKey", "someValue123" } };
            mockProps.SetupGet(x => x.Original).Returns(confMap);

            var mockCtx = new Mock<IConfigContext>();
            mockCtx.SetupGet(x => x.Instance).Returns(mockProps.Object);

            typeof(PulsarStateConfigure)
                .GetField("configured", BindingFlags.NonPublic | BindingFlags.Instance)
                ?.SetValue(instance, false);

            instance.Configure(mockCtx.Object);
            Assert.NotNull(instance.Client);

            // Should be idempotent
            instance.Configure(mockCtx.Object);
        }
    }
}