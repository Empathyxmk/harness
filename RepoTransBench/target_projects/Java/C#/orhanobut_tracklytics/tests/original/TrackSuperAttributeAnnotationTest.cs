using System;
using System.Reflection;
using Xunit;

namespace Orhanobut.Tracklytics.Tests
{
    public class TrackSuperAttributeAnnotationTest
    {
        [TrackSuperAttribute]
        public void Dummy() { }

        [Fact]
        public void TestTrackSuperAttributePresent()
        {
            var method = GetType().GetMethod("Dummy", BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);
            Assert.True(method.IsDefined(typeof(TrackSuperAttribute), inherit: true));
            var dep = typeof(TrackSuperAttribute).GetCustomAttribute<ObsoleteAttribute>();
            Assert.NotNull(dep);
        }
    }
}