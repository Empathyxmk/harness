using System;
using System.Globalization;
using Xunit;
using PrettyTimeLib;

namespace PrettyTimePublicTests
{
    public class PrettyTimeI18n_FR_PublicTest
    {
        [Fact]
        public void TestFrenchMinutesAgoPublic()
        {
            var pt = new PrettyTime(new CultureInfo("fr"));
            // 20 minutes ago
            var tenMinutesAgo = DateTime.Now - TimeSpan.FromMinutes(20);
            var result = pt.Format(tenMinutesAgo);
            Assert.Contains("il y a", result.ToLowerInvariant());
            Assert.Contains("minute", result.ToLowerInvariant());
        }

        [Fact]
        public void TestFrenchInFutureHoursPublic()
        {
            var pt = new PrettyTime(new CultureInfo("fr"));
            // 4 hours from now
            var future = DateTime.Now + TimeSpan.FromHours(4);
            var result = pt.Format(future);
            Assert.Contains("dans", result.ToLowerInvariant());
            Assert.Contains("heure", result.ToLowerInvariant());
        }
    }
}