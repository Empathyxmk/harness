using Xunit;
using System;
using Jude95_Utils;

namespace Jude95_Utils.Tests
{
    public class JTimeTransformTest
    {
        [Fact]
        public void TestDefaultConstructor()
        {
            var jtt = new JTimeTransform();
            Assert.NotNull(jtt);
            Assert.True(jtt.GetYear() > 2000);
            Assert.True(jtt.GetMonth() > 0 && jtt.GetMonth() < 13);
            Assert.True(jtt.GetDay() > 0 && jtt.GetDay() < 32);
            Assert.True(jtt.GetTimestamp() > 0);
        }

        [Fact]
        public void TestLongConstructor()
        {
            long now = DateTimeOffset.UtcNow.ToUnixTimeSeconds();
            var jtt = new JTimeTransform(now);
            Assert.InRange(jtt.GetTimestamp(), now - 1, now + 1); // Allow for rounding
        }

        [Fact]
        public void TestYMDConstructor()
        {
            var jtt = new JTimeTransform(2023, 2, 25); // Java: 0-based month, here we match 2=March
            Assert.Equal(2023, jtt.GetYear());
            Assert.Equal(3, jtt.GetMonth());
            Assert.Equal(25, jtt.GetDay());
        }

        [Fact]
        public void TestToStringFormat()
        {
            var jtt = new JTimeTransform(2022, 0, 2); // Jan 2, 2022
            string str = jtt.ToString("yyyy-MM-dd");
            Assert.StartsWith("2022-01-02", str);
        }

        [Fact]
        public void TestParseSuccess()
        {
            var jtt = new JTimeTransform(2022, 11, 20); // Dec 20, 2022
            var result = jtt.Parse("yyyy-MM-dd", "2022-12-25");
            Assert.NotNull(result);
            Assert.Equal(2022, result.GetYear());
            Assert.Equal(12, result.GetMonth());
            Assert.Equal(25, result.GetDay());
        }

        [Fact]
        public void TestParseFailure()
        {
            var jtt = new JTimeTransform(2022, 11, 20);
            var result = jtt.Parse("yyyy-MM-dd", "abc");
            Assert.Null(result);
        }

        [Fact]
        public void TestRecentDateFormat()
        {
            long now = DateTimeOffset.UtcNow.ToUnixTimeSeconds();
            var justNow = new JTimeTransform(now);
            var oneMinAgo = new JTimeTransform(now - 60);
            var oneHourAgo = new JTimeTransform(now - 3600);
            var yesterday = new JTimeTransform(now - 86400);
            var tomorrow = new JTimeTransform(now + 86400);

            var rdf = new JTimeTransform.RecentDateFormat("yyyy-MM-dd");

            string secText = rdf.Format(new JTimeTransform(now - 1), 1);
            Assert.Contains("秒", secText);

            string minText = rdf.Format(oneMinAgo, 60 * 1);
            Assert.Contains("分钟", minText);

            string hourText = rdf.Format(oneHourAgo, 3600);
            Assert.Contains("小时", hourText);

            string dtText = oneMinAgo.ToString(rdf);
            Assert.NotNull(dtText);

            string futureSec = rdf.Format(new JTimeTransform(now + 1), -1);
            Assert.Contains("秒", futureSec);

            string futureMin = rdf.Format(new JTimeTransform(now + 80), -80);
            Assert.Contains("分钟", futureMin);

            string fallbackPast = rdf.Format(yesterday, 86400);
            Assert.NotNull(fallbackPast);

            string fallbackFuture = rdf.Format(tomorrow, -86400);
            Assert.NotNull(fallbackFuture);
        }
    }
}