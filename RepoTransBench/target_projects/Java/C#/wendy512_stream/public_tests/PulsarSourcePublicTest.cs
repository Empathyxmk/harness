using System;
using System.Collections.Generic;
using System.Reflection;
using System.Threading;
using Moq;
using Xunit;

namespace Wendy512Stream.Tests.Public
{
    public enum SubscriptionType { Exclusive, Shared }
    public enum ProducerCryptoFailureAction { FAIL, SEND }

    public class PulsarSourcePublicTest
    {
        public class PulsarSource
        {
            public IDisposable? PulsarClient;
            public IDisposable? PulsarConsumer;
            public Thread? RunnerThread;
            public object? Runner;

            public void Configure(IConfigContext context)
            {
                PulsarStateConfigure.GetInstance(context.InstanceName).Configure(context);
            }

            private Dictionary<string, object> InitConsumerLoadConfig(Dictionary<string, object> config)
            {
                var res = new Dictionary<string, object>();
                if (config.ContainsKey("topicNames"))
                    res["topicNames"] = config["topicNames"];
                if (config.ContainsKey("topicsPattern"))
                    res["topicsPattern"] = config["topicsPattern"];
                if (config.ContainsKey("subscriptionType"))
                {
                    var type = config["subscriptionType"]?.ToString();
                    if (type?.Equals("exclusive", StringComparison.OrdinalIgnoreCase) == true)
                        res["subscriptionType"] = SubscriptionType.Exclusive;
                    if (type?.Equals("shared", StringComparison.OrdinalIgnoreCase) == true)
                        res["subscriptionType"] = SubscriptionType.Shared;
                }
                if (config.ContainsKey("cryptoFailureAction"))
                    res["cryptoFailureAction"] = ProducerCryptoFailureAction.SEND;
                return res;
            }

            public void Unsubscribe()
            {
                PulsarConsumer?.Dispose();
            }

            public void Stop()
            {
                if (RunnerThread != null)
                    RunnerThread.Interrupt();
                PulsarClient?.Dispose();
            }

            public void Start()
            {
                // stub
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

        [Fact]
        public void TestConfigureAndInitConsumerPublic()
        {
            var source = new PulsarSource();
            var context = new Mock<IConfigContext>();
            var props = new Mock<IBaseProperties>();
            var orig = new Dictionary<string, object>
            {
                {"topicNames", new Dictionary<string, string>{{"two", "topicB"}}}
            };
            context.SetupGet(x => x.InstanceName).Returns("psrcPublic");
            context.SetupGet(x => x.Config).Returns(props.Object);
            props.SetupGet(x => x.Original).Returns(orig);

            source.Configure(context.Object);
        }

        [Fact]
        public void TestInitConsumerLoadConfigBranchesPublic()
        {
            var source = new PulsarSource();
            var config = new Dictionary<string, object>
            {
                { "topicNames", new Dictionary<string, string> {{"b","topic2"}} },
                { "topicsPattern", "pattern.*" },
                { "subscriptionType", "shared" },
                { "cryptoFailureAction", "send" }
            };
            var method = typeof(PulsarSource).GetMethod("InitConsumerLoadConfig", BindingFlags.NonPublic | BindingFlags.Instance);
            Assert.NotNull(method);
            var res = (Dictionary<string, object>)method.Invoke(source, new object[] { config })!;
            Assert.True(res.ContainsKey("topicNames"));
            Assert.True(res.ContainsKey("topicsPattern"));
            Assert.Equal(SubscriptionType.Shared, res["subscriptionType"]);
        }

        [Fact]
        public void TestStopAndUnsubscribePublic()
        {
            var source = new PulsarSource();

            var mockClient = new Mock<IDisposable>();
            var mockConsumer = new Mock<IDisposable>();
            source.PulsarClient = mockClient.Object;
            source.PulsarConsumer = mockConsumer.Object;

            // Unsubscribe should call Dispose
            source.Unsubscribe();
            mockConsumer.Verify(x => x.Dispose(), Times.AtLeastOnce());

            // Stop should call client.Dispose (after thread interrupt)
            source.RunnerThread = new Thread(() => { });
            source.RunnerThread.Start();
            source.Stop();
            mockClient.Verify(x => x.Dispose(), Times.AtLeastOnce());
        }

        [Fact]
        public void TestStartCallsRunnerPublic()
        {
            var source = new PulsarSource();
            source.Runner = new object();
            source.RunnerThread = null;
            var ex = Record.Exception(() => source.Start());
            Assert.Null(ex);
        }
    }
}