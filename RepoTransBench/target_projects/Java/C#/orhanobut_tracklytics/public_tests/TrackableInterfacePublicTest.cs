using System.Reflection;
using Xunit;

namespace Orhanobut.Tracklytics.PublicTests
{
    public class TrackableInterfacePublicTest
    {
        public class Bar : ITrackable
        {
            public void OnTracked(Event e) { }
        }

        [Fact]
        public void TestImplementsTrackablePublic()
        {
            var bar = new Bar();
            Assert.True(bar is ITrackable);
        }

        [Fact]
        public void TestOnTrackedMethodPresentPublic()
        {
            var method = typeof(Bar).GetMethod("OnTracked", new[] { typeof(Event) });
            Assert.NotNull(method);
        }
    }
}