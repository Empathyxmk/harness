using System.Collections.Generic;
using Xunit;

namespace Orhanobut.Tracklytics.PublicTests
{
    public class TracklyticsPublicTest
    {
        [Fact]
        public void TestAddAndRemoveSuperAttributePublic()
        {
            var tracklytics = new Tracklytics();
            tracklytics.AddSuperAttribute("pubA", 42);
            Assert.Equal(42, tracklytics.SuperAttributes["pubA"]);
            tracklytics.RemoveSuperAttribute("pubA");
            Assert.False(tracklytics.SuperAttributes.ContainsKey("pubA"));
        }

        [Fact]
        public void TestTrackEventWithSuperAttributesPublic()
        {
            var tracklytics = new Tracklytics();
            tracklytics.AddSuperAttribute("pubX", 99);
            var attrs = new Dictionary<string, object> { ["pubY"] = "fooBar" };
            var eventObj = new Event("pEvent", new[] { 8 }, new[] { "pT" }, attrs, tracklytics.SuperAttributes);
            var all = eventObj.GetAllAttributes();
            Assert.Equal("fooBar", all["pubY"]);
            Assert.Equal(99, all["pubX"]);
        }
    }
}