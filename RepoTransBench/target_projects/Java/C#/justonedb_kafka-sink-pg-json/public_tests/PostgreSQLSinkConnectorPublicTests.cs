using System;
using System.Collections.Generic;
using Xunit;

namespace JustOne.Kafka.Sink.Pg.Json.PublicTests
{
    public class ConfigDef { }

    public class PostgreSQLSinkTask
    {
        public string Version() => "1.0";
        public void Start(IDictionary<string, string> props) { /* no-op */ }
        public void Stop() { /* no-op */ }
        public void Put(IEnumerable<SinkRecord> records) { /* no-op */ }
    }

    public class SinkRecord
    {
        public string Topic { get; }
        public int Partition { get; }
        public object KeySchema { get; }
        public object Key { get; }
        public object ValueSchema { get; }
        public object Value { get; }
        public long Offset { get; }

        public SinkRecord(string topic, int partition, object keySchema, object key, object valueSchema, object value, long offset)
        {
            Topic = topic;
            Partition = partition;
            KeySchema = keySchema;
            Key = key;
            ValueSchema = valueSchema;
            Value = value;
            Offset = offset;
        }
    }

    public class PostgreSQLSinkConnector
    {
        private IDictionary<string, string> lastProps;

        public string Version() => "1.0";

        public void Start(IDictionary<string, string> props)
        {
            lastProps = new Dictionary<string, string>(props);
        }

        public void Stop() { }

        public List<IDictionary<string, string>> TaskConfigs(int maxTasks)
        {
            var list = new List<IDictionary<string, string>>();
            if (lastProps == null)
                throw new InvalidOperationException("Connector not started before requesting TaskConfigs!");
            for (int i = 0; i < maxTasks; i++)
            {
                list.Add(new Dictionary<string, string>(lastProps));
            }
            return list;
        }

        public Type TaskClass() => typeof(PostgreSQLSinkTask);

        public ConfigDef Config() => new ConfigDef();
    }

    public class PostgreSQLSinkConnectorPublicTests
    {
        private PostgreSQLSinkConnector connector;

        public PostgreSQLSinkConnectorPublicTests()
        {
            connector = new PostgreSQLSinkConnector();
        }

        [Fact]
        public void TestVersionPublic()
        {
            Assert.Equal("1.0", connector.Version());
        }

        [Fact]
        public void TestStartAndTaskConfigsPublic()
        {
            var props = new Dictionary<string, string>
            {
                { "host", "localhost" },
                { "port", "5432" }
            };
            connector.Start(props);
            var configs = connector.TaskConfigs(3);
            Assert.Equal(3, configs.Count);
            foreach (var map in configs)
            {
                Assert.NotNull(map);
                Assert.Equal("localhost", map["host"]);
                Assert.Equal("5432", map["port"]);
            }
        }

        [Fact]
        public void TestTaskClassPublic()
        {
            Assert.Equal(typeof(PostgreSQLSinkTask), connector.TaskClass());
        }

        [Fact]
        public void TestStopPublic()
        {
            connector.Stop();
        }

        [Fact]
        public void TestConfigPublic()
        {
            var configDef = connector.Config();
            Assert.NotNull(configDef);
        }
    }
}