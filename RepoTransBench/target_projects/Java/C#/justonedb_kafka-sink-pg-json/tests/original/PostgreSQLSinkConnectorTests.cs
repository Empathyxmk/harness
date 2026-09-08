using System;
using System.Collections.Generic;
using Xunit;

namespace JustOne.Kafka.Sink.Pg.Json.Tests
{
    // Stub class for ConfigDef (from Kafka Connect API)
    public class ConfigDef { }

    // Skeleton implementation for PostgreSQLSinkConnector for testability
    public class PostgreSQLSinkConnector
    {
        private IDictionary<string, string> lastProps;

        public string Version() => "1.0";

        public void Start(IDictionary<string, string> props)
        {
            lastProps = new Dictionary<string, string>(props);
        }

        public void Stop()
        {
            // Simulate no-op
        }

        public List<IDictionary<string, string>> TaskConfigs(int maxTasks)
        {
            var list = new List<IDictionary<string, string>>();
            if (lastProps == null)
                throw new InvalidOperationException("Connector not started before requesting TaskConfigs!");
            for (int i = 0; i < maxTasks; i++)
            {
                // Each task gets a copy of the props
                list.Add(new Dictionary<string, string>(lastProps));
            }
            return list;
        }

        public Type TaskClass() => typeof(PostgreSQLSinkTask);

        public ConfigDef Config() => new ConfigDef();
    }

    public class PostgreSQLSinkConnectorTests
    {
        private PostgreSQLSinkConnector connector;

        public PostgreSQLSinkConnectorTests()
        {
            connector = new PostgreSQLSinkConnector();
        }

        [Fact]
        public void TestVersion()
        {
            Assert.Equal("1.0", connector.Version());
        }

        [Fact]
        public void TestStartAndTaskConfigs()
        {
            var props = new Dictionary<string, string> { { "foo", "bar" } };
            connector.Start(props);
            var configs = connector.TaskConfigs(2);
            Assert.Equal(2, configs.Count);
            foreach (var map in configs)
            {
                Assert.NotNull(map);
                Assert.Equal("bar", map["foo"]);
            }
        }

        [Fact]
        public void TestTaskClass()
        {
            Assert.Equal(typeof(PostgreSQLSinkTask), connector.TaskClass());
        }

        [Fact]
        public void TestStop()
        {
            connector.Stop();
        }

        [Fact]
        public void TestConfig()
        {
            var configDef = connector.Config();
            Assert.NotNull(configDef);
        }
    }
}