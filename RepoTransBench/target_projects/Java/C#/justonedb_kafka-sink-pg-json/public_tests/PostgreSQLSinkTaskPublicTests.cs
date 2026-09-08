using System;
using System.Collections.Generic;
using Xunit;

namespace JustOne.Kafka.Sink.Pg.Json.PublicTests
{
    // Use the same stubs as original tests
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

    public class PostgreSQLSinkTask
    {
        public string Version() => "1.0";
        public void Start(IDictionary<string, string> props) { /* Simulate startup, no-op */ }
        public void Stop() { /* Simulate shutdown, no-op */ }
        public void Put(IEnumerable<SinkRecord> records) { /* Simulate data ingestion, no-op */ }
    }

    public class PostgreSQLSinkTaskPublicTests
    {
        private PostgreSQLSinkTask task;

        public PostgreSQLSinkTaskPublicTests()
        {
            task = new PostgreSQLSinkTask();
        }

        [Fact]
        public void TestVersionPublic()
        {
            Assert.Equal("1.0", task.Version());
        }

        [Fact]
        public void TestStartAndStopPublic()
        {
            var props = new Dictionary<string, string> {
                { "username", "alice" },
                { "password", "securepass" }
            };
            task.Start(props);
            task.Stop();
        }

        [Fact]
        public void TestPutPublic()
        {
            var records = new List<SinkRecord>
            {
                // topic: "public_topic", partition: 1, offset: 123
                new SinkRecord("public_topic", 1, null, null, null, null, 123)
            };
            task.Put(records);
        }
    }
}