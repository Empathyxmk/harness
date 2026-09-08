using System;
using System.Reflection;
using Xunit;

namespace Orhanobut.Tracklytics.PublicTests
{
    public class TrackSuperAttributeAnnotationPublicTest
    {
        [TrackSuperAttribute]
        public void PublicDummy() { }

        [Fact]
        public void TestTrackSuperAttributePresentPublic()
        {
            var method = GetType().GetMethod("PublicDummy", BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);
            Assert.True(method.IsDefined(typeof(TrackSuperAttribute), inherit: true));
            var dep = typeof(TrackSuperAttribute).GetCustomAttribute<ObsoleteAttribute>();
            Assert.NotNull(dep);
        }
    }
}