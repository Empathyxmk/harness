using System.Collections.Generic;
using Xunit;

namespace Orhanobut.Tracklytics.Tests
{
    public class DummyTrackable : ITrackable
    {
        public Dictionary<string, object> GetTrackableAttributes() =>
            new Dictionary<string, object> { ["key"] = "val" };
    }

    public class TrackableInterfaceTest
    {
        [Fact]
        public void TestTrackableMethod()
        {
            ITrackable t = new DummyTrackable();
            var attrs = t.GetTrackableAttributes();
            Assert.Single(attrs);
            Assert.Equal("val", attrs["key"]);
        }
    }
}