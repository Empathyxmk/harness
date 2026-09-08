using System;
using System.Collections.Generic;
using System.Reflection;
using Moq;
using Xunit;

namespace Wendy512Stream.Tests.Original
{
    public enum MessageRoutingMode { RoundRobinPartition, CustomPartition }
    public enum HashingScheme { JavaStringHash, Murmur3_32Hash }
    public enum ProducerCryptoFailureAction { FAIL, SEND }
    public enum CompressionType { LZ4, ZLIB }

    public class PulsarSink
    {
        public object? PulsarProducer;
        public object? PulsarClient;

        public void Configure(IConfigContext context)
        {
            // Simulate Pulsar configuration logic
            PulsarStateConfigure.GetInstance(context.InstanceName).Configure(context);
        }
        private Dictionary<string, object> InitProducerLoadConfig(Dictionary<string, object> config)
        {
            var res = new Dictionary<string, object>();
            if (config.ContainsKey("messageRoutingMode"))
            {
                var mode = config["messageRoutingMode"]?.ToString();
                if (mode?.Equals("roundrobinpartition", StringComparison.OrdinalIgnoreCase) == true)
                    res["messageRoutingMode"] = MessageRoutingMode.RoundRobinPartition;
                else if (mode?.Equals("custompartition", StringComparison.OrdinalIgnoreCase) == true)
                    res["messageRoutingMode"] = MessageRoutingMode.CustomPartition;
            }
            if (config.ContainsKey("hashingScheme"))
            {
                var scheme = config["hashingScheme"]?.ToString();
                if (scheme?.Equals("javastringhash", StringComparison.OrdinalIgnoreCase) == true)
                    res["hashingScheme"] = HashingScheme.JavaStringHash;
                else if (scheme?.Equals("murmur3_32hash", StringComparison.OrdinalIgnoreCase) == true)
                    res["hashingScheme"] = HashingScheme.Murmur3_32Hash;
            }
            if (config.ContainsKey("cryptoFailureAction"))
            {
                var crypto = config["cryptoFailureAction"]?.ToString();
                if (crypto?.Equals("fail", StringComparison.OrdinalIgnoreCase) == true)
                    res["cryptoFailureAction"] = ProducerCryptoFailureAction.FAIL;
                else if (crypto?.Equals("send", StringComparison.OrdinalIgnoreCase) == true)
                    res["cryptoFailureAction"] = ProducerCryptoFailureAction.SEND;
            }
            if (config.ContainsKey("compressionType"))
            {
                var comp = config["compressionType"]?.ToString();
                if (comp?.Equals("lz4", StringComparison.OrdinalIgnoreCase) == true)
                    res["compressionType"] = CompressionType.LZ4;
                if (comp?.Equals("zlib", StringComparison.OrdinalIgnoreCase) == true)
                    res["compressionType"] = CompressionType.ZLIB;
            }
            return res;
        }
        public void Stop()
        {
            (PulsarProducer as IDisposable)?.Dispose();
            (PulsarClient as IDisposable)?.Dispose();
        }
    }

    public class PulsarSinkTest
    {
        [Fact]
        public void TestConfigureAndInitProducer()
        {
            var sink = new PulsarSink();
            var context = new Mock<IConfigContext>();
            var props = new Mock<IBaseProperties>();
            var config = new Dictionary<string, object> { { "topicName", "test-topic" } };
            props.SetupGet(x => x.Original).Returns(config);
            context.SetupGet(x => x.InstanceName).Returns("testConfigure");
            context.SetupGet(x => x.Config).Returns(props.Object);

            var state = new Mock<PulsarStateConfigure>();
            state.Setup(x => x.Configure(context.Object));

            // Force call to Configure
            sink.Configure(context.Object);
        }

        [Fact]
        public void TestInitProducerLoadConfigBranches()
        {
            var sink = new PulsarSink();
            var config = new Dictionary<string, object>
            {
                { "messageRoutingMode", "roundrobinpartition" },
                { "hashingScheme", "javastringhash" },
                { "cryptoFailureAction", "fail" },
                { "compressionType", "lz4" }
            };
            // Reflection to call the private method
            var method = typeof(PulsarSink).GetMethod("InitProducerLoadConfig", BindingFlags.NonPublic | BindingFlags.Instance);
            Assert.NotNull(method);
            var res = (Dictionary<string, object>)method.Invoke(sink, new object[] { config })!;
            Assert.Equal(MessageRoutingMode.RoundRobinPartition, res["messageRoutingMode"]);
            Assert.Equal(HashingScheme.JavaStringHash, res["hashingScheme"]);
            Assert.Equal(ProducerCryptoFailureAction.FAIL, res["cryptoFailureAction"]);
            Assert.Equal(CompressionType.LZ4, res["compressionType"]);
        }

        [Fact]
        public void TestProcessAndStop()
        {
            var sink = new PulsarSink();

            var context = new Mock<IConfigContext>();
            var props = new Mock<IBaseProperties>();
            context.SetupGet(x => x.InstanceName).Returns("testStop");
            context.SetupGet(x => x.Config).Returns(props.Object);
            var configMap = new Dictionary<string, object> { { "topicName", "foo" } };
            props.SetupGet(x => x.Original).Returns(configMap);

            // Simulate a disposable client
            var client = new Mock<IDisposable>();
            var producer = new Mock<IDisposable>();
            sink.PulsarProducer = producer.Object;
            sink.PulsarClient = client.Object;

            sink.Stop();
            client.Verify(x => x.Dispose(), Times.AtLeastOnce());
        }
    }
}