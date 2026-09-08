using Xunit;
using System;
using Jude95_Utils;

namespace Jude95_Utils.PublicTests
{
    public class JTimeTransformPublicTest
    {
        [Fact]
        public void TestDefaultConstructorPublic()
        {
            var jtt = new JTimeTransform();
            Assert.NotNull(jtt);
            Assert.True(jtt.GetYear() > 2010 && jtt.GetYear() < 2100);
            Assert.True(jtt.GetMonth() >= 1 && jtt.GetMonth() <= 12);
            Assert.True(jtt.GetDay() >= 1 && jtt.GetDay() <= 31);
            Assert.True(jtt.GetTimestamp() > 0);
        }

        [Fact]
        public void TestLongConstructorPublic()
        {
            long fiveDaysAgo = DateTimeOffset.UtcNow.ToUnixTimeSeconds() - 432000;
            var jtt = new JTimeTransform(fiveDaysAgo);
            Assert.InRange(jtt.GetTimestamp(), fiveDaysAgo - 2, fiveDaysAgo + 2); // rounding
        }

        [Fact]
        public void TestYMDConstructorPublic()
        {
            var jtt = new JTimeTransform(2021, 10, 11); // November 11, 2021
            Assert.Equal(2021, jtt.GetYear());
            Assert.Equal(11, jtt.GetMonth());
            Assert.Equal(11, jtt.GetDay());
        }

        [Fact]
        public void TestToStringFormatPublic()
        {
            var jtt = new JTimeTransform(2020, 6, 4); // July 4, 2020
            string str = jtt.ToString("yyyy/MM/dd");
            Assert.StartsWith("2020/07/04", str);
        }

        [Fact]
        public void TestParseSuccessPublic()
        {
            var jtt = new JTimeTransform(2019, 4, 15); // May 15, 2019
            var result = jtt.Parse("yyyy/MM/dd", "2019/06/01");
            Assert.NotNull(result);
            Assert.Equal(2019, result.GetYear());
            Assert.Equal(6, result.GetMonth());
            Assert.Equal(1, result.GetDay());
        }

        [Fact]
        public void TestParseFailurePublic()
        {
            var jtt = new JTimeTransform(2018, 1, 5);
            var result = jtt.Parse("yyyy/MM/dd", "notadate");
            Assert.Null(result);
        }

        [Fact]
        public void TestRecentDateFormatPublic()
        {
            long now = DateTimeOffset.UtcNow.ToUnixTimeSeconds();
            var justNow = new JTimeTransform(now);
            var twoMinAgo = new JTimeTransform(now - 120);
            var threeHourAgo = new JTimeTransform(now - 3 * 3600);
            var twoDaysAgo = new JTimeTransform(now - 2 * 86400);
            var twoDaysLater = new JTimeTransform(now + 2 * 86400);

            var rdf = new JTimeTransform.RecentDateFormat("yyyy/MM/dd");

            string secText = rdf.Format(new JTimeTransform(now - 2), 2);
            Assert.Contains("秒", secText);

            string minText = rdf.Format(twoMinAgo, 120);
            Assert.Contains("分钟", minText);

            string hourText = rdf.Format(threeHourAgo, 3 * 3600);
            Assert.Contains("小时", hourText);

            string dtText = twoMinAgo.ToString(rdf);
            Assert.NotNull(dtText);

            string futureSec = rdf.Format(new JTimeTransform(now + 3), -3);
            Assert.Contains("秒", futureSec);

            string futureDay = rdf.Format(new JTimeTransform(now + 3600 * 50), -3600 * 50);
            Assert.Contains("天", futureDay);

            string fallbackPast = rdf.Format(twoDaysAgo, 2 * 86400);
            Assert.NotNull(fallbackPast);

            string fallbackFuture = rdf.Format(twoDaysLater, -2 * 86400);
            Assert.NotNull(fallbackFuture);
        }
    }
}