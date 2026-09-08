using System;
using System.Collections.Generic;
using System.Linq;
using Moq;
using Xunit;

namespace Wendy512Stream.Tests.Original
{
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
        public virtual IMqttClient? GetClient() => null;
        public virtual int GetQos() => 1;
    }
    public interface IConfigContext { }
    public interface IMessage
    {
        IHeaders Headers { get; }
        object? Payload { get; }
    }
    public interface IHeaders
    {
        string GetString(string key);
    }
    public class MqttSink
    {
        public MqttStateConfigure? StateConfigure;
        public void Configure(IConfigContext ctx)
        {
            StateConfigure = MqttStateConfigure.GetInstance("any");
            StateConfigure.Configure(ctx);
        }

        public void Process(IEnumerable<IMessage> msgs)
        {
            foreach (var msg in msgs)
            {
                var topic = msg.Headers.GetString("topic");
                if (string.IsNullOrWhiteSpace(topic))
                    continue;
                Send(topic, msg.Payload?.ToString() ?? "");
            }
        }

        public void Send(string topic, string payload)
        {
            try
            {
                StateConfigure?.GetClient()?.Publish(topic, payload, StateConfigure.GetQos());
            }
            catch { /* swallow for test */ }
        }
    }
    public interface IMqttClient
    {
        void Publish(string topic, string payload, int qos);
    }

    public class MqttSinkTest
    {
        [Fact]
        public void TestConfigureCallsConfigureOnState()
        {
            var mockCtx = new Mock<IConfigContext>();
            var mockState = new Mock<MqttStateConfigure>();
            mockState.Setup(x => x.Configure(mockCtx.Object));

            var originalGetInstance = MqttStateConfigure.GetInstance;
            try
            {
                typeof(MqttStateConfigure)
                    .GetField("Instances", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Static)!
                    .SetValue(null, new Dictionary<string, MqttStateConfigure> { { "any", mockState.Object } });
                
                var sink = new MqttSink();
                sink.Configure(mockCtx.Object);
                mockState.Verify(x => x.Configure(mockCtx.Object), Times.Once());
            }
            finally
            {
                // No restore required for local static field
            }
        }

        [Fact]
        public void TestProcessIgnoresBlankTopicAndPublishesValid()
        {
            var msg1 = new Mock<IMessage>();
            var msg2 = new Mock<IMessage>();
            var headers1 = new Mock<IHeaders>();
            var headers2 = new Mock<IHeaders>();
            headers1.Setup(h => h.GetString(It.IsAny<string>())).Returns("");
            headers2.Setup(h => h.GetString(It.IsAny<string>())).Returns("topic");
            msg1.SetupGet(x => x.Headers).Returns(headers1.Object);
            msg2.SetupGet(x => x.Headers).Returns(headers2.Object);
            msg1.SetupGet(x => x.Payload).Returns("payload1");
            msg2.SetupGet(x => x.Payload).Returns("payload2");

            var mockClient = new Mock<IMqttClient>();
            var mockState = new Mock<MqttStateConfigure>();
            mockState.Setup(x => x.GetClient()).Returns(mockClient.Object);
            mockState.Setup(x => x.GetQos()).Returns(1);

            typeof(MqttStateConfigure)
                .GetField("Instances", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Static)!
                .SetValue(null, new Dictionary<string, MqttStateConfigure> { { "any", mockState.Object } });

            var sink = new MqttSink();
            sink.Configure(new Mock<IConfigContext>().Object);
            sink.StateConfigure = mockState.Object;

            sink.Process(new List<IMessage> { msg1.Object, msg2.Object });

            mockClient.Verify(cl => cl.Publish("topic", "payload2", 1), Times.Once());
        }

        [Fact]
        public void TestSendHandlesException()
        {
            var mockClient = new Mock<IMqttClient>();
            mockClient.Setup(cl => cl.Publish(It.IsAny<string>(), It.IsAny<string>(), It.IsAny<int>()))
                .Throws(new Exception());
            var mockState = new Mock<MqttStateConfigure>();
            mockState.Setup(x => x.GetClient()).Returns(mockClient.Object);
            mockState.Setup(x => x.GetQos()).Returns(0);

            typeof(MqttStateConfigure)
                .GetField("Instances", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Static)!
                .SetValue(null, new Dictionary<string, MqttStateConfigure> { { "any", mockState.Object } });

            var sink = new MqttSink();
            sink.Configure(new Mock<IConfigContext>().Object);
            sink.StateConfigure = mockState.Object;

            // Should not throw
            var ex = Record.Exception(() => sink.Send("topic", "payload"));
            Assert.Null(ex);
        }
    }
}