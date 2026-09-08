using System;
using System.Collections.Generic;
using Xunit;

namespace JustOne.Kafka.Sink.Pg.Json.Tests
{
    // Stub class for SinkRecord to mimic Kafka Connect SinkRecord behavior
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

    // Skeleton implementation for PostgreSQLSinkTask for testability
    public class PostgreSQLSinkTask
    {
        public string Version() => "1.0";
        public void Start(IDictionary<string, string> props) { /* Simulate startup, no-op */ }
        public void Stop() { /* Simulate shutdown, no-op */ }
        public void Put(IEnumerable<SinkRecord> records) { /* Simulate data ingestion, no-op */ }
    }

    public class PostgreSQLSinkTaskTests
    {
        private PostgreSQLSinkTask task;

        public PostgreSQLSinkTaskTests()
        {
            task = new PostgreSQLSinkTask();
        }

        [Fact]
        public void TestVersion()
        {
            Assert.Equal("1.0", task.Version());
        }

        [Fact]
        public void TestStartAndStop()
        {
            var props = new Dictionary<string, string> { { "a", "b" } };
            task.Start(props);
            task.Stop();
        }

        [Fact]
        public void TestPut()
        {
            var records = new List<SinkRecord>
            {
                new SinkRecord("topic", 0, null, null, null, null, 0)
            };
            task.Put(records);
        }
    }
}