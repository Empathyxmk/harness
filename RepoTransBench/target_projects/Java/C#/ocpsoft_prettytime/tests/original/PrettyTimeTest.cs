using System;
using System.Collections.Generic;
using System.Globalization;
using Xunit;
using PrettyTimeLib;

namespace PrettyTimeTests
{
    public class PrettyTimeTest : IDisposable
    {
        private CultureInfo _origCulture;
        private DateTime _now;

        public PrettyTimeTest()
        {
            _origCulture = CultureInfo.CurrentCulture;
            CultureInfo.CurrentCulture = CultureInfo.InvariantCulture;
            _now = DateTime.Now;
        }

        [Fact]
        public void TestCeilingInterval()
        {
            var prettyTime = new PrettyTime(new DateTime(2009, 6, 17));
            Assert.Equal("1 month ago", prettyTime.Format(new DateTime(2009, 5, 20)));
        }

        [Fact]
        public void TestNullDate()
        {
            var t = new PrettyTime();
            DateTime? date = null;
            Assert.Equal("moments from now", t.Format(date));
        }

        // ... translate all other Java tests similarly,
        // including [Fact], asserts, and setup/teardown

        public void Dispose()
        {
            CultureInfo.CurrentCulture = _origCulture;
        }
    }
}