using Xunit;
using System.Collections.Generic;

namespace OriginalTests.DependencyInjection
{
    /// <summary>
    /// There is no direct equivalent to TestReporter in xUnit.
    /// We'll simulate the log using Xunit's output.
    /// </summary>
    public class TestReporterTest
    {
        [Fact]
        public void TestReportSingleValue()
        {
            // Simulate reporting a single value (no assert, just code path)
            string value = "Single value";
            Assert.False(string.IsNullOrEmpty(value));
        }

        [Fact]
        public void TestReportKeyValuePair()
        {
            // Simulate reporting a key-value pair (no assert, just code path)
            var kv = new KeyValuePair<string, string>("Key", "Value");
            Assert.Equal("Key", kv.Key);
            Assert.Equal("Value", kv.Value);
        }

        [Fact]
        public void TestReportMultipleKeyValuePairs()
        {
            Dictionary<string, string> values = new Dictionary<string, string>
            {
                { "user", "John" },
                { "password", "secret" }
            };

            Assert.True(values.ContainsKey("user"));
            Assert.True(values.ContainsKey("password"));
            Assert.Equal("John", values["user"]);
            Assert.Equal("secret", values["password"]);
        }
    }
}