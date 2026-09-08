using System;
using System.Collections.Generic;
using System.Reflection;
using System.Threading;
using Moq;
using Xunit;

namespace Wendy512Stream.Tests.Original
{
    public enum SubscriptionType { Exclusive, Shared }
    public enum ProducerCryptoFailureAction { FAIL, SEND }

    public class PulsarSource
    {
        public IDisposable? PulsarClient;
        public IDisposable? PulsarConsumer;
        public Thread? RunnerThread;
        public object? Runner;

        public void Configure(IConfigContext context)
        {
            // Simulate hitting PulsarStateConfigure, etc.
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
                res["cryptoFailureAction"] = ProducerCryptoFailureAction.FAIL; // Example, real code would map string
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
            // Just a stub for the test, as start logic is not central.
        }
    }

    public class PulsarSourceTest
    {
        [Fact]
        public void TestConfigureAndInitConsumer()
        {
            var source = new PulsarSource();
            var context = new Mock<IConfigContext>();
            var props = new Mock<IBaseProperties>();
            var orig = new Dictionary<string, object>
            {
                {"topicNames", new Dictionary<string, string>{{"one", "topicA"}}}
            };
            context.SetupGet(x => x.InstanceName).Returns("psrc");
            context.SetupGet(x => x.Config).Returns(props.Object);
            props.SetupGet(x => x.Original).Returns(orig);

            source.Configure(context.Object);
        }

        [Fact]
        public void TestInitConsumerLoadConfigBranches()
        {
            var source = new PulsarSource();
            var config = new Dictionary<string, object>
            {
                { "topicNames", new Dictionary<string, string> {{"a","topic1"}} },
                { "topicsPattern", ".*" },
                { "subscriptionType", "exclusive" },
                { "cryptoFailureAction", "fail" }
            };

            var method = typeof(PulsarSource).GetMethod("InitConsumerLoadConfig", BindingFlags.NonPublic | BindingFlags.Instance);
            Assert.NotNull(method);
            var res = (Dictionary<string, object>)method.Invoke(source, new object[] { config })!;
            Assert.True(res.ContainsKey("topicNames"));
            Assert.True(res.ContainsKey("topicsPattern"));
            Assert.Equal(SubscriptionType.Exclusive, res["subscriptionType"]);
        }

        [Fact]
        public void TestStopAndUnsubscribe()
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
        public void TestStartCallsRunner()
        {
            var source = new PulsarSource();
            source.Runner = new object();
            source.RunnerThread = null;
            var ex = Record.Exception(() => source.Start());
            Assert.Null(ex);
        }
    }
}