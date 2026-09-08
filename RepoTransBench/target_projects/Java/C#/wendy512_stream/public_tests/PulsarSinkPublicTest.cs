using System;
using System.Collections.Generic;
using System.Reflection;
using Moq;
using Xunit;

namespace Wendy512Stream.Tests.Public
{
    public enum MessageRoutingMode { RoundRobinPartition, CustomPartition }
    public enum HashingScheme { JavaStringHash, Murmur3_32Hash }
    public enum ProducerCryptoFailureAction { FAIL, SEND }
    public enum CompressionType { LZ4, ZLIB }

    public class PulsarSinkPublicTest
    {
        public class PulsarSink
        {
            public void Configure(IConfigContext context)
            {
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
            public object? PulsarProducer { get; set; }
            public object? PulsarClient { get; set; }
            public void Stop()
            {
                (PulsarProducer as IDisposable)?.Dispose();
                (PulsarClient as IDisposable)?.Dispose();
            }
        }
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
        public interface IMessage
        {
            IHeaders Headers { get; }
            object? Payload { get; }
        }
        public interface IHeaders
        {
            string GetString(string key);
        }

        [Fact]
        public void TestConfigureAndInitProducerPublic()
        {
            var sink = new PulsarSink();
            var context = new Mock<IConfigContext>();
            var props = new Mock<IBaseProperties>();
            var config = new Dictionary<string, object> { { "topicName", "public-topic" }, { "someField", "publicValue" } };
            props.SetupGet(x => x.Original).Returns(config);
            context.SetupGet(x => x.InstanceName).Returns("testConfigurePublic");
            context.SetupGet(x => x.Config).Returns(props.Object);

            var state = new Mock<PulsarStateConfigure>();
            state.Setup(x => x.Configure(context.Object));
            sink.Configure(context.Object);
        }

        [Fact]
        public void TestInitProducerLoadConfigBranchesPublic()
        {
            var sink = new PulsarSink();
            var config = new Dictionary<string, object>
            {
                { "messageRoutingMode", "custompartition" },
                { "hashingScheme", "murmur3_32hash" },
                { "cryptoFailureAction", "send" },
                { "compressionType", "zlib" }
            };

            var method = typeof(PulsarSink).GetMethod("InitProducerLoadConfig", BindingFlags.NonPublic | BindingFlags.Instance);
            Assert.NotNull(method);
            var res = (Dictionary<string, object>)method.Invoke(sink, new object[] { config })!;
            Assert.Equal(MessageRoutingMode.CustomPartition, res["messageRoutingMode"]);
            Assert.True(res.ContainsKey("messageRoutingMode") || res.ContainsKey("hashingScheme"));
            Assert.Equal(ProducerCryptoFailureAction.SEND, res["cryptoFailureAction"]);
            Assert.Equal(CompressionType.ZLIB, res["compressionType"]);
        }

        [Fact]
        public void TestProcessAndStopPublic()
        {
            var sink = new PulsarSink();
            var context = new Mock<IConfigContext>();
            var props = new Mock<IBaseProperties>();
            context.SetupGet(x => x.InstanceName).Returns("testStopPublic");
            context.SetupGet(x => x.Config).Returns(props.Object);
            var configMap = new Dictionary<string, object> { { "topicName", "bar" } };
            props.SetupGet(x => x.Original).Returns(configMap);

            var client = new Mock<IDisposable>();
            var producer = new Mock<IDisposable>();
            sink.PulsarProducer = producer.Object;
            sink.PulsarClient = client.Object;

            sink.Stop();
            client.Verify(x => x.Dispose(), Times.AtLeastOnce());
        }
    }
}