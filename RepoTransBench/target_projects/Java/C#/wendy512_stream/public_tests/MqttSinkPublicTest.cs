using System;
using System.Collections.Generic;
using Moq;
using Xunit;

namespace Wendy512Stream.Tests.Public
{
    public class MqttSinkPublicTest
    {
        public class MqttSink
        {
            public MqttStateConfigure? StateConfigure;
            public void Configure(IConfigContext ctx)
            {
                StateConfigure = MqttStateConfigure.GetInstance("public-mqtt");
                StateConfigure.Configure(ctx);
            }
        }

        public class MqttStateConfigure
        {
            private static readonly Dictionary<string, MqttStateConfigure> Instances = new();
            public static MqttStateConfigure GetInstance(string name)
            {
                if (!Instances.ContainsKey(name))
                    Instances[name] = new MqttStateConfigure();
                return Instances[name];
            }
            public virtual void Configure(IConfigContext ctx) { }
        }

        public interface IConfigContext
        {
            string InstanceName { get; }
            IBaseProperties Config { get; }
        }
        public interface IBaseProperties
        {
            Dictionary<string, object>? Original { get; }
        }

        [Fact]
        public void TestConfigureAndInitProducerPublic()
        {
            var sink = new MqttSink();
            var context = new Mock<IConfigContext>();
            var props = new Mock<IBaseProperties>();
            var config = new Dictionary<string, object>
            {
                { "topicName", "public-mqtt-topic" },
                { "connection", "tcp://public-mqtt-broker:1883" }
            };
            props.SetupGet(x => x.Original).Returns(config);
            context.SetupGet(x => x.InstanceName).Returns("public-mqtt");
            context.SetupGet(x => x.Config).Returns(props.Object);

            var state = new Mock<MqttStateConfigure>();
            state.Setup(x => x.Configure(context.Object));
            sink.Configure(context.Object);
        }
    }
}